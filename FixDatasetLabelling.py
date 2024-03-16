import json
import time
import demoji
import mysql.connector
from transformers import pipeline

# Load the sentiment analysis pipeline with TensorFlow weights
pipe = [
    pipeline("text-classification", model="candra/indobertweet-sentiment2"),
    pipeline("text-classification", model="ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa"),
    pipeline("text-classification", model="sahri/indonesiasentiment")
]


# Define a function to analyze the sentiment of a review
def analyze_sentiment(review):
    final_result = list()
    for i in range(3):
        if i == 2:
            reviewDemoji = demoji.replace_with_desc(review, "")
        else:
            reviewDemoji = demoji.replace_with_desc(review, ":")
        # Truncate or split the review if it exceeds the maximum length
        max_length = pipe[i].model.config.max_position_embeddings
        time.sleep(0.5)
        if len(reviewDemoji) > max_length:
            review_chunks = [reviewDemoji[i:i + max_length] for i in range(0, len(reviewDemoji), max_length)]
            # Analyze sentiment for each chunk and aggregate the results
            sentiments = [pipe[i](chunk)[0]["label"] for chunk in review_chunks]
            # For simplicity, you can take the most frequent sentiment as the overall sentiment
            # Alternatively, you can devise your own method to aggregate sentiments from chunks
            sentiment_counts = {label: sentiments.count(label) for label in set(sentiments)}
            final_result.append(max(sentiment_counts, key=sentiment_counts.get))
        else:
            # If the review is within the length limit, analyze sentiment directly
            result = pipe[i](reviewDemoji)
            final_result.append(result[0]["label"])
    x, y, z = final_result[0], final_result[1], final_result[2]
    if x == "positive" and y == "Positive" and z == "positive":
        summary_result = "Positif"
    elif x == "negative" and y == "Negative" and z == "negative":
        summary_result = "Negatif"
    elif x == "neutral" and y == "Neutral" and z == "neutral":
        summary_result = "Netral"
    elif x == "positive" and y == "Positive" and z != "positive":
        summary_result = "Positif"
    elif x == "positive" and y != "Positive" and z == "positive":
        summary_result = "Positif"
    elif x != "positive" and y == "Positive" and z == "positive":
        summary_result = "Positif"
    elif x == "negative" and y == "Negative" and z != "negative":
        summary_result = "Negatif"
    elif x == "negative" and y != "Negative" and z == "negative":
        summary_result = "Negatif"
    elif x != "negative" and y == "Negative" and z == "negative":
        summary_result = "Negatif"
    elif x == "neutral" and y == "Neutral" and z != "neutral":
        summary_result = "Netral"
    elif x == "neutral" and y != "Neutral" and z == "neutral":
        summary_result = "Netral"
    elif x != "neutral" and y == "Neutral" and z == "neutral":
        summary_result = "Netral"
    else:
        summary_result = "#ASKME"
    return x, y, z, summary_result


# Set up the database connection
mydb = mysql.connector.connect(
    host="localhost",
    db="wisata_jogja",
    user="user_wisata",
    password="DGNDH/i33-kJpStS"
)

# Initial the list of sentiment
lstOfSentiment = list()

# Make a query to get the reviews that have not been labeled
cursor = mydb.cursor()
query = "SELECT * FROM reviews WHERE review_text != '' AND (sentiment_1 is null OR sentiment_2 is null OR sentiment_3 is null ) ORDER BY id DESC LIMIT 10"
cursor.execute(query)
reviews = cursor.fetchall()

# Add start timer in here
start_time = time.time()

# Analyze the sentiment of each review and update the database
count = 0
for review in reviews:
    plainText = review[5]
    textRev = demoji.replace_with_desc(review[5], ":")
    sentiment1, sentiment2, sentiment3, sentimentResult = analyze_sentiment(plainText)
    query = "UPDATE reviews SET sentiment_1=%s, sentiment_2=%s, sentiment_3=%s, sentiment_result='"+str(sentimentResult)+"' WHERE id='"+str(review[0])+"'"
    values = ("Positif" if sentiment1 == "positive" else "Negatif" if sentiment1 == "negative" else "Netral", "Positif" if sentiment2 == "Positive" else "Negatif" if sentiment2 == "Negative" else "Netral", "Positif" if sentiment3 == "positive" else "Negatif" if sentiment3 == "negative" else "Netral")
    cursor.execute(query, values)

    lstOfSentiment.append(sentimentResult)
    print(count, sentimentResult, "|", sentiment1, "|", sentiment2, "|", sentiment3, "|", plainText.replace('\n', ' '))
    count += 1

# Commit the changes
cursor.execute("Commit")

# close connection
mydb.close()

# Add end timer in here
end_time = time.time()

# Print the total sentiment
print("\nTotal Sentiment : ", len(lstOfSentiment))

# Calculate the time taken
time_taken = end_time - start_time
print(f'Time taken : {time_taken.__round__(2)} seconds\n')

# Print the total sentiment of each category
print("Total Sentiment Positif\t: ", lstOfSentiment.count("Positif"))
print("Total Sentiment Negatif\t: ", lstOfSentiment.count("Negatif"))
print("Total Sentiment Netral \t: ", lstOfSentiment.count("Netral"))
print("Total Sentiment #ASKME \t: ", lstOfSentiment.count("#ASKME"))
