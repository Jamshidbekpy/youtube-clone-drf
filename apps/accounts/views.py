from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyUserSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView,ListAPIView,DestroyAPIView
# Create your views here.

# Reset Password

from .serializers import SimplePasswordResetSerializer, SimplePasswordResetConfirmSerializer

class SimplePasswordResetView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = SimplePasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Parolni tiklash havolasi emailga yuborildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimplePasswordResetConfirmView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = SimplePasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for auth RegisterView,LogoutView,ShowProfile,ChangePasswordAPIView

from .models import MyUser,Channel
class RegisterView(CreateAPIView):
    "Register a new user"
    permission_classes = []
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
    
    
from rest_framework_simplejwt.tokens import RefreshToken
class LogoutView(APIView):
    "Logout a user"
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ShowProfile(APIView):
    "Show user profile"
    def get(self, request):
        user = request.user
        serializer = MyUserSerializer(user)
        return Response(serializer.data)

from .serializers import ChangePasswordSerializer
class ChangePasswordAPIView(APIView):
    "Change user password"
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            RefreshToken.for_user(user)

            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Channel ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,CreateAPIView

from .serializers import ChannelCreateUpdateSerializer
class ChannelCreateAPIView(CreateAPIView):
    "Create a new channel"
    serializer_class = ChannelCreateUpdateSerializer
    queryset = Channel.objects.filter(is_active=True)
    

from .serializers import ChannelRetrieveSerializer
class ChannelRetrieveAPIView(RetrieveAPIView):
    "Retrieve a channel"
    permission_classes = []
    serializer_class = ChannelRetrieveSerializer
    queryset = Channel.objects.filter(is_active=True)
  

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
class ChannelUpdateAPIView(UpdateAPIView):
    "Update a channel"
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = ChannelCreateUpdateSerializer
    queryset = Channel.objects.filter(is_active=True)

from .serializers import ChannelListSerializer
class ChannelListAPIView(ListAPIView):
    "Followed channels"
    serializer_class = ChannelListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.channels.all()
  
from django.shortcuts import get_object_or_404  
class ChannelDestroyAPIView(APIView):       
    "Delete a channel"
    def delete(self, request, pk):
        channel = get_object_or_404(Channel, id=pk)
        if request.user.channel == channel:
            channel.delete()
            return Response({"message": "Channel deleted successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "You don't have permission to delete this channel."}, status=status.HTTP_403_FORBIDDEN)

class ChannelSubscribeAPIView(APIView):
    "Subscribe to a channel"
    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        user = request.user
        if user.channel != channel:
            if channel.subscribers.filter(id=request.user.id).exists():
                channel.subscribers.remove(request.user)
                return Response({"message": "Unsubscribed successfully."}, status=status.HTTP_200_OK)
            channel.subscribers.add(request.user)
            return Response({"message": "Subscribed successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "You cannot subscribe to your own channel."}, status=status.HTTP_400_BAD_REQUEST)
        
        


