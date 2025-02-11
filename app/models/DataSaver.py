import csv
from datetime import datetime


def save_to_csv(username, url, initial_text, vader_sentiment_score, sentiment_text):
    # Define the header
    filename = "results.csv"
    header = ['UserId','Date', 'URL', 'Initial Text', 'Vader Sentiment Score', 'Sentiment Text']
        
    # Get the current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    # Open the file in append mode
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
            
        # Check if the file is empty to write the header
        if file.tell() == 0:
            writer.writerow(header)
            
        # Write the data
        writer.writerow([username, current_date, url, initial_text, vader_sentiment_score, sentiment_text])