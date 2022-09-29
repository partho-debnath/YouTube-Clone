from django import forms
from django.contrib.auth.forms import (AuthenticationForm, ReadOnlyPasswordHashField,
PasswordResetForm,  SetPasswordForm)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse



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
            'date_of_birth': 'Date of Birth',
            'city': 'City'
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


class CustomAuthenticationForm(AuthenticationForm):   # inherite the django builtin AuthenticationForm
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    # add class and placeholder
    username = forms.EmailField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            'class':'form-control',
             'placeholder':'Email'
            }
        )
    )
    # add class and placeholder
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'class':'form-control',
            'placeholder':'Password'
            }
        ),
    )
    # override the error_messages
    error_messages = { 
        "invalid_login": _(
            "Please Enter a Correct %(username)s and Password. Note that Both "
            "Fields may be Case-sensitive."
        ),
        "inactive": _("This Account is Inactive. Before Login please Active your Account."),
    }


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                "autocomplete": "email",
                'class':'form-control',
            }
        ),
    )

    '''
    Override the save method of PasswordResetForm
    '''
    def save(self, request=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """

        domain_override=request.META['HTTP_HOST']  # root url
        subject_template_name='user/password_reset_subject.txt'   # Email Subject
        email_template_name='user/password_reset_email.html'     # Email Link 
        from_email=settings.EMAIL_HOST_USER     # From email
        token_generator = PasswordResetTokenGenerator()
        html_email_template_name=None

        return super(CustomPasswordResetForm, self).save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            from_email= from_email,
            token_generator=token_generator,
            request=request,
            html_email_template_name=html_email_template_name
        )



    # def save(self, request=None):
    #     email = self.cleaned_data['email']
    #     instance = User.objects.get(email=email)
    #     encoded_uid = urlsafe_base64_encode(force_bytes(instance.id))
    #     token = PasswordResetTokenGenerator().make_token(instance)
    #     root_url = 'http://127.0.0.1:8000'
    #     root_url = ''
    #     url = root_url + reverse('confirm-password', kwargs={'uid':encoded_uid, 'token':token})

    #     send_mail(
    #         subject = 'Account Activation Link',
    #         message = f'Goto the link {url} and active your account',
    #         from_email = settings.EMAIL_HOST_USER,
    #         recipient_list = [instance.email,]
    #     )



class CustomSetPasswordForm(SetPasswordForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("New Password and Confirm Password didn’t Match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class':'form-control',
                'placeholder': 'New Password'
                }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'class':'form-control',
                'placeholder': 'New Confirm Password'
                }
        ),
    )


class CustomPasswordChangeForm(CustomSetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "Your old Password was Entered Incorrectly. Please Enter it Again."
        ),
        "password_mismatch": _("New Password and Confirm Password didn’t Match."),
    }

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
            "autofocus": True,
            'class':'form-control',
            'placeholder': 'Old Password'
            }
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password
