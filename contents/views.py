from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from . models import VideoContent, UserReact, VideoHistory
from channelanalytics.models import Channel

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
            

            '''
            The played video is added to the user's watch history if that video does not already exist
            '''
            get_user_history_obj, create = VideoHistory.objects.get_or_create(user=user)
            if get_user_history_obj.video.filter(pk=kwargs['object'].pk).exists() == False:
                # print('This Video is not Found in your watch History.')
                get_user_history_obj.video.add(kwargs['object'])
        
        context['videos'] = VideoContent.objects.exclude(pk=self.kwargs['pk']).order_by('-uploaded')
        return context


class ChannelSubscribeOrUnsubscribe(LoginRequiredMixin, View):

    login_url = 'signin'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        channel = Channel.objects.get(slug=kwargs['slug'])

        if channel.subscriber.filter(email=user).exists() == False:
            # print('Not Exis.Now Add')
            channel.subscriber.add(user)
            return JsonResponse({'message': 'subscribed'})
        else:
            # print('Exis.Now Remove')
            channel.subscriber.remove(user)
        return JsonResponse({'message': 'unsubscribed'})        



class VideoLikeOrRemoveLike(LoginRequiredMixin, View):

    login_url = 'signin'

    def get(self, request, *args, **kwargs):
        
        user = request.user
        videoID = request.GET['video_id']
        
        vcontent = VideoContent.objects.get(pk=videoID)
        # print(user, videoID, vcontent)
        try:
            userReact = UserReact.objects.get(user__email=user, react='LI')
        except UserReact.DoesNotExist:
            userReact = UserReact.objects.create(user=user, react='LI')
        if userReact.content.filter(pk=vcontent.pk).exists() == True:
            # print('Exists.')
            userReact.content.remove(vcontent)
            return JsonResponse({'message': 'like-removed'}, safe=True)
        else:
            # print('Not Exists.')
            userReact.content.add(vcontent)
        
        return JsonResponse({'message': 'like-added'}, safe=True)



class UserVideoHistory(LoginRequiredMixin, View):

    login_url = 'signin'
    template_name = 'contents/history.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        watchvideouser = VideoHistory.objects.filter(user=user)

        if watchvideouser:
            watchvideos = watchvideouser[0].video.all()[::-1]
            context = {'videohistory': watchvideos}
        else:
            context = {}
        return render(request, self.template_name, context)



class RemoveUserVideoHistory(LoginRequiredMixin, View):

    login_url = 'signin'

    def get(self, request, *args, **kwargs):
        user = request.user
        watchvideouser = VideoHistory.objects.filter(user=user).first()

        if watchvideouser:
            watchvideouser.delete()
        return HttpResponseRedirect(reverse('user-video-history'))
