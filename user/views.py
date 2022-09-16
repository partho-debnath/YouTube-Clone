from django.shortcuts import render
from django.views import View

from .signals import *

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
        context = {'form': fm}
        return render(request, self.template_name, context)