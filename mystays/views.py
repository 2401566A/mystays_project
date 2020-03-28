from django.shortcuts import render
from django.http import HttpResponse
from mystays.models import Stay, Review
from mystays.forms import StayForm, ReviewForm
from django.shortcuts import redirect
from django.urls import reverse

def home(request):
    context_dict = {}

    for s in Stay.objects.all():
        reviews = Review.objects.filter(stay=s)
        calcPropertyRating(s, reviews)

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
    for s in stays:
        reviews = Review.objects.filter(stay=s)
        calcPropertyRating(s, reviews)
    
    context_dict['stays'] = stays

    response = render(request, 'mystays/where_to_stay.html', context=context_dict)
    return response


def show_stay(request, stay_name_slug):
    context_dict = {}

    try:
        stay = Stay.objects.get(slug=stay_name_slug)
        reviews = Review.objects.filter(stay=stay)

        calcPropertyRating(stay, reviews)

        context_dict['reviews'] = reviews
        context_dict['stay'] = stay
    except Stay.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['stay']= None

    response = render(request, 'mystays/stay.html', context=context_dict)
    return response


def post_stay(request):
    form = StayForm()

    if request.method == 'POST':
        form = StayForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            #after submitting the stay, return to the homepage (change later)
            return redirect('/mystays/')
        else:
            print(form.errors)

    response = render(request, 'mystays/post_stay.html', {'form': form})
    return response

def rate_and_review(request, stay_name_slug):
    try:
        stay = Stay.objects.get(slug=stay_name_slug)
    except Stay.DoesNotExist:
        stay = None

    if stay is None:
        return redirect('/mystays/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if stay:
                review = form.save(commit=False)
                review.stay = stay
                review.save()

                return redirect(reverse('mystays:show_stay', kwargs={'stay_name_slug': stay_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'stay': stay}
    response = render(request, 'mystays/rate_and_review.html', context=context_dict)
    return response

def calcPropertyRating(stay, reviews):
    total = 0
    count = 0

    for r in reviews:
        total = total + r.impression
        count = count + 1

    average = total/count
    stay.propertyRating = average
    stay.save()







