import json
import time
import mysql.connector
import demoji
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load the sentiment analysis pipeline with TensorFlow weights
pipe = [
    pipeline("text-classification", model="candra/indobertweet-sentiment2"),
    pipeline("text-classification", model="ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa"),
    pipeline("text-classification", model="sahri/indonesiasentiment")
]
pipeTemp = [
    "candra/indobertweet-sentiment2",
    "ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa",
    "sahri/indonesiasentiment"
]
# Define a function to analyze the sentiment of a review
def analyze_sentiment(review):
    final_result = list()

    for i in range(3):
        tokenizer = AutoTokenizer.from_pretrained(pipeTemp[i])
        model = AutoModelForSequenceClassification.from_pretrained(pipeTemp[i])
        sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)
        max_length = tokenizer.model_max_length
        #inputs = tokenizer(review, truncation=True, max_length=512)
        #inputs = tokenizer.decode(inputs["input_ids"])
        inputs = review[:max_length - 2]
        #print(sentiment_analysis(inputs))
        result = sentiment_analysis(inputs)
        #print(result[0])
        final_result.append(result[0])
    
    x, y, z = final_result[0]['label'], final_result[1]['label'], final_result[2]['label']
    if x == "positive" and y == "Positive" and z == "positive":
        resFinal = "Positif"
    elif x == "negative" and y == "Negative" and z == "negative":
        resFinal = "Negatif"
    elif x == "neutral" and y == "Neutral" and z == "neutral":
        resFinal = "Netral"
    elif x == "positive" and y == "Positive" and z != "positive":
        resFinal = "Positif"
    elif x == "positive" and y != "Positive" and z == "positive":
        resFinal = "Positif"
    elif x != "positive" and y == "Positive" and z == "positive":
        resFinal = "Positif"
    elif x == "negative" and y == "Negative" and z != "negative":
        resFinal = "Negatif"
    elif x == "negative" and y != "Negative" and z == "negative":
        resFinal = "Negatif"
    elif x != "negative" and y == "Negative" and z == "negative":
        resFinal = "Negatif"
    elif x == "neutral" and y == "Neutral" and z != "neutral":
        resFinal = "Netral"
    elif x == "neutral" and y != "Neutral" and z == "neutral":
        resFinal = "Netral"
    elif x != "neutral" and y == "Neutral" and z == "neutral":
        resFinal = "Netral"
    else:
        resFinal = "#ASKME"
    print(resFinal)
    return final_result[0], final_result[1], final_result[2], resFinal

mydb = mysql.connector.connect(
    host="localhost",
    db="wisata_jogja",
    user="user_wisata",
    password="DGNDH/i33-kJpStS"
)
mycursor = mydb.cursor()
query = "SELECT * FROM reviews WHERE review_text != '' AND (sentiment_1 is null OR sentiment_2 is null OR sentiment_3 is null ) ORDER BY id DESC LIMIT 1"
mycursor.execute(query)
reviews = mycursor.fetchall()

# Add start timer in here
start_time = time.time()

for review in reviews:
    textRev = demoji.replace_with_desc(review[5], ":")
    sentiment1, sentiment2, sentiment3, sentimentResult = analyze_sentiment(textRev)                               
    query = "UPDATE reviews SET review_text=%s, sentiment_1=%s, sentiment_2=%s, sentiment_3=%s, sentiment_result='"+str(sentimentResult)+"' WHERE id='"+str(review[0])+"'"
    values = (textRev, json.dumps(sentiment1, indent=2), json.dumps(sentiment2, indent=2), json.dumps(sentiment3, indent=2))
    #mycursor.execute(query, values)
    #mycursor.execute("Commit")

# close connection
mydb.close()

# add end timer in here
end_time = time.time()

# Calculate the time taken
time_taken = end_time - start_time
print(f'Time taken: {time_taken} seconds')