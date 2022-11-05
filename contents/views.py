from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
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

        '''
        Here, "kwargs" is just: {'object': <Activity: Activity 2>} but
        self.kwargs if dictonary of keyword agruments "<int: pk>" --> {'pk': 12}
        '''

        if self.request.user.is_authenticated == True:
            user = self.request.user
            video = VideoContent.objects.get(pk=self.kwargs['pk'])
            context['liked'] = UserReact.objects.filter(user=user.pk, content=video.pk, react='LI').exists()
        else:
            pass
        
        context['videos'] = VideoContent.objects.exclude(pk=self.kwargs['pk']).order_by('-uploaded')
        return context

     
class VideoLike(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        
        user = request.user
        videoID = request.GET['video_id']
        
        vcontent = VideoContent.objects.get(pk=videoID)
        print(user, videoID, vcontent)
        try:
            userReact = UserReact.objects.get(user__email=user, react='LI')
        except UserReact.DoesNotExist:
            userReact = UserReact.objects.create(user=user, react='LI')
        if userReact.content.filter(pk=vcontent.pk).exists() == True:
            print('Exists')
            userReact.content.remove(vcontent)
            return JsonResponse({'message': 'like-removed'}, safe=True)
        else:
            print('Not Exists')
            userReact.content.add(vcontent)
        
        return JsonResponse({'message': 'like-added'}, safe=True)

