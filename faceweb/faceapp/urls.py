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
    path('promo/',views.promo,name='promo'),
    path('add_classes/',views.add_classes,name='add_classes'),
    path('add_subjects/',views.add_subjects,name='add_subjects'),
    path('add_classRooms/',views.add_classRooms,name='add_classRooms'),
]
