from django.db import models
from lib.chargify.chargify import Chargify
from lib.redmine import redmine
from django.conf import settings
from django.contrib.auth.models import User
import datetime

class LPIUser(User):
    company = models.CharField(max_length=100)

    def register(self, username, password):
        user = LPIUser.objects.create_user(username, username, password)
        user.is_active = False
        user.save()
        return user



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
          'visible':         'cf_10'
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
          'visible':         '10'

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

    def get_managment_info(self):
        customer = self.chargify.Customer()
        info = customer.getManagementInfo('4484267')
        return info

    def create(self, email, first_name, last_name):
        customer = self.chargify.Customer()
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.save()
        self.load_from_resource(customer)

        return self

    def load_from_resource(self, resource):
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
            self['company'] = Company().find(resource.contact.id)

        self['product'] = custom_fields[self.mapping['product']]
        self['user_id'] = custom_fields[self.mapping['user_id']]
        self['state'] = custom_fields[self.mapping['state']]

        return self

    def find(self, **params):
        results = []
        deals = redmine.Deal().find(**params)
        for deal in deals:
            subscription = self.load_from_resource(deal)
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
        return self
        #self['price'] = "%.2f" % int(resource.price_in_cents)/100


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
        return self.find(contact.id)

    def find(self, id):
        resource = Contact().find(id, include='contacts')
        return self.load_from_resource(resource)

    def load_from_resource(self, resource):
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

        self['image_url'] = ''

        if resource.attributes.has_key('avatar'):
            avatar = Attachment.get(resource.attributes['avatar'].attributes['attachment_id'])
            self['image_url'] = avatar['content_url']
        
        self['Incharge'] = False
        self['Commercial'] = False

        if resource.attributes.has_key('contacts'):
            for contact_resource in resource.attributes['contacts']:
                contact = Person().find(contact_resource.attributes['id'])
                self[contact['Role']] = contact

        return self

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
    def create(self, company_name, company_id, first_name, last_name, job, role):
        contact = redmine.Contact()
        contact.first_name = first_name
        contact.last_name = last_name
        contact.job_title = job
        contact.company = company_name
        contact.project_id = settings.REDMINE_PROJECT
        contact.is_company = False
        contact.custom_fields = [
            { 'value': role, 'id': self.mapping_id['Role']},
            { 'value': company_id, 'id': self.mapping_id['company_id']}
        ]
        print contact.custom_fields
        contact.save()
        
        return self.load_from_resource(contact)

    def find(self, id):
        resource = Contact().find(id)
        return self.load_from_resource(resource)

    def load_from_resource(self, resource):
        self['id'] = resource.id
        self['first_name'] = resource.first_name
        self['last_name'] = resource.last_name
        self['job_title'] = resource.job_title

        self['job_title'] = ''
        if resource.attributes.has_key('job_title'):
            self['job_title'] = resource.job_title

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

        self['image_url'] = ''
        if resource.attributes.has_key('avatar'):
            avatar = Attachment.get(resource.attributes['avatar'].attributes['attachment_id'])
            self['image_url'] = avatar['content_url']

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




class Reference(Model):
    pass

