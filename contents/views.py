from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse

from . models import VideoContent, UserReact

# Create your views here.

class VideoContents(ListView):

    template_name = 'contents/index.html'
    context_object_name = 'videos'
    ordering = '-uploaded'
    model = VideoContent

    # def get_queryset(self):
    #     return VideoContent.objects.all()


class SpecificVideoContent(DetailView):

    template_name = 'contents/playVideo.html'
    context_object_name = 'video_stream'
    model = VideoContent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated == True:
            pass
        else:
            pass

        '''
        Here, "kwargs" is just: {'object': <Activity: Activity 2>} but
        self.kwargs if dictonary of keyword agruments "<int: pk>" --> {'pk': 12}
        '''
        context['videos'] = VideoContent.objects.exclude(pk=self.kwargs['pk']).order_by('-uploaded')
        return context



     
class VideoLike(View):

    def get(self, request, *args, **kwargs):
        
        user = request.user
        videoID = request.GET['video_id']
        
        vcontent = VideoContent.objects.get(pk=videoID)
        print(user, videoID, vcontent)

        try:
            userReact = UserReact.objects.get(user__email=user, react='LI')
        except UserReact.DoesNotExist:
            userReact = UserReact.objects.create(user=user, react='LI')
        userReact.content.add(vcontent)

        return JsonResponse({'message': 'added'}, safe=True)
