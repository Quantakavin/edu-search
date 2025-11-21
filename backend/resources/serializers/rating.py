from rest_framework import serializers
from resources.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "resource", "user", "score", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value


class RatingInputSerializer(serializers.Serializer):
    """
    Simple serializer for POST /resources/{id}/rate/ style endpoints.
    """
    score = serializers.IntegerField()

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value
