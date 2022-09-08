from rest_framework import serializers, fields
from shorturl.models import Url
from shorturl.utils import get_hostname


class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Url
        fields = ("short_url", "long_url", "expired_at")

    def get_short_url(self, obj):
        hostname = get_hostname()
        return f"{hostname}?url={obj.short_url}"
