import pandas as pd
from pymongo import MongoClient

# Change the port from 27018 to 27017 (the default MongoDB port)
client = MongoClient('mongodb://localhost:27017/')
db = client['apex_reviews']
collection = db['reviews']

# Read the CSV file
df = pd.read_csv('apex_reviews_structured.csv')

# Convert DataFrame to a list of dictionaries for MongoDB
records = df.to_dict('records')

# Add error handling
try:
    # Insert the data into MongoDB
    result = collection.insert_many(records)
    print(f"Successfully inserted {len(result.inserted_ids)} documents into MongoDB")
except Exception as e:
    print(f"An error occurred: {e}")

# Verify insertion
try:
    count = collection.count_documents({})
    print(f"Total documents in collection: {count}")
except Exception as e:
    print(f"Error counting documents: {e}")