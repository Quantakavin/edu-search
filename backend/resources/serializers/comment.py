from rest_framework import serializers
from resources.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    # Show username instead of user id
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "resource",
            "user",
            "body",
            "parent",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "is_deleted", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Attach current request.user as the comment author.
        """
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
