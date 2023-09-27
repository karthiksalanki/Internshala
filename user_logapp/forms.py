from django import forms
from .models import *

class Login(forms.Form):
  User_Name = forms.CharField(max_length=200)
  Password = forms.CharField(max_length=200)
  
  
#from django import forms

class ResetPasswordRequestForm(forms.Form):
  email = forms.EmailField()
    
class JobApplications(forms.ModelForm):
  
  class Meta:
    model = Jobs
    fields = '__all__'
  
