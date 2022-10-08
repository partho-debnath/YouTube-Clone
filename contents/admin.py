from django.contrib import admin


from .models import PlayList, VideoContent, UserReact

# Register your models here.

@admin.register(PlayList)
class AdminPlayList(admin.ModelAdmin):
    
    model = PlayList
    list_display = ['channel', 'title', 'created']
    list_filter = ['title']
    search_fields = ['channel']
    list_editable = ['title']



@admin.register(VideoContent)
class AdminVideoContent(admin.ModelAdmin):

    model = VideoContent
    list_display = ['contenttitle', 'playlisttitle', 'uploaded', 'updated']
    list_filter =  ['contenttitle']
    search_fields = ['contenttitle']
    


class AdminUserReact(admin.ModelAdmin):
    
    model = UserReact
    list_display = ['user', 'react']
    list_filter = ['user', 'content', 'react']

admin.site.register(UserReact, AdminUserReact)
