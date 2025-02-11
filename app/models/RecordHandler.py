import csv
from datetime import datetime


def save_to_csv(username, url, initial_text, vader_sentiment_score, sentiment_text):
    filename = "results.csv"
    header = ['UserId','Date', 'URL', 'Initial Text', 'Vader Sentiment Score', 'Sentiment Text']
        
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(header)

        writer.writerow([username, current_date, url, initial_text, vader_sentiment_score, sentiment_text])

def get_user_records(self, username):
    records = []
    with open("results.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['UserId'] == username:
                records.append({
                    'date': row['Date'],
                    'initial_text': row['Initial Text'],
                    'vader_sentiment_score': row['Vader Sentiment Score'],
                    'sentiment_text': row['Sentiment Text']
                })
    #descending order
    records.sort(key=lambda x: x['date'], reverse=True)
    return records