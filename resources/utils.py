from urllib.parse import urlparse
import random, string, requests


def generate_short_url():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))

def validate_url(url):
    try:
        parsed_url = urlparse(url)
        if all([parsed_url.scheme, parsed_url.netloc]):
            response = requests.get(url)
            response.raise_for_status()
            return True
        return False
    except requests.exceptions.RequestException:
        return False