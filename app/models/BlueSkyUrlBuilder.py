def extract_profile_and_post(url):
    try:
        profile_part = url.split('profile/')[1].split('/')[0]
        post_part = url.split('post/')[1]
        return [profile_part, post_part]
    except IndexError:
        return ["", ""]
    
def create_uri(profile_and_post):
    profile_part, post_part = profile_and_post
    return f'at://{profile_part}/app.bsky.feed.post/{post_part}'

def get_bluesky_uri(url):
    profile_part, post_part = extract_profile_and_post(url)
    return create_uri([profile_part, post_part])
