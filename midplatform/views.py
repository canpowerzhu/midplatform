from django.shortcuts import render, HttpResponse
import requests
# Create your views here.

def login(request):
    return render(request,'login.html')

def home(request):
    return  render(request,'home.html')