from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    CharField,
    ValidationError,
    )

from .models import MyUser, Channel

class MyUserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'profile_picture', 'bio','password','confirm_password']

    def validate(self, data):
        if MyUser.objects.filter(username=data.get('username')).exists():
            raise ValidationError({"username": "Username already exists!"})
        
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError({"password": "Password do not match!"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        return MyUser.objects.create_user(**validated_data)
    
    
class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True, min_length=8)
    confirm_password = CharField(required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError({"error": "New passwords do not match"})
        return data


class ChannelCreateUpdateSerializer(ModelSerializer):
    owner = MyUserSerializer(read_only=True)
    class Meta:
        model = Channel
        fields = ['name', 'owner','description', 'image', 'banner','created_at','updated_at']
        
    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['owner'] = user
        return Channel.objects.create(**validated_data)
        
        
        
from apps.content.models import Category
from apps.content.serializers import CategorySerializer, VideoSerializer
class ChannelRetrieveSerializer(ModelSerializer):
    subscribers_count = SerializerMethodField()
    categories = SerializerMethodField()
    videos_count = SerializerMethodField()
    videos_list = SerializerMethodField()
    
    class Meta:
        model = Channel
        fields = ['name', 'owner','description', 'image', 'banner','subscribers_count','categories','videos_count','videos_list']
        
    def get_subscribers_count(self, obj):
        return obj.subscribers.count()
    
    def get_categories(self, obj):
        categories = Category.objects.all().order_by('name')
        return CategorySerializer(categories, many=True).data
    
    def get_videos_list(self, obj):
        default_category =  Category.objects.all().order_by('name').first()
        category = self.context.get('request').query_params.get('slug').capitalize()
        if category:
            try:
                category = Category.objects.get(name=category)
            except Category.DoesNotExist:
                category = default_category
        else:
            category = default_category
        videos = obj.videos.filter(category=category,is_active=True)
        return VideoSerializer(videos, many=True).data
    
    def get_videos_count(self, obj):
        return obj.videos.count()
        

class ChannelListSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'image']  
        

# serializers.py

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SimplePasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Bu email bilan foydalanuvchi topilmadi.")

        return value

    def send_reset_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"http://localhost:8000/accounts/api/password-reset-confirm/?uid={uid}&token={token}"

        send_mail(
            "Parolni tiklash",
            f"Parolingizni tiklash uchun quyidagi havolani bosing: {reset_url}",
            "your-email@gmail.com",
            [user.email],
            fail_silently=False,
        )

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        self.send_reset_email(user)


class SimplePasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError("Noto‘g‘ri URL.")

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Token noto‘g‘ri yoki muddati o‘tgan.")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
