from django.core.management.base import BaseCommand, CommandError
from partners.models import *

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        companies = Company().find_all({})

        for company in companies:
            print "Parsing: %s" % company['first_name']
            locations = self.get_locations(company)
            teachers = self.get_teachers(company)

            references = self.get_references(company)
            deals = LPISubscription().find(contact_id=company['id'])

            if len(deals) > 0:
                deal = deals[0]

                index = self.create_index(company)
                index.contact_id = company['id']
                index.contact_name = company['first_name']
                index.tags = self.get_tags(company)
                index.cities = self.parse_locations(locations)
                index.handle = deal['product']
                index.family = self.parse_family(deal['product'])
                index.lpic_id = self.parse_lpicid(teachers)
                index.status = deal['state']
                index.references = len(references)
                index.teachers = len(teachers)
                index.locations = len(locations)

                index.save()

    def create_index(self, company):
        exists = LPIIndexes.objects.filter(contact_id=company['id'])
        ret = False

        if len(exists) > 0:
            ret = exists[0]
        else:
            ret = LPIIndexes()

        return ret

    def get_tags(self, company):
        tags = ''
        if company['tag_list'] is not None:
            tags = company['tag_list']

        return tags

    def get_locations(self, company):
        params = {
          'company': company['first_name'],
          'cf_1': 'Location'
        }

        return Location().find_all(params)

    def parse_locations(self, locations):
        ret = []
        for location in locations:
            if location['city'] not in ret:
                ret.append(location['city'])

        return ", ".join(ret)

    def get_teachers(self, company):
        return Person().find_all({'company':company['first_name'], 'cf_1': 'Teacher'})

    def get_references(self, company):
        return Person().find_all({'company':company['first_name'], 'cf_1': 'Reference'})

    def parse_family(self, product):
        family = ''
        split = product.split('-')
        if len(split) > 1:
            family = split[1]

        return family

    def parse_lpicid(self, teachers):
        lpic_id = ''
        # TOFIX
        return lpic_id

