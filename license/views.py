from django.shortcuts import render

from .models import Client
from license.models import License


# Create your views here.

def index(request):
    licenses = License.objects.all()
    
    return render (request, 'html/index.html', {'licenses':licenses})