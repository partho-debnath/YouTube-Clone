from statistics import mode
from django import forms
from django.core.exceptions import ValidationError

from . models import Channel

class ChannelCreateForm(forms.ModelForm):

    name = forms.CharField(
        max_length=20, 
        min_length=5,
        widget=forms.TextInput(attrs={
            'class':'form-control', 'placeholder': 'Enter a New Channel Name'
            }
        )
    )

    class Meta:
        model = Channel
        fields = ['user', 'name']

        widgets = {
            'user': forms.HiddenInput(),
        }
        

    def clean(self, *args, **kwargs):
        '''
        clean method through non-field error messages, instead of field error

        super().clean(*args, **kwargs)
        super(ChannelCreateForm, self).clean(*args, **kwargs)
        
        here, these are identical

        '''

        data = super(ChannelCreateForm, self).clean(*args, **kwargs)
    
        channels = Channel.objects.all()
        if channels.filter(user=data['user']).exists() == True:
            raise ValidationError('You Already Have a Channel.')
        elif channels.filter(name=data['name']).exists() == True:
            raise ValidationError('This Channel Name Already Used. Try another Name.')
        return data

    # error_messages = {
    #         'name': {
    #             'required': 'Channel Name Is Requird.',
    #         },
    #         'user': {'unique': 'You Already Have a Channel.'}
    #     }

    # def clean_name(self):
    #     ''''
    #     clean_fieldName through field error_messages instead of non-field error_messages.
    #     '''
    #     name = self.cleaned_data['name']
    #     if Channel.objects.filter(name=name).exists() == True:
    #         raise forms.ValidationError('This Channel Name Already Used. Try another Name.')
    #     return name

class ChannelEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        for field in self.Meta.required:
            self.fields[field].required = True
    

    class Meta:
        model = Channel
        fields = ['user', 'maincontent', 'coverPicture', 'channelLogo', 'about']
        # exclude = ['user']
        required = ['maincontent', 'coverPicture', 'channelLogo', 'about']


        labels = {
            'maincontent': 'Main Content',
            'coverPicture': 'Cover Picture',
            'channelLogo': 'Channel Logo',
            'about': 'About',
        }
        
        widgets = {
            'about': forms.Textarea(attrs={'placeholder': 'About This Channel'}),
            'user': forms.HiddenInput(),
        }

        error_messages = {
            'coverPicture':{'required':'Cover Picture can not be Empty.'},
            'channelLogo':{'required':'Channel Logo can not be Empty.'},
            'about':{'required':'About can not be Empty.'},
        }
        
        # # help_texts = {
        # #     # 'author_name': 'Some useful help text.',
        # # }

    # def clean(self, *args, **kwargs):
    #     data = super().clean(*args, **kwargs)
    #     print('---------', data)
    #     Channel.objects.update(user=data['user'], 
    #         coverPicture=data['coverPicture'], channelLogo=data['channelLogo'], about=data['about'])
        

    #     return data
