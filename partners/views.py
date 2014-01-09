from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from models import *
import json


def index(request):
    return render_to_response('index.html', {}, 
            context_instance=RequestContext(request))

def load_products(request):
    return renderJSON(Product().load_from_family(request.GET['family']))

def search(request):
    return renderJSON(Company().find_all(request.GET))

def register_contact(request):
    person = Person().create(request.GET)
    company = Company().create(request.GET)

    company['owner'] = person

    url = Product().hostedURL(request.GET['handle'])

    url += '?first_name=' + person['name']
    url += '&last_name=' + person['lastname']

    data = {
      'company': company,
      'url': url
    }

    return renderJSON(data)

def login(request):
    user = User()

def register(request):
    user = User()
    ret = { 'error': 0, 'data': {} }
    if not user.exists(request.GET['mail']):
        saved = user.register(request.GET['mail'], request.GET['password'])        
        if saved:
            ret['data'] = {'login': user.mail, 'id': user.id}
        else:
            ret['error'] = 2  # error registering
            ret['data'] = 'Error registering user.'
    else:
        ret['error'] = 1 # alreay exists
        ret['data'] = 'User alreay exists.'
    
    return renderJSON(ret)


def renderJSON(data):
    return HttpResponse(json.dumps(data, separators=(',', ':')), 
                                         content_type="application/json")

