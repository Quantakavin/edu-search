from django.conf import settings
from django.db import models
from resources.models import Resource

class MindMap(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mindmaps",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "-created_at"]),
        ]

    def __str__(self):
        return f"MindMap({self.title})"
    


class MindMapNode(models.Model):
    mindmap = models.ForeignKey(
        MindMap,
        on_delete=models.CASCADE,
        related_name="nodes",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)

    # Optional link to a resource
    resource = models.ForeignKey(
        Resource,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mindmap_nodes",
    )

    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["mindmap"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return f"MindMapNode({self.title}) in {self.mindmap_id}"