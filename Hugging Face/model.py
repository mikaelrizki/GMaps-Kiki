import pandas as pd
from transformers import pipeline

# Load the sentiment analysis pipeline with TensorFlow weights
pipe = pipeline("text-classification", model="candra/indobertweet-sentiment2")

# Read the text from the document.txt file
with open("document.txt", "r", encoding="utf-8") as file:
    reviews = file.readlines()

# Remove the first line ("review") as it is just a header
reviews = reviews[1:]

# Create a list to store the results
results = []

# Analyze sentiments and add results to the list
for review in reviews:
    review = review.strip()  # Remove leading/trailing whitespaces
    result = pipe(review)
    sentiment = result[0]["label"]
    results.append({"review": review, "result": sentiment})

# Create a DataFrame from the list of results
df = pd.DataFrame(results, columns=["review", "result"])

# Save the DataFrame to a CSV file
df.to_csv("result.csv", index=False)

# Display the DataFrame
print(df)
