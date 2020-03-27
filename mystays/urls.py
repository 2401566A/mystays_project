from django.urls import path
from mystays import views

app_name = 'mystays'

urlpatterns = [
    path('', views.home, name='home'),
    path('AboutUs/', views.about_us, name='about_us'),
    path('WhereToStay/', views.where_to_stay, name='where_to_stay'),
    path('ChosenStay/<slug:stay_name_slug>/', views.show_stay, name='show_stay'),
    path('WhereToStay/ChosenStay/<slug:stay_name_slug>/', views.show_stay, name='show_stay'),
]
