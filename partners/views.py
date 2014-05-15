from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from forms import *
from models import *
import json
import os
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

    return render_to_response('index.html', {'user': request.user}, 
            context_instance=RequestContext(request))

def load_products(request):
    return renderJSON(Product().load_from_family(request.GET['family']))

def search(request):
    ret = { 'error': 0, 'data': {} }
    if request.GET.has_key('type'):
        if request.GET['type'] == 'services':
            contacts = LPIIndexes().search_services()
        elif request.GET['type'] == 'academic':
            contacts = LPIIndexes().search_academies()
        elif request.GET['type'] == 'training':
            contacts = LPIIndexes().search_trainers()
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
    redirect = '/#subscription_error'

    print "subscribing"

    form = SubscriptionForm(request.GET, request.FILES)

    if form.is_valid():
        subscription = LPISubscription().link_deal(form.cleaned_data['id'],
                                                   form.cleaned_data['ref'],
                                                   form.cleaned_data['product'])

        redirect = '/#payment_success'
    
    return HttpResponseRedirect(redirect)

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

    if profile.has_key('id'):
        if profile['id'] == '':
            print "Creating contact"
            if profile['Role'] == 'Location':
                contact = Location().create(profile['company'], 
                                            profile['company_id'], 
                                            profile['first_name'], 
                                            profile['street'],
                                            profile['city'], 
                                            profile['postcode'],
                                            profile['country'])

            else:
                contact = Person().create(profile['company'], 
                                          profile['company_id'], 
                                          profile['first_name'], 
                                          profile['last_name'],
                                          profile['job_title'], 
                                          profile['email'], 
                                          profile['phone'], 
                                          profile['Role'],'','')

            
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
        locations = company['Location']
        teacher = company['Teacher']
        references = company['Reference']
        products = company['products']


        del company['Incharge']
        del company['Commercial']
        del company['Location']
        del company['Teacher']
        del company['Reference']
        del company['products']

        print company
        ret['data'] = { 
            'company': company,
            'commercial': commercial,
            'incharge': incharge,
            'teachers': teacher,
            'locations': locations,
            'products': products,
            'references': references
        }
        
    return renderJSON(ret)


@csrf_exempt
def hook(request):
    ret = {'error': 0, 'data': []}

    print "called webhook"

    form = WebhookForm(request.POST)
    if request.POST.has_key('id'):
        print request.POST['id']

    if request.POST.has_key('event'):
        print request.POST['event']

    if form.is_valid():
       print form.cleaned_data

    return renderJSON(ret)

@check_login
def account_info(request):
    ret = {'error': 0, 'data': []}

    if request.GET['section'] == 'partnership':
        data = {'training':[], 'services':[], 'academic':[], 'teachers': []}
        subscriptions = LPISubscription().find(cf_7=request.user.id)
        print subscriptions
        for sub in subscriptions:
            product = Product().get_by_handle(sub['product'])
            sub['product'] = product
            sub['product']['url'] = Product().hostedURL(product['id'], request.user.id)

            family = product.family()

            if family:
                data[family].append(sub)

        ret['data'] = data
    
    if request.GET['section'] == 'profile' and request.GET.has_key('data'):
        subscriptions = LPISubscription().find(id=request.GET['data'])
        if len(subscriptions) > 0:
            subscription = subscriptions[0]
            company = Company().find(subscription['company'])
            commercial = company['Commercial']
            incharge = company['Incharge']
            locations = company['Location']
            teacher = company['Teacher']
            products = company['products']

            del company['Incharge']
            del company['Commercial']
            del company['Location']
            del company['Teacher']
            del company['Reference']
            del company['products']


            ret['data'] = { 
              'company': company,
              'commercial': commercial,
              'subscription': subscription,
              'incharge': incharge,
              'teachers': teacher,
              'locations': locations
            }

    if request.GET['section'] == 'billing':
        user = LPIUser.objects.get(id=request.user.id)
        link = user.get_management_url()
        ret['data'] = {'url': link}
  
    return renderJSON(ret)

@check_login
def avatar_upload(request):
    ret = {
        "name": "",
        "size": 0,
    }

    form = AvatarForm(request.POST, request.FILES)

    if form.is_valid():
        avatar = LPIAvatar.objects.filter(contact_id=form.cleaned_data['contact_id']).first()
        if not avatar:
            avatar = LPIAvatar(
                image = form.cleaned_data['avatar'],
                contact_id = form.cleaned_data['contact_id']
            )
        else:
            avatar.image = form.cleaned_data['avatar']

        avatar.save()

        ret['name'] = "%s" % form.cleaned_data['avatar']
        ret['size'] = 0
        ret['url'] = 'http://partner.lpi-italia.org/static/%s' % avatar.image
        ret['thumbnailUrl'] = 'http://partner.lpi-italia.org/static/%s' % avatar.image
    else:
        ret['error'] = 'file not allowed.'


    return renderJSON(ret)

@check_login
def change_password(request):
    ret = {'error': 1, 'data': ''}
    form = PasswordForm(request.POST)

    if form.is_valid():
        if request.user.check_password(form.cleaned_data['old_password']):
            print "setting password %s" % form.cleaned_data['new_password']
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            ret['error'] = 0
            ret['data'] = 'Password ok'
        else:
            ret['data'] = "La vecchia password non e' valida."
    else:
        ret['data'] = 'Errore nel cambio password.'

    return renderJSON(ret)  

@check_login
def attach_contact(request):
    ret = {'error': 1, 'data': ''}

    form = AttachSubscriptionForm(request.POST)

    if form.is_valid():
        subscription = LPISubscription().create(product=form.cleaned_data['product'],
                                                user_id=request.user.id,
                                                company_id=form.cleaned_data['company'])

        ret['error'] = 0
    else:
        ret['data'] = 'Not valid form.'

    return renderJSON(ret)



@check_login
def register_contact(request):
    ret = {'error': 1, 'data:': ''}

    if not Product().check_family("ct", request.GET['product']):
        company = Company().create(request.GET['company_name'], request.GET['company_sector'])

        person = Person().create(request.GET['company_name'],
                                 company['id'],
                                 request.GET['owner_firstname'],
                                 request.GET['owner_lastname'],
                                 request.GET['owner_role'],
                                 request.GET['owner_email'],
                                 request.GET['owner_phone'],
                                 'Incharge',
                                 '',
                                 '')

        company['owner'] = person
        subscription = LPISubscription().create(product=request.GET['product'],
                                                user_id=request.user.id,
                                                company_id=company['id'])
    else:
        person = Person().create('',
                                 '',
                                 request.GET['owner_firstname'],
                                 request.GET['owner_lastname'],
                                 request.GET['owner_role'],
                                 request.GET['owner_email'],
                                 request.GET['owner_phone'],
                                 'Teacher',
                                 request.GET['lpic_id'],
                                 request.GET['lpic_verification_code'])

        subscription = LPISubscription().create(product=request.GET['product'],
                                                user_id=request.user.id,
                                                company_id=person['id'])

    
    #if Product().check_family("aap", request.GET['product']):
    #    issues = Issue().create('')

    if person is not None:
        ret['error'] = 0

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
        ret['data'] = "L'indirizzo email risulta gi&agrave; registrato."

    return renderJSON(ret)

def template(request):
    return render_to_response('%s.html' % request.GET['id'], {}, 
            context_instance=RequestContext(request))

def renderJSON(data):
    return HttpResponse(json.dumps(data, separators=(',', ':')), 
                                         content_type="")
