from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from .models import UserRegistration, ExcelFile

# Choices for the department field
DEPARTMENT_CHOICES = (
    ('sc','select choice'),
    ('cse', 'Computer science and Engineering'),
    ('ec', 'Electrical Engineering'),
    ('me', 'Mechanical Engineering'),
    ('ce','civil Engineering'),
)
mooccourse_CHOICES = (
    ('sc','select choice'),
    ('cse', 'Computer science and Engineering'),
    ('ec', 'Electrical Engineering'),
    ('me', 'Mechanical Engineering'),
    ('ce','civil Engineering'),
)


class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']

class UserRegistrationForm(UserCreationForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label='Department')
    mooc_course = forms.ChoiceField(choices=mooccourse_CHOICES, label='Mooc course')
    year = forms.IntegerField(required=False, label='Year')
    semester = forms.ChoiceField(choices=UserRegistration.SEMESTER_CHOICES, required=False, label='Semester')
    username = forms.CharField(
        max_length=150,
        help_text='',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text=''
    )
      
    class Meta:
        model = UserRegistration
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'department',
            'registration_number',
            'admission_number',
            'cgpa',
            'year',
            'semester',
            'higher_secondary_score',
            'sslc_score',
            'mooc_course',
            'internship_attended',
            'phone_number',
        ]

    # Custom validation for password
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        validate_password(password2)
        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
