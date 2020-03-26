from django.urls import path
from mystays import views

app_name = 'mystays'

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('where_to_stay/', views.where_to_stay, name='where_to_stay'),
]
