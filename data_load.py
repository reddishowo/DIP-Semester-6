import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['apex_reviews']
collection = db['reviews']

df = pd.read_csv('apex_reviews_structured.csv')

records = df.to_dict('records')

try:
    result = collection.insert_many(records)
    print(f"Successfully inserted {len(result.inserted_ids)} documents into MongoDB")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    count = collection.count_documents({})
    print(f"Total documents in collection: {count}")
except Exception as e:
    print(f"Error counting documents: {e}")