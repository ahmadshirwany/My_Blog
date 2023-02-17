from .models import comments
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class commentsform(forms.ModelForm):
    class Meta:
        model = comments
        exclude = ["post"]
        labels = {
            "username": "Your Name",
            "user_email": "Your Email",
            "comment_text": "Your Comment",
        }


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
