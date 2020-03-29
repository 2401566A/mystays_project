from django.shortcuts import render
from django.http import HttpResponse
from mystays.models import Stay, Review
from mystays.forms import StayForm, ReviewForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

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


def sign_up(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            #doesn't save until the connection between the user and user profile is created
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'mystays/sign_up.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})        


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #checks if the username and password provided match an account
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                #login the user
                login(request, user)
                return redirect(reverse('mystays:home'))
            else:
                return HttpResponse("Your MyStays account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    #the form is accessed via GET, display the login form
    else:
        return render(request, 'mystays/login.html')
    

#helper function to recalculate the overall rating of a stay
def calcPropertyRating(stay, reviews):
    total = 0
    count = 0

    for r in reviews:
        total = total + r.impression
        count = count + 1

    average = total/count
    stay.propertyRating = average
    stay.save()








