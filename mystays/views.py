from django.shortcuts import render
from django.http import HttpResponse
from mystays.models import Stay, Review

def home(request):
    context_dict = {}

    highest_rated = Stay.objects.order_by('-propertyRating')[:5]
    context_dict['best_stays'] = highest_rated                                         

    response = render(request, 'mystays/home.html', context=context_dict)
    return response

def about_us(request):
    context_dict = {}

    response = render(request, 'mystays/about_us.html', context=context_dict)
    return response

def where_to_stay(request):
    context_dict = {}

    stays = Stay.objects.all()
    context_dict['stays'] = stays

    response = render(request, 'mystays/where_to_stay.html', context=context_dict)
    return response

def show_stay(request, stay_name_slug):
    context_dict = {}

    try:
        stay = Stay.objects.get(slug=stay_name_slug)
        reviews = Review.objects.filter(stay=stay)

        context_dict['reviews'] = reviews
        context_dict['stay'] = stay
    except Stay.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['stay']= None

    response = render(request, 'mystays/stay.html', context=context_dict)
    return response
