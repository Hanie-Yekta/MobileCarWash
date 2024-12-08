from django import forms
from .models import User, WorkerUser, CustomerUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

STATIC_WORKER_ID = 355

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match!')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class WorkerUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = WorkerUser
        fields = ('email', 'phone_number', 'workerID','first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match!')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class CustomerUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'gender')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match!')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\">this form</a>.')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'password', 'last_login')



class WorkerUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\">this form</a>.')

    class Meta:
        model = WorkerUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'workerID','first_name', 'last_name', 'password', 'last_login')


class CustomerUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password using <a href=\"../password/\">this form</a>.')

    class Meta:
        model = CustomerUser
        fields = ('email', 'phone_number', 'first_name', 'last_name','gender', 'password', 'last_login')



class UserRegistrationForm(forms.Form):
    GENDER = [
        ('F' , 'female'),
        ('M' , 'male'),
    ]

    email = forms.EmailField()
    first_name = forms.CharField(label='first name')
    last_name = forms.CharField(label='last name')
    phone = forms.CharField(max_length=11)
    gender = forms.ChoiceField(choices=GENDER)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email
    

    def clean_phone(self):
        phone=self.cleaned_data['phone']
        user=User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exists')
        return phone



    

