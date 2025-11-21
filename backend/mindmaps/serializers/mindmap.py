from rest_framework import serializers
from mindmaps.models import MindMap, MindMapNode


class MindMapSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = MindMap
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Attach current user as owner when creating.
        """
        user = self.context["request"].user
        return MindMap.objects.create(owner=user, **validated_data)
    
class MindMapNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindMapNode
        fields = [
            "id",
            "mindmap",
            "parent",
            "title",
            "note",
            "resource",
            "position_x",
            "position_y",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]