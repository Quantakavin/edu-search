from rest_framework import serializers
from resources.models import Resource, ResourceFile, Tag


class ResourceFileSerializer(serializers.ModelSerializer):
    """Read-only representation of files attached to a resource."""

    class Meta:
        model = ResourceFile
        fields = ["id", "file_url", "file", "label", "order", "created_at"]
        read_only_fields = ["id", "created_at"]


class ResourceFileInputSerializer(serializers.Serializer):
    """
    Write-only input format for files when creating/updating a resource.
    (You can send either file_url or upload a file later.)
    """
    file_url = serializers.URLField(required=False, allow_blank=True)
    label = serializers.CharField(max_length=100, required=False, allow_blank=True)
    order = serializers.IntegerField(required=False, default=0)
    # If you want to support direct file upload now, you can add:
    # file = serializers.FileField(required=False)


class ResourceSerializer(serializers.ModelSerializer):
    """
    Main serializer for resources.

    - Read: includes tags + files.
    - Write: accepts tag_names (list of strings) and files_input (list of file objects).
    """

    # Read-only nested tags + files
    tags = serializers.SerializerMethodField(read_only=True)
    files = ResourceFileSerializer(many=True, read_only=True)

    # Write-only inputs
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of tag names to attach to this resource.",
    )
    files_input = ResourceFileInputSerializer(
        many=True,
        write_only=True,
        required=False,
        help_text="List of files to attach to this resource.",
    )

    # Show the creator as username in responses
    created_by = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Resource
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "content_type",
            "subject",
            "difficulty",
            "tags",
            "tag_names",
            "files",
            "files_input",
            "created_by",
            "is_published",
            "avg_rating",
            "rating_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "created_by",
            "avg_rating",
            "rating_count",
            "created_at",
            "updated_at",
        ]

    # ----- Helpers -----

    def get_tags(self, obj):
        """Return tags as simple objects {id, name, slug}."""
        tags = obj.tags.all()
        return [{"id": t.id, "name": t.name, "slug": t.slug} for t in tags]

    # ----- Create / update -----

    def create(self, validated_data):
        """
        Create a resource + its tags + files.
        """
        tag_names = validated_data.pop("tag_names", [])
        files_data = validated_data.pop("files_input", [])
        user = self.context["request"].user

        # Create the resource
        resource = Resource.objects.create(created_by=user, **validated_data)

        # Attach tags
        self._set_tags(resource, tag_names)

        # Attach files
        self._set_files(resource, files_data)

        return resource

    def update(self, instance, validated_data):
        """
        Update a resource and optionally replace tags/files.
        """
        tag_names = validated_data.pop("tag_names", None)
        files_data = validated_data.pop("files_input", None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Tags: if provided, replace them
        if tag_names is not None:
            self._set_tags(instance, tag_names)

        # Files: if provided, replace them
        if files_data is not None:
            self._set_files(instance, files_data)

        return instance

    # ----- Internal helpers -----

    def _set_tags(self, resource, tag_names):
        if not tag_names:
            resource.tags.clear()
            return

        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        resource.tags.set(tags)

    def _set_files(self, resource, files_data):
        # Simple strategy: clear and recreate. Good enough for v1.
        ResourceFile.objects.filter(resource=resource).delete()
        for file_data in files_data:
            ResourceFile.objects.create(resource=resource, **file_data)
