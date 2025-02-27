from rest_framework.serializers import ModelSerializer,SerializerMethodField,HiddenField,CurrentUserDefault
from .models import Category, Video

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class CategoryRetrieveSerializer(ModelSerializer):
    videos_list = SerializerMethodField()
    class Meta:
        model =Category 
        fields = ('name','videos_list')
        
    def get_videos_list(self, obj):
        videos = obj.videos.filter(is_active=True)
        return VideoSerializer(videos, many=True).data

class VideoSerializer(ModelSerializer):
    view_count = SerializerMethodField()
    class Meta:
        model = Video
        fields = ('video','title', 'photo','view_count','created_at')
        
    def get_view_count(self, obj):
        return obj.views.count()

class VideoCreateSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('video','title', 'description','photo','category') 


class VideoUpdateSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description','photo','category')
class VideoRetrieveSerializer(ModelSerializer):
    channel = SerializerMethodField()
    subscribed_count = SerializerMethodField()
    is_subscribed = SerializerMethodField() 
    is_liked = SerializerMethodField()
    is_disliked = SerializerMethodField()
    like_count = SerializerMethodField()
    dislike_count = SerializerMethodField()
    view_count = SerializerMethodField()
    class Meta:
        model = Video
        fields = ('title','description','like_count','dislike_count','view_count','subscribed_count','is_subscribed','channel','is_liked','is_disliked')
    def get_like_count(self, obj):
        return obj.likes.filter(like=True).count()  
     
    def get_dislike_count(self, obj):
        return obj.likes.filter(like=False).count()
    
    def get_view_count(self, obj):
        return obj.views.count()
    
    def get_subscribed_count(self, obj):
        channel = obj.channel
        return channel.subscribers.count()
    def get_is_subscribed(self, obj):
        channel = obj.channel
        user = self.context['request'].user
        return channel.subscribers.filter(id=user.id).exists()
    def get_channel(self, obj):
        return obj.channel.name
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user, like=True).exists()
        return False
    def get_is_disliked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user, like=False).exists()
        return False
    
from .models import Like

from rest_framework.serializers import BooleanField
class LikeVideoSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('like','video','user')
        read_only_fields = ('video','user')

from .models import Comment
class CommentSerializer(ModelSerializer):
    is_liked = SerializerMethodField()
    is_disliked = SerializerMethodField()
    like_count = SerializerMethodField()
    dislike_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('text','video','user','is_liked','is_disliked','like_count','dislike_count')
        read_only_fields = ('video','user')
        
    def get_like_count(self, obj):
        return obj.comment_likes.filter(like=True).count()  
     
    def get_dislike_count(self, obj):
        return obj.comment_likes.filter(like=False).count()
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.comment_likes.filter(user=user, like=True).exists()
        return False
    def get_is_disliked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.comment_likes.filter(user=user, like=False).exists()
        return False
    
        

from .models import CommentLike
class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('like','comment','user')
        read_only_fields = ('comment','user')
        
        
class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text','video','parent')
        
class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)
        
from .models import Playlist   
class PlaylistListSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name',)

class PlaylistCreateSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name','description')
        
class PlaylistUpdateSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name','description')
        
class PlaylistRetrieveSerializer(ModelSerializer):
    videos_list = SerializerMethodField()
    class Meta:
        model =Playlist 
        fields = ('name','description','videos_list','created_at','updated_at')
        
    def get_videos_list(self, obj):
        videos = obj.videos.filter(is_active=True)
        return VideoSerializer(videos, many=True).data
    
    
        
        
        
        
        

        


        