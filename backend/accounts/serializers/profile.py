from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Minimal public view of a User for embedding in Profile."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "avatar_url", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        """
        Allow updating bio + avatar_url only.
        """
        instance.bio = validated_data.get("bio", instance.bio)
        instance.avatar_url = validated_data.get("avatar_url", instance.avatar_url)
        instance.save()
        return instance