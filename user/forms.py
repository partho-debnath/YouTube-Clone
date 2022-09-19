from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""


    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserCreationForm, self).__init__(*args, **kwargs)
        
        # now required field set to True
        for field in self.Meta.required:
            self.fields[field].required = True
            
        # if specific field is not required
        # self.fields['desired_field_name'].required = False
    
    password1 = forms.CharField(label='Confirm Password', 
    widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label='Confirm Password', 
    widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'country', 'city', 'date_of_birth']
        # exclude = ['email']

        required = ['first_name', 'last_name', 'country', 'city']
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth'
        }
        
        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}),
            'country': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Country Name'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'City Name'}),
            'date_of_birth': forms.TextInput(attrs={'class':'form-control', 'placeholder': '(Date of Birth) YY/MM/DD'}),
        }

        error_messages = {

            'email':{'required':'Emain can not be Empty.'}
        }
        
        # help_texts = {
        #     # 'author_name': 'Some useful help text.',
        # }


    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name.isalpha() == False or last_name.isalpha() == False:
            raise forms.ValidationError('First & Last name must contain only alphabetic characters.')

        return self.cleaned_data

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">This Form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

