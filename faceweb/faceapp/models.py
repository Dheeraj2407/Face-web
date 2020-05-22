from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50,default='')
    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    classRoom = models.IntegerField()
    def __str__(self):
        """Return string representation of the model."""
        return str(self.classRoom)

class TeacherClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject)

class StudentClass(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

class AttendanceLogs(models.Model):
    student = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherClass, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class TimeTable(models.Model):
    ClassRoom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    day = models.CharField(max_length=50, default='')
    hour = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject)
