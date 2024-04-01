from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse(bytes('LOGIN', 'utf-8'))
