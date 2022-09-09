from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.cache import cache

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from shorturl.models import Url
from shorturl import responses
from shorturl.serializers import UrlSerializer
from shorturl.utils import shorten_url, is_short_url_exists
from shorturl import constants


class CreateShortUrl(generics.CreateAPIView):
    """
    Creates the unique short url for the given
    long url entered by the user

    Args:
        - long_url(`str`): the url that needs to be shortened

    Returns:
        - short_url(`string`): the short form url.
        - long_url(`string`): the orignal url.
        - expired_at(`datetime`): url expiry time.
    """
    queryset = Url.objects.none()
    serializer_class = UrlSerializer

    def post(self, request):
        long_url = request.data.get("long_url", None)

        if not long_url:
            return Response({
                "code": responses.ERR_4103_MISSING_KEY_OR_QUERY,
                "message": "Missing long_url key",
                "usage_examples": [
                    "{ 'long_url' : 'https://abcdefghi.com' }"
                ],
            }, status=status.HTTP_400_BAD_REQUEST)

        # if long url already exists
        # assuming we can return same short url with same long url
        uniq_long = True
        url = Url.objects.filter(long_url=long_url).last()
        if url:
            # can check for user uniqueness as well.
            # if we need to return every user the uniq url
            uniq_long = False

        elif uniq_long:
            # believe in randomness and limit it to 10
            iter_count = 0
            short_url = None
            while iter_count < constants.MAX_RANDOM_RETRIES:
                short_url = shorten_url(long_url)
                if not is_short_url_exists(short_url):
                    break

                iter_count += 1

            # Let user try again after 10 random internal attempts.
            if not short_url or is_short_url_exists(short_url):
                return Response({
                    "code": responses.ERR_4009_CONFLICT,
                    "message": "Unable to process your request. Please try again",
                    "usage_examples": [
                        "{ 'long_url' : 'https://abcdefghi.com' }"
                    ],
                }, status=status.HTTP_409_CONFLICT)

            url = Url.objects.create(
                short_url=short_url,
                long_url=long_url,
                expired_at=timezone.now() + timedelta(days=365),
            )

        serializer_data = UrlSerializer(url).data
        return Response(serializer_data)


class FetchShortUrl(generics.ListAPIView):
    """
    Generate long url if user enters the
    short url. Front-end will use the long url to
    show the orignal content

    Args: url(`string`) as query param

    Returns:
        - short_url(`string`): the short form url.
        - long_url(`string`): the orignal url.
        - expired_at(`datetime`): url expiry time.
    """

    def list(self, request):
        short_url = request.query_params.get('url', None)
        if not short_url:
            return Response({
                "code": responses.ERR_4103_MISSING_KEY_OR_QUERY,
                "message": "Missing url query param",
                "usage_examples": [
                    "{ 'GET' : '?url=http://shurl.com/saI9WF' }"
                ],
            }, status=status.HTTP_400_BAD_REQUEST)

        url = Url.objects.filter(short_url=short_url).last()
        if url:
            """
            #! redirecting in API just for illustration
            purposes otherwise this should be done on FE.
            """
            return redirect(url.long_url)

            """
            #! If FE is integrated then it can utilise the
            returned long url to display the exact contents
            of the page.
            """

            serializer_data = UrlSerializer(url).data
            return Response(serializer_data)

        else:
            return Response({
                "code": responses.ERR_4044_RESOURCE_NOT_FOUND,
                "message": "Resouce not found",
                "usage_examples": [
                    "{ 'GET' : 'host?url=http://shurl.com/saI9WF' }"
                ],
            }, status=status.HTTP_404_NOT_FOUND)
