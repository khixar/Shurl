from rest_framework import serializers, fields
from shorturl.models import Url


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ("short_url", "long_url", "expired_at")
