from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Reset password

from .views import SimplePasswordResetView, SimplePasswordResetConfirmView

urlpatterns = [
    path("api/password-reset/", SimplePasswordResetView.as_view(), name="password-reset"),
    path("api/password-reset-confirm/", SimplePasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]


# for login and refresh
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# for register and logout

from .views import RegisterView, LogoutView

urlpatterns += [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]


# show profile and change password
from .views import ShowProfile, ChangePasswordAPIView

urlpatterns += [
    path('api/profile/', ShowProfile.as_view(), name='show_profile'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]

# channel list,retrieve,create,update and delete
from .views import (
    ChannelCreateAPIView,
    ChannelRetrieveAPIView,
    ChannelUpdateAPIView,
    ChannelListAPIView,
    ChannelDestroyAPIView,
    ChannelSubscribeAPIView
    )

urlpatterns += [
    path('api/channel/', ChannelCreateAPIView.as_view(), name='channel_create'),
    path('api/channel/<int:pk>/', ChannelRetrieveAPIView.as_view(), name='channel_retrieve'),
    path('api/channel/update/<int:pk>/', ChannelUpdateAPIView.as_view(), name='channel_update'),
    path('api/channel/list/', ChannelListAPIView.as_view(), name='channel_list'),
    path('api/channel/delete/<int:pk>/', ChannelDestroyAPIView.as_view(), name='channel_delete'),
    path('api/channel/subscribe/<int:pk>/', ChannelSubscribeAPIView.as_view(), name='channel_subscribe'),
    
]