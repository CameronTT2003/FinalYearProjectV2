import csv
from datetime import datetime

#this function is used to save the results to a csv file
def save_to_csv(username, url, initial_text, vader_sentiment_score, sentiment_text):
    filename = "results.csv"
    header = ['UserId','Date', 'URL', 'Initial Text', 'Vader Sentiment Score', 'Sentiment Text']
        
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(header)

        writer.writerow([username, current_date, url, initial_text, vader_sentiment_score, sentiment_text])

def delete_record(username, record_date):
    filename = "results.csv"
    records = []

    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not (row['UserId'] == username and row['Date'] == record_date):
                records.append(row)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['UserId', 'Date', 'URL', 'Initial Text', 'Vader Sentiment Score', 'Sentiment Text'])
        writer.writeheader()
        writer.writerows(records)

#this function is used to get the records of a user from the csv file
def get_user_records(username):
    with open("results.csv", mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = [
            {
                'date': row['Date'],
                'initial_text': row['Initial Text'],
                'vader_sentiment_score': row['Vader Sentiment Score'],
                'sentiment_text': row['Sentiment Text']
            }
            for row in reader if row['UserId'] == username
        ]
    return sort_records_by_date(records)

#this function is used to sort the records by date in descending order
def sort_records_by_date(records):
    return sorted(records, key=lambda x: x['date'], reverse=True)