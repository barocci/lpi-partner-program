from django.db import models
from lib.chargify.chargify import Chargify
from lib.redmine import redmine
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
import datetime
import os

class LPIUser(User):
    company = models.CharField(max_length=100)
    management_url = models.CharField(max_length=255, null=True)
    management_url_expire = models.DateField(null=True)

    def register(self, username, password):
        user = LPIUser.objects.create_user(username, username, password)
        user.management_url = ""
        user.management_url_expire = datetime.datetime.today()
        user.is_active = False
        user.save()
        return user

    def get_management_url(self):
        if self.management_url_expire < datetime.date.today() \
            or self.management_url == '':
            url_info = self.request_new_management_url()
            if len(url_info) > 0:
                self.management_url = url_info[0].url
                self.management_url_expire = url_info[0].expires_at
                self.save()
        
        return self.management_url

    def request_new_management_url(self):
        customer = Customer().find(self.id)
        link = customer.get_management_link()
        print link
        return link

class LPIIndexes(models.Model):
    contact_id = models.IntegerField()
    contact_name = models.CharField(max_length=250, db_index=True)
    tags = models.CharField(db_index=True, max_length=250)
    cities = models.CharField(db_index=True, max_length=250)
    handle = models.CharField(max_length=100, db_index=True)
    family = models.CharField(max_length=50, db_index=True)
    lpic_id = models.CharField(max_length=20, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    references = models.IntegerField()
    teachers = models.IntegerField()
    locations = models.IntegerField()

    def search_services(self, params={}):
        result = []
        contacts = LPIIndexes.objects.filter(family__endswith='sp',status='active')
        for contact in contacts:
            result.append(self.load_from_db(contact))

        return result

    def search_academies(self, params={}):
        result = []
        contacts = LPIIndexes.objects.filter(family__startswith='aa',status='active')
        for contact in contacts:
            result.append(self.load_from_db(contact))

        return result

    def search_trainers(self, params={}):
        result = []
        contacts = LPIIndexes.objects.filter(family__startswith='at',status='active')
        for contact in contacts:
            result.append(self.load_from_db(contact))

        return result

    def load_from_db(self, item):
        contact = {}
        contact['tags'] = item.tags
        contact['contact_id'] = item.contact_id
        contact['contact_name'] = item.contact_name
        contact['cities'] = item.cities
        contact['handle'] = item.handle
        contact['family'] = item.family
        contact['lpic_id'] = item.lpic_id
        contact['status'] = item.status
        contact['references'] = item.references
        contact['teachers'] = item.teachers
        contact['locations'] = item.locations
        contact['image_url'] = LPIAvatar().company_avatar_url(contact['contact_id'])

        return contact

def LPIAvatar_filename(instance, filename):
    name, ext = os.path.splitext(filename)
    filename = "%s%s" % (instance.contact_id, ext)
    return "/".join(['logos', filename])

class LPIAvatar(models.Model):
    image = models.ImageField(null=True, upload_to=LPIAvatar_filename)
    contact_id = models.IntegerField()

    def company_avatar_url(self, contact_id):
        path = ''
        avatar = LPIAvatar.objects.filter(contact_id=contact_id).first()
        if avatar is not None:
            path = static(avatar.image.name)

        return path

class LPIRule(models.Model):
    handle = models.CharField(max_length=40,db_index=True)
    exams_discount = models.IntegerField()
    max_locations = models.IntegerField()
    max_tags = models.IntegerField()
    max_references = models.IntegerField()
    max_facebook_posts = models.IntegerField()
    max_googleplus_post = models.IntegerField()
    max_newsletter_post = models.IntegerField()
    free_exam_voucher = models.IntegerField()


    def __unicode__(self):
        return self.handle




# Create your models here.
class Model(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

        self.chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)

        self.mapping = {
          'Role':            'cf_1',
          'company_id':      'cf_2',
          'piva':            'cf_3',
          'state':           'cf_4',
          'contact_id':      'cf_5',
          'product':         'cf_6',
          'user_id':         'cf_7',
          'subscription_id': 'cf_8',
          'visible':         'cf_10',
          'LPICID':          'cf_11',
          'Verification':    'cf_12',
        }

        self.mapping_id = {
          'Role':            '1',
          'company_id':      '2',
          'piva':            '3',
          'state':           '4',
          'contact_id':      '5',
          'product':         '6',
          'user_id':         '7',
          'subscription_id': '8',
          'visible':         '10',
          'LPICID':          '11',
          'Verification':    '12'
        }

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def encode_custom_fields(self, params):
        encoded = {}
        for key, value in params.iteritems():
           if self.mapping.has_key(key):
                encoded[self.mapping[key]] = value
           else:
                encoded[key] = value

        return encoded

class Customer(Model):

    def find(self, id):
        customer = self.chargify.Customer()
        info = customer.getByReference(id)
        return self.load_from_resource(info)

    def create(self, email, first_name, last_name):
        customer = self.chargify.Customer()
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.save()
        self.load_from_resource(customer)

        return self

    def get_management_link(self):
        link = self.chargify.ManagementURL()
        return link.get(self['id'])

    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['first_name'] = resource.first_name
        self['last_name'] = resource.last_name
        self['email'] = resource.email

        return self


class ProductFamily(Model):
    def get_by_handle(self, handle):
        families = self.chargify.ProductFamily().getAll()
        for family in families:
            if family.handle == handle:
                print 'found'
                self.load_from_resource(family)

        return self

    def load_from_resource(self, resource):
        self['name'] = resource.name
        self['handle'] = resource.handle
        self['accounting_code'] = resource.accounting_code
        self['description'] = resource.description
        self['id'] = resource.id

        return self


class LPISubscription(Model):
    def create(self, product, user_id, company_id):
        deal = redmine.Deal()

        custom_fields = [
          {'id': self.mapping_id['product'], 'value': product},
          {'id': self.mapping_id['user_id'], 'value': user_id},
          {'id': self.mapping_id['state'], 'value': 'pending'} 
        ]

        deal.name = product
        deal.project_id = settings.REDMINE_PROJECT
        deal.currency = settings.CURRENCY
        deal.contact_id = company_id
        deal.custom_fields = custom_fields
        deal.save()

        self.load_from_resource(deal)

        return self

    def is_owner(self, user_id, contact_id):
        print 'checku %s  comp %s' % (user_id, contact_id)
        deals = self.find(cf_7=user_id)
        ret = False
        for deal in deals:
            if str(deal['company']) == str(contact_id):
                ret = True
                break

        print "ret: %d" % ret
        return ret

    def link_deal(self, subscription_id, user_id, product):
        # load chargify subscription info
        cs = self.chargify.Subscription().getBySubscriptionId(subscription_id)

        # get right deal by userid/handle
        subscriptions = self.find(cf_7=user_id, cf_6=product)


        if len(subscriptions) > 0:
            subscription = subscriptions[0]
            deal = redmine.Deal().find(id_=subscription['id'])

            deal.due_date = cs.current_period_ends_at
            for field in deal.custom_fields:
                if field.id == self.mapping_id['subscription_id']:
                    field.value = subscription_id
                if field.id == self.mapping_id['state']:
                    field.value = 'active'
            

            deal.save()

            self.load_from_resource(deal)

        return self

    def load_from_resource(self, resource):
        if resource.attributes.has_key('name'):
            self['name'] = resource.name
        self['id'] = resource.id
        self['due_date'] = resource.due_date

        custom_fields = {}

        for field in resource.custom_fields:
            custom_fields["cf_%s" % field.id] = field.value

        self['company'] = False
        if resource.attributes.has_key('contact'):
            self['company'] = resource.contact.id
            self['company_name'] = resource.contact.name
        #    print "looking for %s" % resource.contact.id
        #    self['company'] = Company().find(resource.contact.id)

        self['product'] = custom_fields[self.mapping['product']]
        self['user_id'] = custom_fields[self.mapping['user_id']]
        self['state'] = custom_fields[self.mapping['state']]

        return self

    def find(self, **params):
        results = []
        deals = redmine.Deal().find(**params)
        for deal in deals:
            subscription = LPISubscription().load_from_resource(deal)
            results.append(subscription)

        return results


class Subscription(Model):
    pass

class Product(Model):
    def load_from_family(self, handle):
        products = []
        family = ProductFamily().get_by_handle(handle)
        resources = self.chargify.Product().getByFamilyId(family['id'])

        for res in resources:
            product = Product()
            product.load_from_resource(res)
            products.append(product)

        return products

    def family(self):
        for key, family in settings.PRODUCT_FAMILIES.iteritems():
            if self['handle'].find(key) >= 0:
                print "%s -> %s"  % (self['handle'], family)
                return family

        return False

    def check_family(self, family, handle):
        families = family.split(',')
        for f in families:
            if handle.find(f) >= 0:
                return True

        return False

    def get_by_handle(self, handle):
        resource = self.chargify.Product().getByHandle(handle)
        return self.load_from_resource(resource)

    def hostedURL(self, product_id, user_id):
        url = "%s%s/subscriptions/new?reference=%s" % (settings.CHARGIFY_HOSTED_PAGE, product_id, user_id)
        return url

    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['name'] = resource.name
        self['handle'] = resource.handle
        self['description'] = resource.description
        self['product_family'] = resource.product_family
        self['price_in_cents'] = resource.price_in_cents
        self['image_url'] = static('lpi/%s.png' % resource.handle)

        return self
        #self['price'] = "%.2f" % int(resource.price_in_cents)/100

class Issue(Model):
    def create(self, tracker, subject, description):
        issue = redmine.Issue()
        issue.project_id = settings.REDMINE_PROJECT
        issue.tracker = tracker
        issue.subject = subject
        issue.description = description
        issue.save()

        return self.load_from_resource(issue)

    def new_registration(self, contact, product):
        pass


    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['tracker'] = resource.tracker
        self['subject'] = resource.subject
        self['description'] = resource.description

        return self

class Contact(Model):
    def find(self, id, **kwarg):
        resource = redmine.Contact.find(id_=id, **kwarg)
        return resource

    def exists(self, id):
        return redmine.Contact.exists(id)

    def edit(self, data):
        exclude = ['image_url', 'csrfmiddlewaretoken', 'type', 
                   'street', 'city', 'country', 'postcode']
        contact = redmine.Contact()
        data = self.encode_custom_fields(data)

        custom_fields = []

        for key, value in data.iteritems():
            if key in exclude: continue
            if key[:2] == 'cf':
                custom_fields.append({ 'value': value, 'id': key[3:]})
            else:
                print "setting %s = %s " % (key, value)
                setattr(contact, key, value)

        contact.custom_fields = custom_fields

        contact.address_attributes = {
            'street1': data['street'],
            'city': data['city'],
            'postcode': data['postcode'],
            'country_code': 'IT'
        }

        contact.save()
        
    def find_one(self, params):
        params = self.encode_custom_fields(params)
        print params
        resource = erdmine.Contact.find_one(**params)
        return resource

    def find_all(self, params):
        params = self.encode_custom_fields(params)
        resources = redmine.Contact.find(**params)
        return resources
        

class Company(Contact):
    def create(self, company_name, company_industry):
        contact = redmine.Contact()
        contact.is_company = True
        contact.first_name = company_name
        contact.job_title = company_industry
        contact.visibility = 1
        contact.custom_fields = [
            { 'value': 'Company', 'id': self.mapping_id['Role']}
        ]
        contact.project_id = settings.REDMINE_PROJECT
        contact.save()
        print contact.id
        return self.find(contact.id)

    def find(self, id):
        resource = Contact().find(id=id, include='contacts')
        return self.load_from_resource(resource)

    def load_from_resource(self, resource):
        print resource
        self['first_name'] = resource.first_name
        self['id'] = resource.id

        self['job_title'] = ''
        if resource.attributes.has_key('job_title'):
            self['job_title'] = resource.job_title

        self['background'] = ''
        if resource.attributes.has_key('background'):
            self['background'] = resource.background

        self['website'] = ''
        if resource.attributes.has_key('website'):
            self['website'] = resource.website

        self['phone'] = ''
        if resource.attributes.has_key('phones'):
            self['phone'] = resource.phones[0].number

        self['email'] = ''
        if resource.attributes.has_key('emails'):
            self['email'] = resource.emails[0].address

        self['tag_list'] = ''
        if resource.attributes.has_key('tag_list'):
            self['tag_list'] = resource.tag_list

        self['street'] = ''
        self['postcode'] = ''
        self['city'] = ''
        self['country'] = ''
        if resource.attributes.has_key('address'):
            address = resource.attributes['address'].attributes

            self['city'] = address['city']
            self['postcode'] = address['postcode']
            self['street'] = address['street']
            self['country'] = address['country']

        self['image_url'] = LPIAvatar().company_avatar_url(self['id'])

        self['Incharge'] = False
        self['Commercial'] = False
        self['Location'] = []
        self['Teacher'] = []
        self['Reference'] = []

        if resource.attributes.has_key('contacts'):
            for contact_resource in resource.attributes['contacts']:
                contact = Person().find(id=contact_resource.attributes['id'])

                print type(self[contact['Role']])
                
                if type(self[contact['Role']]) == type([]):
                    self[contact['Role']].append(contact)
                else:
                    self[contact['Role']] = contact

        return self

    def search_services(self, params={}):
        name = "lpi-sp|lpi-csp|lpi-csp-gold"
        return self.search(name)

    def search_academies(self, params={}):
        name = "lpi-aap|lpi-aap-pro"
        return self.search(name)

    def search_trainers(self, params={}):
        name = "lpi-atp|lpi-atp-pro"
        return self.search(name)

    def search(self, name):
        deals = redmine.Deal().find(name=name, cf_4='active')
        ids = []
        for deal in deals:
            ids.append(deal.contact.id)

        resources = redmine.Contact().find(id="|".join(ids))

        companies = []

        for res in resources:
            companies.append(Company().load_from_resource(res))

        return companies

    def find_all(self, params):
        params['is_company'] = 1
        resources = Contact().find_all(params)
        companies = []
        for res in resources:
            company = Company()
            company.load_from_resource(res)
            companies.append(company)

        return companies


class Person(Contact):
    def create(self, company_name, company_id, first_name, last_name, job, email, phone, role,
                     lpicid=None, verification_code=None):
        contact = redmine.Contact()
        contact.first_name = first_name
        contact.last_name = last_name
        contact.job_title = job
        contact.company = company_name
        contact.email = email
        contact.phone = phone
        contact.project_id = settings.REDMINE_PROJECT
        contact.is_company = False
        contact.custom_fields = [
            { 'value': role, 'id': self.mapping_id['Role']},
            { 'value': company_id, 'id': self.mapping_id['company_id']}
        ]

        if lpicid is not None:
            contact.custom_fields.append({'value': lpicid, 'id': self.mapping_id['LPICID']})
            contact.custom_fields.append({'value': verification_code, 
                                           'id': self.mapping_id['Verification']})

        contact.save()

        resource = Contact().find(contact.id)

        return self.load_from_resource(resource)


    def find(self, id):
        resource = Contact().find(id)
        return self.load_from_resource(resource)

    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['first_name'] = resource.first_name
        self['last_name'] = resource.last_name

        self['job_title'] = ''
        if resource.attributes.has_key('job_title'):
            self['job_title'] = resource.job_title

        self['background'] = ''
        if resource.attributes.has_key('background'):
            self['background'] = resource.background

        self['website'] = ''
        if resource.attributes.has_key('website'):
            self['website'] = resource.website

        self['phone'] = ''
        if resource.attributes.has_key('phones'):
            self['phone'] = resource.phones[0].number

        self['email'] = ''
        if resource.attributes.has_key('emails'):
            self['email'] = resource.emails[0].address

        self['street'] = ''
        self['postcode'] = ''
        self['city'] = ''
        self['country'] = ''
        if resource.attributes.has_key('address'):
            address = resource.attributes['address'].attributes

            self['city'] = address['city']
            self['postcode'] = address['postcode']
            self['street'] = address['street']
            self['country'] = address['country']

        for cf in resource.custom_fields:
            self[cf.name] = cf.value

        self['image_url'] = LPIAvatar().company_avatar_url(self['id'])

        return self

    def find_all(self, params):
        params['is_company'] = 0    
        resources = Contact().find_all(params)
        people = []
        for res in resources:
            person = Person()
            person.load_from_resource(res)
            people.append(person)

        return people


class Location(Contact):
    def create(self, company_name, company_id, first_name, address, city, postcode, country):
        contact = redmine.Contact()
        contact.first_name = first_name
        contact.address_attributes = {
            'street1': address,
            'city': city,
            'country_code': 'IT',
            'postcode': postcode
        }
        contact.company = company_name
        contact.project_id = settings.REDMINE_PROJECT
        contact.is_company = False
        contact.custom_fields = [
            { 'value': "Location", 'id': self.mapping_id['Role']},
            { 'value': company_id, 'id': self.mapping_id['company_id']}
        ]

        contact.save()
        
        return self.load_from_resource(contact)

    def find(self, id):
        resource = Contact().find(id)
        return self.load_from_resource(resource)

    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['first_name'] = resource.first_name

        self['street'] = ''
        self['postcode'] = ''
        self['city'] = ''
        self['country'] = ''
        if resource.attributes.has_key('address'):
            address = resource.attributes['address'].attributes

            self['city'] = address['city']
            self['postcode'] = address['postcode']
            self['street'] = address['street']
            self['country'] = address['country']


        for cf in resource.custom_fields:
            self[cf.name] = cf.value

        return self

    def find_all(self, params):
        params['is_company'] = 0    
        resources = Contact().find_all(params)
        locations = []
        for res in resources:
            location = Location()
            location.load_from_resource(res)
            locations.append(location)

        return locations



class Reference(Model):
    pass




