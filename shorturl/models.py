from django.db import models
from django.contrib.auth.models import User

from shurl.project_utils import ModelWithUUID


class Profile(ModelWithUUID):
    """
    location: just to improve the cache url capabilities later
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


class Url(ModelWithUUID):
    """
    short_url: shorten url of max length 6
    long_url: original url
    expired_at: short url expiry
    user: user who generated the short url
    """
    short_url = models.CharField(max_length=30, unique=True)
    long_url = models.CharField(max_length=5000)
    expired_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="shurl",
        null=True,
        blank=True)

    indexes = [
        models.Index(fields=['short_url']),
        models.Index(fields=['long_url']),
    ]

    def __str__(self):
        return f"{self.short_url} - {self.long_url}"
