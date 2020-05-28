from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
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
        days = ('Mon','Tue','Wed','Thu','Fri','Sat')
        hours = range(1,8)
        tab = '1'

        if request.method == "POST":
            data = request.POST
            tab = data.get('tab')
            if data.get('first_name'):
                form = UserUpdateForm(data=request.POST, instance=user)
                if form.is_valid():
                    user = form.save()
            elif data.get('old_password'):
                passwordForm = PasswordChangeForm(user=user,data=request.POST)
                if passwordForm.is_valid():
                    user = passwordForm.save()

            elif data.get('class_Room'):
                engageClassesForm = EngageClassesForm(data=data)
                if engageClassesForm.is_valid():
                    classRoom = ClassRoom.objects.get(pk=engageClassesForm.cleaned_data['class_Room'])
                    res = TeacherClass.objects.filter(classRoom=classRoom, user=Teacher.objects.get(pk=user))
                    if len(res)==0:
                        subject = Subject.objects.get(pk=engageClassesForm.cleaned_data['subject'])
                        teacher = Teacher.objects.get(pk=user.username)
                        teacherClass = TeacherClass(classRoom=classRoom, subject=subject, user=teacher)
                        teacherClass.save()
                    else:
                        engageClassesForm._errors['class_Room'] = ['You have already engaged for this class']
                

            elif data.get('classRoom'):
                addClassRoomsForm = AddClassRoomsForm(data=request.POST)
                if addClassRoomsForm.is_valid():
                    if data.get('addClass') == '1':
                        addClassRoomsForm.save()
                    elif data.get('addClass') == '0':
                        addSubjectsForm._errors['classRoom'] = '<ul class="errorlist"><li>ClassRoom does not exist</li></ul>'
                else:
                    if data.get('addClass') == '0':
                        res = ClassRoom.objects.filter(classRoom=data.get('classRoom'))
                        if len(res)>0:
                            res.delete()

            elif data.get('addSubject'):
                addSubjectsForm = AddSubjectForm(data=request.POST)
                print(addSubjectsForm.is_valid())
                if addSubjectsForm.is_valid():
                    if data.get('addSubject') == '1':
                        addSubjectsForm.save()
                    elif data.get('addSubject') == '0':
                        addSubjectsForm._errors['name'] = '<ul class="errorlist"><li>Subject does not exist</ul></li>'
                elif data.get('addSubject') == '0':
                        res = Subject.objects.filter(name=data.get('name'))
                        if len(res)>0:
                            res.delete()
                        
            

        context = {'form':form,'passwordForm':passwordForm,'group':group,'days':days, 'hours':hours, 'tab':tab}
        if group == 'Teacher':
            context['scheduleClassForm'] = ScheduleClassForm()
            context['addSubjectsForm'] = addSubjectsForm
            context['addClassRoomsForm'] = addClassRoomsForm
            context['engageClassesForm'] = engageClassesForm
            context['distinctClasses'] = TeacherClass.objects.filter(user = user.username).values('classRoom').distinct()
            context['classes'] = TeacherClass.objects.filter(user = user.username)
            context['classRooms'] = ClassRoom.objects.all()
            context['subjects'] = Subject.objects.all()
            if len(context['distinctClasses'])>0:
                context['timeTable'] = TimeTable.objects.filter(classRoom=context['distinctClasses'][0]['classRoom'])
            else:
                context['timeTable'] = ''
        return render(request, 'registration/index.html',context=context)

    else:    
        return render(request, 'registration/index.html')

def test(request):
    return render(request, 'registration/test.html')

def contact(request):
    return render(request,'registration/contact.html')

def promo(request):
    return render(request,'registration/promo.html')

@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def scheduleClass(request):
    response_data = {}
    data = request.POST
    day = data.get('day')
    hour = data.get('hour')
    classRoom = data.get('classRoom')
    user = request.user
    print("Got request")

    classRoom = ClassRoom.objects.get(pk=classRoom)
    teacher = Teacher.objects.get(pk=user.username)

    try: 
        timeTable = TimeTable(teacher=teacher, day=day, hour=hour, classRoom=classRoom)
        timeTable.save()
        print("DONE")
        response_data['success'] = "<font color='green'>Scheduled successfully</font>"
        response_data['code'] = 1
    except Exception as e:
        response_data['success'] = "<font color='red'>Scheduling failed</font>"
        response_data['code'] = 0
        print(e)
        return JsonResponse(response_data)

    return JsonResponse(response_data)

@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def unscheduleClass(request):
    response_data = {}
    data = request.POST
    day = data.get('day')
    hour = data.get('hour')
    classRoom = data.get('classRoom')
    user = request.user
    print("Got request")

    classRoom = ClassRoom.objects.get(pk=classRoom)
    teacher = Teacher.objects.get(pk=user.username)

    try: 
        t = TimeTable.objects.filter(teacher=teacher, day=day, hour=hour, classRoom=classRoom)
        print("DONE")
        if len(t)>0:
            response_data['success'] = "<font color='green'>Disengaged successfully</font>"
            response_data['code'] = 1
            t.delete()
        else:
            response_data['success'] = "<font color='red'>Disengaging failed</font>"
            response_data['code'] = 0
    except Exception as e:
        response_data['success'] = "<font color='red'>Disengaging failed</font>"
        response_data['code'] = 0
        print(e)
        return JsonResponse(response_data)

    return JsonResponse(response_data)

@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def fetchTimeTable(request):
    response_data = {}
    classRoom = request.POST.get('classRoom')
    user = Teacher.objects.get(pk=request.user)
    timetable = None
    try:
        timeTable = TimeTable.objects.filter(classRoom=classRoom)
        r_t = []
        for i in timeTable:
            r_t.append((i.day,i.hour,str(i.teacher)))
        response_data['code'] = 1
        response_data['data'] = r_t
        response_data['subject'] = TeacherClass.objects.filter(user=user, classRoom=classRoom).values('subject')[0]['subject']
    except Exception as e:
        print(e)
        response_data['code'] = 0
    
    return JsonResponse(response_data)
    
@require_POST
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == "Teacher")
def disengageClass(request):
    data = request.POST
    classRoom = ClassRoom.objects.get(pk=data.get('class_Room'))
    subject = Subject.objects.get(pk=data.get('subject'))
    user = Teacher.objects.get(user=request.user)
    try:
        res = TeacherClass.objects.filter(classRoom=classRoom, subject=subject, user=user)
        if len(res)>0:
            res.delete()
        res = TimeTable.objects.filter(classRoom=classRoom, teacher=user)
        if len(res)>0:
            res.delete()
    except:
        pass
    return redirect(data.get('next'))
