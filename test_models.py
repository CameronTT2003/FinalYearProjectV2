import os
import csv
import json
import asyncio
import tempfile
import datetime
import pytest
from functools import reduce

# ---- SentimentVADER Tests ----
from app.models.SentimentVADER import (
    get_sentiment_score,
    merge_scores,
    get_average_sentiment_score,
    format_sentiment_score,
    format_scores_to_two_decimals,
    format_sentiment_scores,
)

def test_get_sentiment_score():
    comment = "I love this product!"
    scores = get_sentiment_score(comment)
    for key in ['neg', 'neu', 'pos', 'compound']:
        assert key in scores
        assert isinstance(scores[key], float)

def test_merge_scores():
    s1 = {'neg': 0.1, 'neu': 0.6, 'pos': 0.1, 'compound': 0.2}
    s2 = {'neg': 0.2, 'neu': 0.3, 'pos': 0.3, 'compound': 0.1}
    merged = merge_scores(s1, s2)
    formatted = format_scores_to_two_decimals(merged)
    #print(formatted)
    expected = {'neg': 0.3, 'neu': 0.9, 'pos': 0.4, 'compound': 0.3}
    assert formatted == expected

def test_format_sentiment_score():
    assert format_sentiment_score(0.1) == "Positive"
    assert format_sentiment_score(-0.1) == "Negative"
    assert format_sentiment_score(0) == "Neutral"


# ---- RecordHandler Tests ----
import app.models.RecordHandler as RecordHandler

@pytest.fixture(autouse=True)
def isolated_csv(tmp_path, monkeypatch):
    # Change CWD so RecordHandler functions use a temp "results.csv"
    monkeypatch.chdir(tmp_path)
    # Ensure a clean slate
    open("results.csv", mode="w").close()
    yield

def test_save_and_get_records():
    username = "test_user"
    url = "http://example.com"
    initial_text = "Hello world"
    vader_score = "{'neg': 0.1, 'neu': 0.6, 'pos': 0.1, 'compound': 'Neutral'}"
    sentiment_text = "Test sentiment summary"
    
    # Save record
    RecordHandler.save_to_csv(username, url, initial_text, vader_score, sentiment_text)
    
    # Get records for that user
    records = RecordHandler.get_user_records(username)
    assert len(records) == 1
    rec = records[0]
    assert rec['initial_text'] == initial_text
    assert rec['vader_sentiment_score'] == vader_score
    assert rec['sentiment_text'] == sentiment_text
    assert rec['url'] == url

def test_delete_record():
    username = "test_user"
    url = "http://example.com"
    initial_text = "Hello world"
    vader_score = "{'neg': 0.1, 'neu': 0.6, 'pos': 0.1, 'compound': 'Neutral'}"
    sentiment_text = "Test sentiment summary"
    
    # Save two records with different timestamp
    RecordHandler.save_to_csv(username, url, initial_text, vader_score, sentiment_text)
    # Force a different date by manually writing another record
    fake_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    header = ['UserId','Date', 'URL', 'Initial Text', 'Vader Sentiment Score', 'Sentiment Text']
    with open("results.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, fake_date, url, initial_text, vader_score, sentiment_text])
    
    # Delete record with fake_date
    RecordHandler.delete_record(username, fake_date)
    records = RecordHandler.get_user_records(username)
    # Only one record should remain (the one with the later date)
    assert len(records) == 1
    assert records[0]['date'] != fake_date

# ---- BlueSkyTextBuilder Tests ----
from app.models.BlueSkyTextBuilder import extract_text_from_thread, extract_replies_from_thread

# Define dummy thread objects to simulate nested replies structure
class DummyRecord:
    def __init__(self, text):
        self.text = text

class DummyThread:
    def __init__(self, text=None, replies=None):
        self.record = DummyRecord(text) if text is not None else None
        self.replies = replies or []
        # Some threads may have a "post" attribute for replies extraction
        self.post = self

def create_dummy_thread():
    # A thread with an initial text and two nested replies
    reply1 = DummyThread("Reply 1")
    reply2 = DummyThread("Reply 2")
    main_thread = DummyThread("Initial text", replies=[reply1, reply2])
    return main_thread

def test_extract_text_from_thread():
    thread = create_dummy_thread()
    texts = extract_text_from_thread(thread)
    # The main thread's record is included in extract_replies_from_thread only
    # extract_text_from_thread gets text from child replies recursively.
    # Here we expect two replies.
    assert "Reply 1" in texts
    assert "Reply 2" in texts

def test_extract_replies_from_thread():
    thread = create_dummy_thread()
    initial_text, texts = extract_replies_from_thread(thread)
    assert initial_text == "Initial text"
    assert "Reply 1" in texts and "Reply 2" in texts

# ---- BlueSkyLoginLogic Tests ----
from app.models.BlueSkyLoginLogic import bluesky_login, BlueSkyClient
from atproto_client.exceptions import UnauthorizedError

# For testing login function we can monkeypatch Client.login
class DummyClient:
    def __init__(self):
        self.logged_in = False
    def login(self, username, password):
        if username == "valid" and password == "valid":
            self.logged_in = True
        else:
            from atproto_client.exceptions import UnauthorizedError
            raise UnauthorizedError("Invalid credentials")

def dummy_client_factory():
    return DummyClient()

def test_bluesky_login_success(monkeypatch):
    # Monkey-patch the Client in BlueSkyLoginLogic to use DummyClient.
    from atproto import Client as RealClient
    monkeypatch.setattr("app.models.BlueSkyLoginLogic.Client", lambda: dummy_client_factory())
    
    client = bluesky_login("valid", "valid")
    assert client.logged_in is True

def test_bluesky_login_failure(monkeypatch):
    monkeypatch.setattr("app.models.BlueSkyLoginLogic.Client", lambda: dummy_client_factory())
    with pytest.raises(UnauthorizedError):
        bluesky_login("invalid", "invalid")

