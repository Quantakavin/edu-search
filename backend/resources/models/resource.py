from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Resource(models.Model):
    ARTICLE = "article"
    VIDEO = "video"
    PDF = "pdf"
    COURSE = "course"
    OTHER = "other"

    CONTENT_TYPE_CHOICES = (
        (ARTICLE, "Article"),
        (VIDEO, "Video"),
        (PDF, "PDF"),
        (COURSE, "Course"),
        (OTHER, "Other"),
    )

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

    DIFFICULTY_CHOICES = (
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default=ARTICLE,
    )
    subject = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        blank=True,
    )

    tags = models.ManyToManyField("resources.Tag", related_name="resources", blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    is_published = models.BooleanField(default=True)

    # denormalised rating info
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["subject"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["content_type"]),
            models.Index(fields=["-created_at"]),
            models.Index(fields=["-avg_rating"]),
            models.Index(fields=["title"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:240]
            slug = base_slug
            counter = 1
            # simple uniqueness loop
            while Resource.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ResourceFile(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="files",
    )
    # For Cloudinary or any external storage
    file_url = models.URLField(blank=True)
    # If you want local file storage as a fallback
    file = models.FileField(upload_to="resource_files/", blank=True)
    label = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["resource", "order"]),
        ]

    def __str__(self):
        return self.label or f"File {self.pk} for {self.resource_id}"
