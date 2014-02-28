from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
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
    ret = { 'error': 0, 'data': {} }
    if request.GET.has_key('type'):
        if request.GET['type'] == 'services':
            contacts = Company().search_services()
        elif request.GET['type'] == 'academic':
            contacts = Company().search_academies()
        elif request.GET['type'] == 'training':
            contacts = Company().search_trainers()
        else:
            contacts = []

        ret['data'] = contacts
        
    return renderJSON(ret)

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


@check_login
def subscribe(request):
    ret = {'error': 0, 'data:': ''}
    subscription = LPISubscription().link_deal(request.GET['id'],
                                               request.GET['ref'],
                                               request.GET['product'])

    return HttpResponseRedirect("/#account")

@check_login
def user_info(request):
    ret = {
      'username': request.user.username,
      'user_id': request.user.id
    }

    return renderJSON(ret)

@check_login
def profile(request):
    ret = {'error': 0, 'data': []}
    if request.GET.has_key('id'):
        contact = Contact().find_one({'id': request.GET['id']})
        if contact:
            ret['data'] = contact

    return renderJSON(ret);

@check_login
def edit_profile(request):
    ret = {'error': 0, 'data': []}

    profile = request.POST.copy()
    print profile

    if profile.has_key('id'):
        if profile['id'] == '':
            print "Creating contact"
            contact = Person().create(profile['company'], 
                                      profile['company_id'], 
                                      profile['first_name'], 
                                      profile['last_name'],
                                      profile['job_title'], 
                                      profile['Role'])

            profile['id'] = contact['id']

        print profile
        Contact().edit(profile)
        ret['data'] = profile
 
    return renderJSON(ret);

def details(request):
    ret = {'error': 0, 'data': []}
    if request.GET.has_key('id'):
        company = Company().find(request.GET['id'])
        commercial = company['Commercial']
        incharge = company['Incharge']

        del company['Incharge']
        del company['Commercial']
        ret['data'] = { 
          'company': company,
          'commercial': commercial,
          'incharge': incharge
        }
        
    return renderJSON(ret);


@check_login
def account_info(request):
    ret = {'error': 0, 'data': []}

    if request.GET['section'] == 'partnership':
        data = {'training':[], 'services':[], 'academic':[]}
        subscriptions = LPISubscription().find(cf_7=request.user.id)
        print subscriptions
        for sub in subscriptions:
            product = Product().get_by_handle(sub['product'])
            info = {}
            info['state'] = sub['state']  
            info['product'] = product
            info['id'] = sub['id']
            info['due_date'] = sub['due_date']
            info['product']['url'] = Product().hostedURL(product['id'], request.user.id)

            family = product.family()

            if family:
                data[family].append(info)

        ret['data'] = data
    
    if request.GET['section'] == 'profile' and request.GET.has_key('data'):
        subscriptions = LPISubscription().find(id=request.GET['data'])
        if len(subscriptions) > 0:
            subscription = subscriptions[0]
            company = Company().find(subscription['company'])
            commercial = company['Commercial']
            incharge = company['Incharge']


            del company['Incharge']
            del company['Commercial']
            ret['data'] = { 
              'company': company,
              'commercial': commercial,
              'incharge': incharge
            }

    if request.GET['section'] == 'account':
        user = LPIUser.objects.get(id=request.user.id)
        link = user.get_management_url()
        ret['data'] = {'url': link}
  
    return renderJSON(ret)

@check_login
def register_contact(request):
    ret = {'error': 1, 'data:': ''}

    try:
        company = Company().create(request.GET['company_name'], request.GET['company_sector'])

        person = Person().create(request.GET['company_name'],
                                 company['id'],
                                 request.GET['owner_firstname'],
                                 request.GET['owner_lastname'],
                                 request.GET['owner_role'],
                                 'Incharge')
        company['owner'] = person


        subscription = LPISubscription().create(product=request.GET['product'],
                                                user_id=request.user.id,
                                                company_id=company['id'])

            
        if person is not None and company is not None:
            ret['error'] = 0

    except Exception, e:
        ret['data'] = "Chargify error %s" % e
    
    return renderJSON(ret)

def register(request):
    ret = { 'error': 0, 'data': {} }
    try:
        user = LPIUser().register(request.GET['mail'], request.GET['password'])        
        user.save()

        if user:
            
            user = auth.authenticate(username=request.GET['mail'], 
                                             password=request.GET['password'])
            if user:
                auth.login(request, user)
                ret['data'] = {'login': user.username, 'id': user.id}
            else:
                ret['error'] = 2  # error registering
                ret['data'] = 'Error registering user.'
        else:
                ret['error'] = 2  # error registering
                ret['data'] = 'Error registering user.'
    except Exception, e:
        ret['error'] = 1
        ret['data'] = 'User --already exists. %s' % e

    return renderJSON(ret)


def renderJSON(data):
    return HttpResponse(json.dumps(data, separators=(',', ':')), 
                                         content_type="application/json")



