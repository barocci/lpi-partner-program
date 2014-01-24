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
        ret['data'] = {'login': user.username, 'id': user.id}
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
def profile(request):
    ret = {'error': 0, 'data:': ''}
    return renderJSON(ret)

@check_login
def register_contact(request):
    person = Person().create(request.GET)
    company = Company().create(request.GET)
    company['owner'] = person
    
    #STUB
    url = Product().hostedURL(request.GET['handle'])
    url += '?first_name=' + person['name']
    url += '&last_name=' + person['lastname']

    data = {
      'company': company,
      'url': url
    }

    return renderJSON(data)


def renderJSON(data):
    return HttpResponse(json.dumps(data, separators=(',', ':')), 
                                                                   content_type="application/json")



