from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from functools import reduce

def get_sentiment_score(comment):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(comment)

def merge_scores(score1, score2):
    return {key: score1[key] + score2[key] for key in score1}

def get_average_sentiment_score(comments):
    num_comments = len(comments)
    total_scores = reduce(merge_scores, map(get_sentiment_score, comments))
    average_scores = {key: total / num_comments for key, total in total_scores.items()}
    return format_sentiment_scores(average_scores)

def format_sentiment_scores(scores):
    formatted_scores = {}
    for key, score in scores.items():
        if key == 'compound':
            formatted_scores[key] = format_sentiment_score(score)
        else:
            formatted_scores[key] = score
    return formatted_scores

def format_sentiment_score(score):
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"
    

    
# The compound score is the most important and is computed as a normalized value between -1 (most negative) and +1 (most positive). It summarizes the sentiment of the text:
# Compound score > 0.05: Positive sentiment
# Compound score < -0.05: Negative sentiment
# Compound score between -0.05 and 0.05: Neutral sentiment