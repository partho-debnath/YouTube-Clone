from django.shortcuts import render
from django.views.generic import ListView, DetailView

from . models import VideoContent

# Create your views here.

class VideoContents(ListView):

    template_name = 'contents/index.html'
    context_object_name = 'videos'
    ordering = '-uploaded'
    model = VideoContent

    # def get_queryset(self):
    #     return VideoContent.objects.all()


class SpecificVideoContent(DetailView):

    template_name = 'contents/'
    context_object_name = 'video'
    model = VideoContent

     
