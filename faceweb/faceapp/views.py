from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login
from faceapp.forms import *
from django.contrib.auth.models import Group
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import TeacherClass, Subject, ClassRoom
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
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
                t = Teacher(user=new_user)    
                t.save()
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
        group = user.groups.all()[0].name
        default_data = {'username':user.username, 'first_name':user.first_name,'last_name':user.last_name, 'email':user.email}
        form = UserUpdateForm(default_data, auto_id=False)
        passwordForm = PasswordChangeForm(user=user)
        addSubjectsForm = AddSubjectForm()
        addClassRoomsForm = AddClassRoomsForm()
        engageClassesForm = EngageClassesForm()

        if request.method == "POST":
            data = request.POST
            if data.get('first_name'):
                form = UserUpdateForm(data=request.POST, instance=user)
                if form.is_valid():
                    user = form.save()
            elif data.get('old_password'):
                passwordForm = PasswordChangeForm(user=user,data=request.POST)
                if passwordForm.is_valid():
                    user = passwordForm.save()

            elif data.get('engageClass'):
                engageClassesForm = EngageClassesForm(data=data)
                if engageClassesForm.is_valid():
                    classRoom = ClassRoom.objects.get(pk=engageClassesForm.cleaned_data['classRoom'])
                    subject = Subject.objects.get(pk=engageClassesForm.cleaned_data['subject'])
                    teacher = Teacher.objects.get(pk=user.username)
                    teacherClass = TeacherClass(classRoom=classRoom, subject=subject, user=teacher)
                    teacherClass.save()
                

            elif data.get('addClass'):
                addClassRoomsForm = AddClassRoomsForm(data=request.POST)
                if addClassRoomsForm.is_valid():
                    addClassRoomsForm.save()

            elif data.get('addSubject'):
                addSubjectForm = AddSubjectForm(data=request.POST)
                if addSubjectForm.is_valid():
                    addSubjectForm.save()

        context = {'form':form,'passwordForm':passwordForm,'group':group, 'addSubjectsForm':addSubjectsForm, 'addClassRoomsForm':addClassRoomsForm, 'engageClassesForm':engageClassesForm}
        if group == 'Teacher':
            context['distinctClasses'] = TeacherClass.objects.filter(user = user.username).values('classRoom').distinct()
            context['classes'] = TeacherClass.objects.filter(user = user.username)
            context['classRooms'] = ClassRoom.objects.all()
            context['subjects'] = Subject.objects.all()
        return render(request, 'registration/index.html',context=context)
    else:    
        return render(request, 'registration/index.html')

def test(request):
    return render(request, 'registration/test.html')

def contact(request):
    return render(request,'registration/contact.html')

def promo(request):
    return render(request,'registration/promo.html')
"""
@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def add_classes(request):
    pass
"""

@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def add_classRooms(request):
    form = AddClassRoomsForm(data=request.POST)
    if form.is_valid():
        form.save()
    next = request.POST.get('next')
    return redirect(next)
