def extract_text_from_thread(thread):
    texts = []
    if hasattr(thread, 'record') and hasattr(thread.record, 'text'):
        texts.append(thread.record.text)
    if hasattr(thread, 'replies'):
        for reply in thread.replies:
            texts.extend(extract_text_from_thread(reply.post))
    return texts

def extract_replies_from_thread(thread):
    initial_text = thread.post.record.text if hasattr(thread, 'post') and hasattr(thread.post, 'record') and hasattr(thread.post.record, 'text') else ""
    texts = extract_text_from_thread(thread)
    return initial_text, texts

