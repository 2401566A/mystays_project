from django.urls import path
from mystays import views

app_name = 'mystays'

urlpatterns = [
    path('', views.home, name='home'),
    path('AboutUs/', views.about_us, name='about_us'),
    path('WhereToStay/', views.where_to_stay, name='where_to_stay'),
    path('WhereToStay/ChosenStay/<slug:stay_name_slug>/', views.show_stay, name='show_stay'),
    path('WhereToStay/ChosenStay/<slug:stay_name_slug>/RateAndReview/<username>', views.RateAndReview.as_view(), name='rate_and_review'),
    path('SignUp/', views.sign_up, name='sign_up'),
    path('Login/', views.user_login, name='user_login'),
    path('Login/MyAccount/<username>/', views.MyAccountView.as_view(), name='my_account'),
    path('Login/MyAccount/<username>/EditAccount/', views.EditAccountView.as_view(), name='edit_account'),
    path('Login/MyAccount/<username>/PostedStays/', views.PostedStaysView.as_view(), name='posted_stays'),
    path('Login/MyAccount/<username>/PostedStays/EditStay/<slug:stay_name_slug>/', views.EditStayView.as_view(), name='edit_stay'),    
    path('Login/MyAccount/<username>/PostStay/', views.PostStayView.as_view(), name='post_stay'),
    path('Login/MyAccount/<username>/MyReviews/', views.MyReviewsView.as_view(), name='my_reviews'),
    path('Logout/', views.user_logout, name='user_logout'),
]
