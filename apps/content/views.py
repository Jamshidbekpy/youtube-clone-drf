from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView)
from .models import Category
from .serializers import CategorySerializer,CategoryRetrieveSerializer
# Create your views here.

# Category

class CategoryListAPIView(ListAPIView):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryRetrieveAPIView(RetrieveAPIView):
    permission_classes = []
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryRetrieveSerializer

# Video

from .serializers import (
    VideoSerializer,
    VideoCreateSerializer,
    VideoUpdateSerializer,
    VideoRetrieveSerializer
    )
from .models import Video
class VideoListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_active=True)

from rest_framework.permissions import IsAuthenticated
from .permissions import HasChannel,IsOwner
from .models import View
class VideoCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated,HasChannel]
    serializer_class = VideoCreateSerializer
    def perform_create(self, serializer):
        serializer.save(channel=self.request.user.channel)
class VideoRetrieveAPIView(RetrieveAPIView):
    permission_classes = []
    serializer_class = VideoRetrieveSerializer
    queryset = Video.objects.filter(is_active=True)
    
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            view = View.objects.filter(video_id=kwargs['pk'],user_id=request.user.id).first()
            if not view:
                View.objects.create(video_id=kwargs['pk'],user_id=request.user.id)
        response = super().retrieve(request, *args, **kwargs)
        return response
    
class VideoUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated,HasChannel,IsOwner]
    serializer_class = VideoUpdateSerializer
    queryset = Video.objects.filter(is_active=True)

from django.shortcuts import get_object_or_404
class VideoDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated,HasChannel,IsOwner]
    queryset = Video.objects.all()
    
    # def destroy(self, request, *args, **kwargs):
    #     video = get_object_or_404(Video, pk=kwargs['pk'])
    #     video.delete()
    #     return Response({"message": "Video deleted successfully."},status=status.HTTP_204_NO_CONTENT)


# Like

from .models import Like,CommentLike
from .serializers import LikeVideoSerializer
            
class LikeVideoAPIView(APIView):
    def post(self, request, pk):
        user = request.user
        like = Like.objects.filter(user_id=user.id, video_id=pk).first()
        serializer = LikeVideoSerializer(data=request.data)
        if serializer.is_valid():
            if like:
                if like.like != serializer.validated_data.get('like'):
                    like.like = serializer.validated_data.get('like')
                    like.save()
                    return Response({"message": "Like updated successfully."},status=status.HTTP_200_OK)
                like.delete()
                return Response({"message": "Like deleted successfully."},status=status.HTTP_204_NO_CONTENT)
            like = Like.objects.create(user_id=user.id, video_id=pk, like=serializer.validated_data.get('like'))
            return Response({"message": "Like created successfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
from .models import Comment
from .serializers import CommentLikeSerializer
class LikeCommentAPIView(APIView):
    def post(self, request, pk):
        user = request.user
        like = CommentLike.objects.filter(user_id=user.id, comment_id=pk).first()
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            if like:
                if like.like != serializer.validated_data.get('like'):
                    like.like = serializer.validated_data.get('like')
                    like.save()
                    return Response({"message": "Like updated successfully."},status=status.HTTP_200_OK)
                like.delete()
                return Response({"message": "Like deleted successfully."},status=status.HTTP_204_NO_CONTENT)
            like = CommentLike.objects.create(user_id=user.id, comment_id=pk, like=serializer.validated_data.get('like'))
            return Response({"message": "Like created successfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LikedVideosListAPIView(ListAPIView):
    serializer_class = VideoSerializer
    def get_queryset(self):
        user = self.request.user
        return Video.objects.filter(likes__user_id=user.id,likes__like=True)


# Playlist

from .serializers import (
    PlaylistListSerializer,
    PlaylistCreateSerializer,
    PlaylistRetrieveSerializer,
    PlaylistUpdateSerializer,
    )

from .models import Playlist
class PlaylistListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated,HasChannel]
    serializer_class = PlaylistListSerializer
    def get_queryset(self):
        return Playlist.objects.filter(channel=self.request.user.channel,is_active=True)

class PlaylistCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated,HasChannel]
    serializer_class = PlaylistCreateSerializer
    def perform_create(self, serializer):
        serializer.save(channel=self.request.user.channel)

class PlaylistRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated,HasChannel,IsOwner]
    serializer_class = PlaylistRetrieveSerializer
    queryset = Playlist.objects.filter(is_active=True)

class PlaylistUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated,HasChannel,IsOwner]
    serializer_class = PlaylistUpdateSerializer
    queryset = Playlist.objects.filter(is_active=True)

class PlaylistDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated,HasChannel]
    def delete(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        if request.user.channel == playlist.channel:
            playlist.delete()
            return Response({"message": "Playlist deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete this playlist."},status=status.HTTP_403_FORBIDDEN)
    
class AddToPlaylistVideoAPIView(APIView): 
    permission_classes = [IsAuthenticated,HasChannel]   
    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        if request.user.channel == playlist.channel:
            if playlist.videos.filter(id=request.data.get('video')).exists():
                return Response({"message": "Video already added to playlist."},status=status.HTTP_400_BAD_REQUEST)
            video = get_object_or_404(Video, id=request.data.get('video'))
            playlist.videos.add(video)
            return Response({"message": "Video added to playlist successfully."},status=status.HTTP_201_CREATED)
        return Response({"message": "You don't have permission to add video to this playlist."},status=status.HTTP_403_FORBIDDEN)

class RemoveFromPlaylistVideoAPIView(APIView):
    permission_classes = [IsAuthenticated,HasChannel]
    def post(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        if request.user.channel == playlist.channel:
            if playlist.videos.filter(id=request.data.get('video')).exists():
                video = get_object_or_404(Video, id=request.data.get('video'))
                playlist.videos.remove(video)
                return Response({"message": "Video removed from playlist successfully."},status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "Video not found in playlist."},status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "You don't have permission to remove video from this playlist."},status=status.HTTP_403_FORBIDDEN)


# Comment

from .serializers import CommentSerializer,CommentCreateSerializer,CommentUpdateSerializer
class CommentParentListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(is_active=True,parent=None,video_id=self.kwargs['pk']).order_by('-created_at')  
    
class CommentReplyListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(is_active=True,parent_id=self.kwargs['pk']).order_by('-created_at')

class CommentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated,HasChannel]
    serializer_class = CommentCreateSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.channel)
from .permissions import IsOwner2
class CommentUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated,HasChannel,IsOwner2]
    serializer_class = CommentUpdateSerializer
    queryset = Comment.objects.filter(is_active=True)
    
class CommentDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated,HasChannel]
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        user = request.user.channel
        if comment.user == user or comment.video.channel == user:
            comment.delete()
            return Response({"message": "Comment deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete this comment."},status=status.HTTP_403_FORBIDDEN)


# ordering, search

class VideoOrderByTimeListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(is_active=True).order_by("-created_at")

from django.db.models import Count
class VideoOrderByViewsCountListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = VideoSerializer
    def get_queryset(self):
        return Video.objects.filter(is_active=True).annotate(
            view_count=Count('views')
        ).order_by('-view_count') 

class VideoSearchListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = VideoSerializer
    def get_queryset(self):
        query = self.request.query_params.get('query', '').strip()
        return Video.objects.filter(is_active=True,title__icontains=query).order_by('-created_at')
    

# class VideoSearchListAPIView(APIView):
#     permission_classes = []
#     def get(self, request):
#         query = request.query_params.get('query', '').strip()
#         videos = Video.objects.filter(is_active=True)
#         if query:
#             videos = videos.filter(title__icontains=query).order_by('-created_at')
#         serializer = VideoSerializer(videos, many=True)
#         return Response(serializer.data)





