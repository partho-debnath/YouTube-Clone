from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from .forms import ChannelCreateForm, ChannelEditForm

from .models import Channel


# Create your views here.


class CreateChannel(LoginRequiredMixin, View):
    login_url = 'signin'
    template_name ='channelanalytics/createOrEditChannel.html'

    def get(self, request, *args, **kwargs):
        
        form = ChannelCreateForm(initial={'user':request.user})
        context = {'form': form}
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):

        form = ChannelCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Channel Created Successfully.')
            return HttpResponseRedirect(reverse('update-channel', kwargs={'pk':request.POST['user']}))
        context = {'form': form}
        return render(request, self.template_name, context)


class EditChannel(LoginRequiredMixin, View):

    login_url = 'signin'
    template_name ='channelanalytics/createOrEditChannel.html'

    def get(self, request, *args, **kwargs):
        user_channel = Channel.objects.get(user=request.user)
        form = ChannelEditForm(instance=user_channel)
        context = {
            'form': form,
            'channel': user_channel
        }
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        user_channel = Channel.objects.get(user=request.POST.get('user'))
        form = ChannelEditForm(request.POST, request.FILES, instance=user_channel)
    
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Successfully.')
        
        return HttpResponseRedirect(reverse('update-channel', kwargs={}))



class Channels(ListView):

    template_name = 'channelanalytics/channels.html'
    context_object_name = 'channels'
    # ordering = 'field name'

    def get_queryset(self, *args, **kwargs):
        return Channel.objects.all()
    


class ChannelDetails(DetailView):

    template_name ='channelanalytics/ChannelDetails.html'
    model = Channel
    slug_field = 'slug'
    context_object_name = 'channel'
