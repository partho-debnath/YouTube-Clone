from django.shortcuts import render, HttpResponse
from django.views import View

# Create your views here.


class CreateChannel(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('ok')