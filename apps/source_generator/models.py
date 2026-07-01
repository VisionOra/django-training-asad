from django.db import models
from django.conf import settings


class SourceSearch(models.Model):
    """A search query submitted by a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='source_searches',
    )
    topic = models.CharField(max_length=500)
    limit = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.topic} ({self.limit} sources)"


class Source(models.Model):
    """A single source result fetched from Serper API for a search."""
    search = models.ForeignKey(
        SourceSearch,
        on_delete=models.CASCADE,
        related_name='sources',
    )
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=1000)
    snippet = models.TextField(blank=True)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"[{self.position}] {self.title}"
