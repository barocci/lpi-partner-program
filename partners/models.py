from django.db import models
from lib.chargify.chargify import Chargify
from lib.redmine import redmine
from django.conf import settings
from django.contrib.auth.models import User

class LPIUser(User):
    product = models.CharField(max_length=30)
    company = models.CharField(max_length=100)

    def register(self, username, password):
        user = LPIUser.objects.create_user(username, username, password)
        user.is_active = False
        #redmine_user = redmine.User()
        user.save()

        #saved = redmine_user.register(username, password)        
        return user

        return False


# Create your models here.
class Model(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

        self.chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
        self.mapping = {
          'Tipo': 'cf_14',
          'Incharge': 'cf_7',
        }

        self.mapping_id = {
          'Tipo': '14',
          'Incharge': '7',
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
    def create(self, email, first_name, last_name):
        customer = self.chargify.Customer()
        print dir(customer)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.save()
        print "saving customer %s" % customer.first_name
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
        print families
        print 'looking for ', handle
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


class Company(Model):
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
        return self.load_from_resource(contact)


    def load_from_resource(self, resource):
        self['name'] = resource.attributes['first_name']
        self['image_url'] = ''
        if resource.attributes.has_key('avatar'):
            avatar = Attachment.get(resource.attributes['avatar'].attributes['attachment_id'])
            self['image_url'] = avatar['content_url']

        contact = redmine.Contact.find(is_company=False,cf_7=1,company=self['name'])
        if contact:
            self['owner'] = Person()
            self['owner'].load_from_resource(contact[0])

        return self

    def find_all(self, params):
        params = self.encode_custom_fields(params)
        print params
        resources = redmine.Contact.find(is_company=1, **params)
        companies = []
        for res in resources:
          company = Company()
          company.load_from_resource(res)
          companies.append(company)

        return companies

class Person(Model):
    def create(self, company_name, first_name, last_name, role):
        contact = redmine.Contact()
        contact.first_name = first_name
        contact.last_name = last_name
        contact.job_title = role
        contact.company = company_name
        contact.project_id = settings.REDMINE_PROJECT
        contact.is_company = False
        contact.save()
        return self.load_from_resource(contact)

    def load_from_resource(self, resource):
        self['first_name'] = resource.attributes['first_name']
        self['last_name'] = resource.attributes['last_name']
        self['job_title'] = resource.attributes['job_title']
        return self


class Subscription(Model):
    pass

class Reference(Model):
    pass

