from django.shortcuts import render
from django.http import HttpResponse
from mystays.models import Stay, Review
from mystays.forms import StayForm, ReviewForm, UserForm, UserProfileForm, UserProfile
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views import View

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


class PostStayView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        return (user, user_profile)

    @method_decorator(login_required)
    def get(self, request, username):
        form = StayForm()
        return render(request, 'mystays/post_stay.html', {'form':form})
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('mystays:home'))

        form = StayForm(request.POST, request.FILES)
        
        if form.is_valid():
            stay = form.save(commit=False)
            stay.postedBy = user_profile
            
            stay.save()
            
            return redirect('mystays:posted_stays', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'mystays/posted_stays.html', context_dict)


class RateAndReview(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        return (user, user_profile)

    @method_decorator(login_required)
    def get(self, request, stay_name_slug, username):
        try:
            stay = Stay.objects.get(slug=stay_name_slug)
        except Stay.DoesNotExist:
            stay = None

        if stay is None:
            return redirect('/mystays/')
        
        form = ReviewForm()
        return render(request, 'mystays/rate_and_review.html', {'form':form, 'stay':stay})

    @method_decorator(login_required)
    def post(self, request, stay_name_slug, username):
        try:
            stay = Stay.objects.get(slug=stay_name_slug)
        except Stay.DoesNotExist:
            stay = None

        if stay is None:
            return redirect('/mystays/')

        try:
            (user, user_profile) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('mystays:show_stay', kwargs={'stay_name_slug': stay_name_slug}))

        reviewer=user_profile
        form = ReviewForm(request.POST)

        if form.is_valid():
            if stay:
                review = form.save(commit=False)
                review.stay = stay
                review.reviewedBy = reviewer
                review.save()

                return redirect(reverse('mystays:show_stay', kwargs={'stay_name_slug': stay_name_slug}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form, 'stay': stay}
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


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('mystays:home'))
    

class MyAccountView(View):
    def get(self, request, username):
        context_dict = {}
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        
        context_dict['user_profile'] = user_profile
        context_dict['selected_user'] = user

        response = render(request, 'mystays/my_account.html', context_dict)
        return response


#view that allows users to change their account information
class EditAccountView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})

        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('mystays:home'))

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'mystays/edit_account.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('mystays:home'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('mystays:my_account', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'mystays/edit_account.html', context_dict)


class PostedStaysView(View):
    def get(self, request, username):
        context_dict = {}
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        posted_stays = Stay.objects.filter(postedBy=user_profile)
        
        context_dict['user_profile'] = user_profile
        context_dict['selected_user'] = user
        context_dict['posted_stays'] = posted_stays

        response = render(request, 'mystays/posted_stays.html', context_dict)
        return response


#view that allows the user to edit the details of the stays they have posted
class EditStayView(View):
    @method_decorator(login_required)
    def get(self, request, username, stay_name_slug):
        context_dict = {}
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        
        form = StayForm()
        stay = Stay.objects.get(slug=stay_name_slug)

        context_dict['form'] = form
        context_dict['stay'] = stay
        context_dict['user'] = user
        context_dict['user_profile'] = user_profile

        response = render(request, 'mystays/edit_stay.html', context_dict)
        return response

    @method_decorator(login_required)
    def post(self, request, username, stay_name_slug):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        stay = Stay.objects.get(slug=stay_name_slug)
        form = StayForm(request.POST, request.FILES, instance=stay)
        
        if form.is_valid():
            form.save(commit=True)

            #once the stay data has been changed, redirect back to their posted stays - the changes just made should be visible
            return redirect('mystays:posted_stays', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'mystays/edit_stay.html', context_dict)


#view that allows the user to see the reviews they've posted
class MyReviewsView(View):
    def get(self, request, username):
        context_dict = {}

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        my_reviews = Review.objects.filter(reviewedBy=user_profile)
        
        context_dict['user_profile'] = user_profile
        context_dict['selected_user'] = user
        context_dict['my_reviews'] = my_reviews      

        response = render(request, 'mystays/my_reviews.html', context_dict)
        return response


#helper function to recalculate the overall rating of a stay
def calcPropertyRating(stay, reviews):
    total = 0
    count = 0

    for r in reviews:
        total = total + r.impression
        count = count + 1

    if count != 0:
        average = total/count
        stay.propertyRating = average
    
    stay.save()
    
##### Search

def search(request, keyword):
    context_dict = {}
    s_keyword = get_object_or_404(keyword)
    s_keyword = s_keyword.lower()
    
    for s in Stay.objects.all():
        if s.keyword.lower().equals(s_keyword):
            context_dict['desired_stays'] = s
    
    response = render(request, 'mystays/search.html', context_dict)
    
