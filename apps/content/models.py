from django.db import models
from django.utils.text import slugify
from apps.base.models import BaseModel

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Video(BaseModel):
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='video_photos/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='videos')
    channel = models.ForeignKey('accounts.Channel', on_delete=models.CASCADE,related_name='videos')
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        
class Playlist(BaseModel):
    videos = models.ManyToManyField(Video, related_name='playlists')
    name = models.CharField(max_length=200)
    description = models.TextField()
    channel = models.ForeignKey('accounts.Channel', on_delete=models.CASCADE,related_name='playlists')
    class Meta:
        ordering = ['name']
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

class Comment(BaseModel):
    text = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey('accounts.Channel', on_delete=models.CASCADE,related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='replies')
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        
class Like(BaseModel):
    like = models.BooleanField(default=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey('accounts.MyUser', on_delete=models.CASCADE,related_name='likes')
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        

        
class CommentLike(BaseModel):
    like = models.BooleanField(default=None)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comment_likes')
    user = models.ForeignKey('accounts.MyUser', on_delete=models.CASCADE,related_name='comment_likes')
    class Meta:
        verbose_name = 'CommentLike'
        verbose_name_plural = 'CommentLikes'
        
class View(BaseModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='views')
    user = models.ForeignKey('accounts.MyUser', on_delete=models.CASCADE,related_name='views')
    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'Views'