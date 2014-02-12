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

class LPISubscription(models.Model):
    product = models.CharField(max_length=30)
    user = models.ForeignKey(LPIUser)
    company = models.CharField(max_length=100)
    active = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.today()
        return super(LPISubscription, self).save(*args, **kwargs)


# Create your models here.
class Model(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

        self.chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)

        self.mapping = {
          'Tipo':       'cf_14',
          'Incharge':   'cf_7',
          'Role':       'cf_1',
          'company_id': 'cf_2',
          'piva':       'cf_3'
        }

        self.mapping_id = {
          'Tipo':       '14',
          'Incharge':   '7',
          'Role':       '1',
          'company_id': '2',
          'piva': '3',
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
            if self['handle'].find(key):
                return family

        return False

    def get_by_handle(self, handle):
        resource = self.chargify.Product().getByHandle(handle)

        return self.load_from_resource(resource)

    def hostedURL(self, handle):
        resource = self.chargify.Product().getByHandle(handle)
        url = "%s%s/subscriptions/new" % (settings.CHARGIFY_HOSTED_PAGE, resource.id)

        return url

    def load_from_resource(self, resource):
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
        resources = redmine.Contact.find_all(**params)
        return resources
        

class Company(Contact):
    def create(self, company_name):
        contact = redmine.Contact()
        contact.is_company = True
        contact.first_name = company_name
        contact.visibility = 1
        contact.custom_fields = [
            { 'value': 0, 'id': self.mapping_id['Incharge']}
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


class Subscription(Model):
    pass

class Reference(Model):
    pass

