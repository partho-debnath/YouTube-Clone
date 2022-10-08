from django.shortcuts import render
from django.views.generic import ListView

from . models import VideoContent

# Create your views here.

class VideoContents(ListView):

    template_name = 'contents/index.html'
    model = VideoContent
    context_object_name = 'videos'
    ordering = '-uploaded'
