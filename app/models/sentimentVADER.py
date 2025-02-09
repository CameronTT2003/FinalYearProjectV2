from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
from functools import reduce

def get_sentiment_score(comment):
    analyzer = SentimentIntensityAnalyzer()
    comment = emoji.demojize(comment)
    return analyzer.polarity_scores(comment)

def merge_scores(score1, score2):
    return {key: score1[key] + score2[key] for key in score1}

def get_average_sentiment_score(comments):
    num_comments = len(comments)
    total_scores = reduce(merge_scores, map(get_sentiment_score, comments))
    return {key: total / num_comments for key, total in total_scores.items()}
