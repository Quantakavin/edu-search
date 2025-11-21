from rest_framework import serializers
from resources.models import Bookmark
from .resource import ResourceSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Used to list a user's bookmarks with the full resource embedded.
    """
    resource = ResourceSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "resource", "created_at"]
        read_only_fields = ["id", "resource", "created_at"]
