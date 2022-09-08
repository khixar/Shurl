import random
import string

from shorturl.models import Url


def generate_random_string(random_str):
    """
    - This could generate 56 billion uniq combinations
    - No need to pre-populate DB with uniq strings because
    of MVP nature of the project
    """

    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def shorten_url(long_url):
    """
    return the short url
    """
    random_str = generate_random_string(long_url)
    return f"http://shurl.com/{random_str}"


def is_short_url_exists(short_url):
    return Url.objects.filter(short_url=short_url).exists()
