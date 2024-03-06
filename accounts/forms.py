from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from .models import User
from django.forms import ClearableFileInput
from django.contrib import messages


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type":"text",
        "name":"email",
        "id":"email",
        "autocomplete":"off",
    }), label="Email")

    username = forms.CharField(widget=forms.TextInput(attrs={
        "type":"text",
        "name":"username",
        "id":"username",
        "autocomplete":"off",
    }), label="Username")

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "type":"password",
        "name":"password1",
        "id":"password1",
        "autocomplete":"off",
    }), label="Password")

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "type":"password",
        "name":"password2",
        "id":"password2",
        "autocomplete":"off",
    }), label="Password")

    class Meta:
        model = User
        fields = ['email','username','password1','password2']



# class ContactForm(forms.Form):
#     address = AddressField()
#     phone =  PhoneNumberField(
#         region="IN",
#     )

#     class META:
#         fields = ['address','phone']
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactAddress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                print('error')
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.state.district_set.order_by('name')

class ProfilePictureForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type":"text",
        "name":"username",
        "id":"username",
        "autocomplete":"off",
        "class": "form-control"
    }), label="Username")
    
    class Meta:
        model = User
        fields = ['username','profile']

        widgets = {
            'profile': ClearableFileInput(attrs={'class': 'form-control-file'})
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        user_with_username = User.objects.filter(username=username).exclude(id=self.instance.id)

        if user_with_username.exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.", code='username_taken')

        return username 
