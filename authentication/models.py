from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

# class User(AbstractUser):
#     # Add any additional fields you need
#     bio = models.TextField(blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name


class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is an update
            try:
                old_file = ExcelFile.objects.get(pk=self.pk).file
            except ExcelFile.DoesNotExist:
                pass  # When new file is added
            else:
                if old_file and self.file and old_file != self.file:
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)
        super(ExcelFile, self).save(*args, **kwargs)

@receiver(pre_delete, sender=ExcelFile)
def delete_file_from_storage(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class UserRegistration(AbstractUser):
    CS = 'CS'
    EC = 'EC'
    EEE = 'EEE'
    MECH = 'MECH'

    SEMESTER_CHOICES = [(f's{i}', f'Semester {i}') for i in range(1, 9)]

    DEPARTMENT_CHOICES = [
        (CS, 'Computer Science'),
        (EC, 'Electronics and Communication'),
        (EEE, 'Electrical and Electronics'),
        (MECH, 'Mechanical'),
    ]

    department = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=100)
    cgpa = models.FloatField(null= True)
    year = models.IntegerField(null=True, blank=True, default=None)  # Add year field
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES, null=True, blank=True, default=None)  # Add semester field
    higher_secondary_score = models.CharField(max_length=100)
    sslc_score = models.CharField(max_length=100)
    mooc_course = models.CharField(max_length=100)
    internship_attended = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    groups = models.ManyToManyField('auth.Group', related_name='custom_users_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_users_permissions')