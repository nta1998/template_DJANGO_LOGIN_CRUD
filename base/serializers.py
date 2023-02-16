# ------import------
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Profile,Post
# ------login serializers return token-------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        return token
# -----model serializers-----
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    def create(self, validated_data):
        user = self.context['user']
        print(user)
        return Profile.objects.create(**validated_data,user=user)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    def create(self, validated_data):       
        user = self.context['user']
        print(user)
        return Post.objects.create(**validated_data,user=user)