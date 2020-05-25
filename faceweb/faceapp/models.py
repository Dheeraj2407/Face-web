from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=50,default='',primary_key=True)
    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    classRoom = models.IntegerField(default=0, primary_key=True)
    def __str__(self):
        """Return string representation of the model."""
        return str(self.classRoom)

class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True, to_field='username', on_delete=models.CASCADE)

class TeacherClass(models.Model):
    user = models.ForeignKey(Teacher, on_delete=models.CASCADE, to_field='user')
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, to_field='classRoom')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, to_field='name')

class StudentClass(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='username', primary_key=True)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

class AttendanceLogs(models.Model):
    student = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherClass, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class TimeTable(models.Model):
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    day = models.CharField(max_length=50, default='')
    hour = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, default='')
    class Meta:
        unique_together = (('classRoom','day','hour'))
