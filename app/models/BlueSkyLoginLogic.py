from atproto import Client
from atproto_client.exceptions import UnauthorizedError

def bluesky_login(username, password):
    client = Client()
    try:
        client.login(username, password)
    except UnauthorizedError as e:
        print("Wrong Details")
        raise UnauthorizedError(f"Login failed: {e}")
    return client
    
class BlueSkyClient:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password   