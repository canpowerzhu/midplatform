from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def tasklist(request):
    if request.method == 'GET' or request.method == 'get':
        return  HttpResponse('this is get')

    if request.method == 'POST' or request.method == 'post':
        return HttpResponse('this is post')