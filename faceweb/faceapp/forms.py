# Create your forms here

from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )
        labels = {'username': 'User ID'}

class UserUpdateForm(forms.ModelForm):   
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)      
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email',)
class AddSubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=50,required=True)
    class Meta:
        model = Subject
        fields = ('name',)
        labels = {'name':'Subject Name'}

class AddClassRoomsForm(forms.ModelForm):
    classRoom = forms.IntegerField(required=True)
    class Meta:
        model = ClassRoom
        fields = ('classRoom',)
        labels = {'classRoom':"Room Number"}

class EngageClassesForm(forms.Form):
    classRoom = forms.IntegerField(required=True)
    subject = forms.CharField(max_length=50, required=True)
    class Meta:
        fields = ('classRoom','subject')
    
    def is_valid(self):
        valid = super(EngageClassesForm,self).is_valid()
        if not valid:
            return valid
        try:
            ClassRoom.objects.get(pk=self.cleaned_data['classRoom'])
        except:
            #raise ValidationError('ClassRoom does not exist')
            self._errors['classRoom'] = ["ClassRoom does not exist"]
            return False
        
        try:
            Subject.objects.get(pk=self.cleaned_data['subject'])
        except:
            #raise ValidationError('Subject does not exist')
            self._errors['subject'] = ["Subject does not exist"]
            return False
        
        return True

dayChoices = (
    ('Mon','Mon'),
    ('Tue','Tue'),
    ('Wed','Wed'),
    ('Thu','Thu'),
    ('Fri','Fri'),
    ('Sat','Sat'),
)
class ScheduleClassForm(forms.Form):
    day = forms.CharField(label='', widget=forms.Select(choices=dayChoices))
    hour = forms.IntegerField(label='', initial=1, min_value=1, max_value=7)
    class Meta:
        fields = ('day')