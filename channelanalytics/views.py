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
        context = {'form': form}
        return render(request, self.template_name, context)


class EditChannel(LoginRequiredMixin, View):

    login_url = 'signin'
    form_class = ChannelEditForm
    template_name ='channelanalytics/createOrEditChannel.html'

    def get(self, request, *args, **kwargs):

        form = ChannelEditForm(initial={'user':request.user.pk})
        context = {'form': form}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        
        print('=================', request.POST, '---', request.FILES)
        form = ChannelEditForm(request.POST)
    
        if form.is_valid():
            print(form.cleaned_data)
        #     # form.save()
        #     messages.success(request, 'Update Successfully.')
        else:
            print('error-----------------')
        #     print(form.errors)
        #     print(form.cleaned_data)
        context = {'form': form}
        return render(request, self.template_name, context)



class Channels(ListView):

    template_name = 'channelanalytics/channels.html'
    context_object_name = 'channels'
    # ordering = 'field name'

    def get_queryset(self, *args, **kwargs):
        return Channel.objects.all()
    


class ChannelDetails(DetailView):

    template_name ='channelanalytics/ChannelDetails.html'
    model = Channel
    context_object_name = 'channel'
