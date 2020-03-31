"""Defines URL pattern for faceapp"""

from django.urls import path
from . import views

app_name = 'faceapp'

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Register page
    path('register/', views.register, name='register'),
]
