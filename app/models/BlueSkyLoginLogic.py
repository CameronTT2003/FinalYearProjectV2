from atproto import Client
from atproto_client.exceptions import UnauthorizedError

def bluesky_login(username, password):
    client = Client()
    try:
        client.login(username, password)
        print("hi")
        return client
    except UnauthorizedError as e:
        raise UnauthorizedError(f"Login failed: {e}")
    