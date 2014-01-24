from partners.lib.pyactiveresource.activeresource import ActiveResource
from django.conf import settings


class BaseResource(ActiveResource):
    _site = settings.REDMINE_URL
    _user = settings.REDMINE_USER
    _password = settings.REDMINE_PASS

class Contact(BaseResource):
    pass

class Issue(BaseResource):
    pass

class Deal(BaseResource):
    pass

class Attachment(BaseResource):
    pass

class Membership(BaseResource):
    _site = '%s/projects/%s' % (settings.REDMINE_URL, settings.REDMINE_PROJECT)

    def new_user(self, user_id):
        self.user_id = user_id
        self.role_ids = [8]
        self.save()
   

class User(BaseResource):
    def exists(self, mail):
        users = self.find()
        for user in users:
            if mail == user.attributes['login']:
                return True

        return False

    def register(self, mail, password):
        self.mail = mail
        self.login  = mail
        self.password  = password
        self.firstname  = 'web'
        self.lastname  = 'user'
        self.save()

        membership = Membership()
        membership.new_user(self.id)

        return True
