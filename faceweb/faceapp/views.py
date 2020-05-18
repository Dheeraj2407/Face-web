from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login
from faceapp.forms import SignUpForm, UserUpdateForm
from django.contrib.auth.models import Group
import re
from django.contrib.auth.models import User
# Create your views here.


def register(request):
    '''Register a new user'''
    if request.user.is_authenticated:
        return redirect('faceapp:index')
    if request.method != "POST":
        # Display new registration form
        form = SignUpForm()
    else:
        # Process completed form
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            if re.search(r'\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}',username):
                group = Group.objects.get(name='Student')
            elif re.search(r'[A-Z]{2}\d{3}',username):
                group = Group.objects.get(name='Teacher')    
            new_user.groups.add(group)
            # Login the user and redirect to home page
            login(request, new_user)
            return redirect('faceapp:index')
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get_by_natural_key(request.user.username)
        if request.method!='POST':
            default_data = {'username':user.username, 'first_name':user.first_name,'last_name':user.last_name, 'email':user.email}
            form = UserUpdateForm(default_data, auto_id=False)
        else:
            form = UserUpdateForm(data=request.POST, instance=user)
            if form.is_valid():
                user = form.save()
        context = {'form':form}
        return render(request, 'registration/index.html',context=context)
    else:    
        return render(request, 'registration/index.html')

def test(request):
    return render(request, 'registration/test.html')

def contact(request):
    return render(request,'registration/contact.html')

def promo(request):
    return render(request,'registration/promo.html')