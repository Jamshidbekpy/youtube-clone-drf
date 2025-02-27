from django.contrib import admin
from .models import Category,Video,Playlist,Comment,CommentLike,Like,View
# Register your models here.

admin.site.register(Category)
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','category','channel')

admin.site.register(Playlist)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Like)
admin.site.register(View)
    

