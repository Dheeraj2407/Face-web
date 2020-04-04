from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login
from faceapp.forms import SignUpForm

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
            # Login the user and redirect to home page
            login(request, new_user)
            return redirect('faceapp:index')
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def index(request):
    return render(request, 'registration/index.html')


def test(request):
    return render(request, 'registration/test.html')
