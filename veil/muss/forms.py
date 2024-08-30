from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture']

class UploadForm(forms.Form):
    pdf_file = forms.FileField()
