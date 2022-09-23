from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .signals import *
from .helper import get_user
from .models import User
from .forms import (UserCreationForm, CustomAuthenticationForm, 
                CustomPasswordResetForm, CustomSetPasswordForm,
                CustomPasswordChangeForm,)

# Create your views here.


class Signup(View):
    template_name = 'user/signup.html'

    def get(self, request, *args, **kwargs):
        fm = UserCreationForm()
        context = {'form': fm}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        fm = UserCreationForm(request.POST)
        if fm.is_valid() == True:
            fm.save()
            messages.info(request, 'Please confirm your email address to complete the registration')
        context = {'form': fm}
        return render(request, self.template_name, context)


class Signin(View):

    template_name = 'user/signin.html'

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):

        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid() == True:
            user = authenticate(email=form.cleaned_data['username'], password=form.cleaned_data['password'])
        
            if user is not None:
                login(request, user)
            return HttpResponse(f'{request.user}')
        else:
            context = {'form': form}
            
        return render(request, self.template_name, context)


def accountActivation(request, *args, **kwargs):

    try:
        user = get_user(kwargs)
        if PasswordResetTokenGenerator().check_token(user, kwargs['token']) == True:
            user.is_active = True
            user.save()
            messages.success(request, 'Your Account is Activated now You can Login your Account.')
            return render(request, 'user/signup.html')
        else:
            messages.warning(request, 'This Link(Token) is not Valid or Expired.Try to Generate another Link.')
            return render(request, 'user/link_expired_or_not_valid.html')

    except Exception as e:
        messages.warning(request, 'User not Found.')
        return render(request, 'user/signup.html')

@login_required(login_url='signin')
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin'))


class PasswordReset(View):

    template_name = 'user/passwordReset.html'

    def get(self, request, *args, **kwargs):

        form = CustomPasswordResetForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid() == True:
            '''
            this save method is not save in data on databases. 
            ''' 
            messages.success(request, "We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.")
            form.save(request)
        context = {'form': form}
        return render(request, self.template_name, context)


class PasswordResetConfirm(View):

    template_name = 'user/password_reset_confirm.html'

    def get(self, request, *args, **kwargs):
        user = get_user(kwargs)

        if PasswordResetTokenGenerator().check_token(user, kwargs['token']) == True:
            form = CustomSetPasswordForm(user=user)
        else:
            messages.warning(request, 'This Link(Token) is not Valid or Expired.Try to Generate another Link.')
            return render(request, 'user/link_expired_or_not_valid.html')

        context = {'form': form}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        user = get_user(kwargs)

        if PasswordResetTokenGenerator().check_token(user, kwargs['token']) == True:
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid() == True:
                form.save()
                messages.success(request, 'Password Reset Successfully completed. You Can now Signin Your Account.')
        else:
            messages.warning(request, 'This Link(Token) is not Valid or Expired.Try to Generate another Link.')
            return render(request, 'user/link_expired_or_not_valid.html')

        context = {'form': form}
        return render(request, self.template_name, context)

        
class PasswordChange(LoginRequiredMixin, View):

    login_url = 'signin'
    template_name = 'user/changePassword.html'

    def get(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid() == True:
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password Change Successfully.')
        context = {'form': form}
        return render(request, self.template_name, context)