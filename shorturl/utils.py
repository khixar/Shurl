import random
import string
import environ

from shorturl.models import Url
from shorturl import constants

env = environ.Env()


def generate_random_string(random_str):
    """
    - This could generate 56 billion uniq combinations
    - No need to pre-populate DB with uniq strings because
    of MVP nature of the project
    """

    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def get_hostname():
    if env('PROJECT_ENV') == "development":
        return constants.DEV_URL
    elif env('PROJECT_ENV') == "staging":
        return constants.STAGE_URL
    else:
        return constants.PROD_URL


def shorten_url(long_url):
    """
    return the short url
    """
    return generate_random_string(long_url)


def is_short_url_exists(short_url):
    return Url.objects.filter(short_url=short_url).exists()
