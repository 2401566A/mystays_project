from django.contrib import admin
from django.urls import path
from django.urls import include
from mystays import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mystays/', include('mystays.urls')),
    path('admin/', admin.site.urls),
]
