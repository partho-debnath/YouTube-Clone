import email
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import View
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


from .signals import *
from .models import User
from .forms import UserCreationForm

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
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        
        if form.is_valid() == True:
            user = authenticate(email=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            return HttpResponse(f'{request.user}')
        else:
            context = {'form': form}
        return render(request, self.template_name, context)


def signin(request):
    form = AuthenticationForm(request=request, data=request.POST)
    
    if form.is_valid() == True:
        user = authenticate(email=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
        return HttpResponse(f'{request.user}')
    else:
        context = {'form': form}
    return render(request, 'signin.html', context)


def accountActivation(request, *args, **kwargs):

    encoded_uid = kwargs['uid']
    token = kwargs['token']
    
    try:
        uid = force_str(urlsafe_base64_decode(encoded_uid))
        user = get_object_or_404(User, pk=uid)
        if PasswordResetTokenGenerator().check_token(user, token) == True:
            user.is_active = True
            user.save()
            messages.success(request, 'Your Account is Activated now You can Login your Account.')
            return render(request, 'user/signup.html')
        else:
            messages.warning(request, 'Token is not Valid.')
            return render(request, 'user/signup.html')

    except Exception as e:
        messages.warning(request, 'User not Found.')
        return render(request, 'user/signup.html')