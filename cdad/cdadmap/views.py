from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

# import all cdadmap models
from cdadmap.models import *

# Create your views here.
def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('cdadmap/index.html', context_dict, context)
    