from django.conf import settings
from django.db import models

class Rating(models.Model):
    resource = models.ForeignKey(
        "resources.Resource",
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    score = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("resource", "user")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["resource", "-created_at"]),
        ]

    def __str__(self):
        return f"Rating({self.score}) by {self.user_id} on {self.resource_id}"
