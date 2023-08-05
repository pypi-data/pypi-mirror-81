import requests

PROXY_POOL_URL = 'http://localhost:5555/random'
DEFAULT_PROXY = 'default_proxy'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
