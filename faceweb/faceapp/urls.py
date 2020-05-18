"""Defines URL pattern for faceapp"""

from django.urls import path,include
from . import views

app_name = 'faceapp'

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Register page
    path('register/', views.register, name='register'),
    path('login/',include('django.contrib.auth.urls'),name='login'),
    path('test/',views.test,name='test'),
    path('contact/',views.contact,name='contact'),
]
