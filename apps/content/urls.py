from django.urls import path


# Category

from .views import CategoryListAPIView,CategoryRetrieveAPIView
urlpatterns = [
    path('api/category/list/', CategoryListAPIView.as_view(), name='category_list'),
    path('api/category/retrieve/<int:pk>',CategoryRetrieveAPIView.as_view(),name='category_retrieve'),
]


# Video

from .views import (
    VideoListAPIView,
    VideoRetrieveAPIView,
    VideoCreateAPIView,
    VideoUpdateAPIView,
    VideoDestroyAPIView,
    )
urlpatterns += [
    path('api/video/list/', VideoListAPIView.as_view(), name='video_list'),
    path('api/video/create/', VideoCreateAPIView.as_view(), name='video_create'),
    path('api/video/retrieve/<int:pk>/', VideoRetrieveAPIView.as_view(), name='video_retrieve'),
    path('api/video/update/<int:pk>/', VideoUpdateAPIView.as_view(), name='video_update'),
    path('api/video/delete/<int:pk>/', VideoDestroyAPIView.as_view(), name='video_delete'),  
]


#Like

from .views import (
    LikeVideoAPIView,
    LikedVideosListAPIView,
    LikeCommentAPIView,
)
urlpatterns += [
    path('api/like/video/<int:pk>/',LikeVideoAPIView.as_view(),name='like_video'),
    path('api/liked-videos/',LikedVideosListAPIView.as_view(),name='liked_videos'),
    path('api/like/comment/<int:pk>/',LikeCommentAPIView.as_view(),name='like_comment'),
]


# Comment

from .views import (
    CommentParentListAPIView,
    CommentReplyListAPIView,
    CommentCreateAPIView,
    CommentUpdateAPIView,
    CommentDestroyAPIView
    )
urlpatterns += [
    path('api/comment/list/<int:pk>', CommentParentListAPIView.as_view(), name='comment_list'),
    path('api/comment/replies/<int:pk>/', CommentReplyListAPIView.as_view(), name='comment_replies'),
    path('api/comment/create/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('api/comment/update/<int:pk>/', CommentUpdateAPIView.as_view(), name='comment_update'),
    path('api/comment/delete/<int:pk>/', CommentDestroyAPIView.as_view(), name='comment_delete'),
]


# Playlist

from .views import (
    PlaylistListAPIView,
    PlaylistCreateAPIView,
    PlaylistRetrieveAPIView,
    PlaylistUpdateAPIView,
    PlaylistDestroyAPIView,
    AddToPlaylistVideoAPIView,
    RemoveFromPlaylistVideoAPIView
    
)
urlpatterns += [
    path('api/playlist/list/', PlaylistListAPIView.as_view(), name='playlist_list'),
    path('api/playlist/create/', PlaylistCreateAPIView.as_view(), name='playlist_create'),
    path('api/playlist/retrieve/<int:pk>/', PlaylistRetrieveAPIView.as_view(), name='playlist_retrieve'),
    path('api/playlist/update/<int:pk>/', PlaylistUpdateAPIView.as_view(), name='playlist_update'),
    path('api/playlist/delete/<int:pk>/', PlaylistDestroyAPIView.as_view(), name='playlist_delete'),
    path('api/playlist/add/<int:pk>/', AddToPlaylistVideoAPIView.as_view(), name='add_to_playlist'),
    path('api/playlist/remove/<int:pk>/', RemoveFromPlaylistVideoAPIView.as_view(), name='remove_from_playlist'),
]


#ordering and search

from .views import VideoOrderByTimeListAPIView,VideoOrderByViewsCountListAPIView,VideoSearchListAPIView
urlpatterns += [
    path('api/video/orderby/time/list',VideoOrderByTimeListAPIView.as_view(),name='orderby_time'),
    path('api/video/orderby/viewscount/list',VideoOrderByViewsCountListAPIView.as_view(),name='orderby_views'),
    path('api/video/search/list',VideoSearchListAPIView.as_view(),name='search_videos')
]


# Documentation

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="YouTube API",
        default_version='v1',
        description="API lar",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jamshidbekshodibekov2004@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]