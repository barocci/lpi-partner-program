from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import auth
from models import *
import json
from functools import wraps

def check_login(view):
      @wraps(view)
      def wrapper(request, *args, **kwargs):
            if(request.user.is_authenticated()):
                return view(request, *args, **kwargs)
            else:
                return redirect('#login')

      return wrapper


def index(request):
    return render_to_response('index.html', {}, 
            context_instance=RequestContext(request))

def load_products(request):
    return renderJSON(Product().load_from_family(request.GET['family']))

def search(request):
    return renderJSON(Company().find_all(request.GET))


def redirect(page):
    data = {'redirect': page}
    return renderJSON(data)

def login(request):
    ret = { 'error': 0, 'data': {} }
    user = auth.authenticate(username=request.GET['username'], 
                             password=request.GET['password'])
    if user:
        auth.login(request, user)
        ret['data'] = {'username': user.username, 'id': user.id}
    else:
        ret['error'] = 1

    return renderJSON(ret)

def logout(request):
    ret = {'error': 0, 'data:': ''}
    auth.logout(request)
    return renderJSON(ret)

def register(request):
    ret = { 'error': 0, 'data': {} }
    try:
        user = LPIUser().register(request.GET['mail'], request.GET['password'])        
        user.product = request.GET['product']
        user.save()
        if user:
            user = auth.authenticate(username=request.GET['mail'], 
                                             password=request.GET['password'])
            if user:
                auth.login(request, user)
                ret['data'] = {'login': user.username, 'id': user.id}
            else:
                ret['error'] = 2  # error registering
                ret['data'] = 'Error registering redmine_user.'
        else:
                ret['error'] = 2  # error registering
                ret['data'] = 'Error registering redmine_user.'
    except Exception, e:
        ret['error'] = 1
        ret['data'] = 'User already exists.'

    return renderJSON(ret)

@check_login
def user_info(request):
    ret = {
      'username': request.user.username,
      'user_id': request.user.id
    }

    return renderJSON(ret)

@check_login
def profile(request):
    ret = {'error': 0, 'data:': ''}
    return renderJSON(ret)

@check_login
def register_contact(request):
    ret = {'error': 1, 'data:': ''}
    print 'registering contact %s %s' %(request.GET['owner_firstname'], request.GET['owner_lastname'])
    print request.GET

#    try:
    person = Person().create(request.GET['company_name'],
                             request.GET['owner_firstname'],
                             request.GET['owner_lastname'],
                             request.GET['owner_role'])
    company = Company().create(request.GET['company_name'])
    company['owner'] = person
    print "email: %s" % request.user.email 
    print person
    customer = Customer().create(request.user.email, 
                               person['first_name'], 
                               person['last_name'])
        
    print "created customer %s" % customer['first_name']
    if person is not None and company is not None:
        ret['error'] = 0
#    except Exception, e:
#        print "Chargify error %s" % e
    
    return renderJSON(ret)


def renderJSON(data):
    return HttpResponse(json.dumps(data, separators=(',', ':')), 
                                         content_type="application/json")



