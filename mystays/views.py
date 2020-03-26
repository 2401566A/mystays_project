from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context_dict = {}

    response = render(request, 'mystays/home.html', context=context_dict)
    return response

def about_us(request):
    context_dict = {}

    response = render(request, 'mystays/about_us.html', context=context_dict)
    return response

def where_to_stay(request):
    context_dict = {}

    response = render(request, 'mystays/where_to_stay.html', context=context_dict)
    return response


