from django import forms
from .models import Profile, File, LANGUAGE_CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, profile_photo='path/to/default.png')
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'photo', 'location']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['pdf_file']



class LanguageSelectionForm(forms.Form):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(LanguageSelectionForm, self).__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'form-control'})