import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pymongo import MongoClient

# Connect to MongoDB and fetch data
# If you still have connection issues, you can comment out this part and load directly from CSV
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['apex_reviews']
    collection = db['reviews']
    
    # Convert MongoDB collection to DataFrame
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    print("Successfully loaded data from MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Loading from CSV file instead...")
    # Load from CSV as fallback
    df = pd.read_csv('apex_reviews_structured.csv')

# Print the shape and first few rows
print(f"Dataset shape: {df.shape}")
print("\nSample data:")
print(df.head())

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Set the aesthetic style of the plots
sns.set_style("whitegrid")
plt.figure(figsize=(14, 10))

# 1. Sentiment Distribution
plt.subplot(2, 2, 1)
sentiment_counts = df['sentiment'].value_counts()
colors = ['#ff9999' if x == 'negative' else '#66b3ff' if x == 'positive' else '#99ff99' for x in sentiment_counts.index]
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Distribution of Review Sentiment', fontsize=14)

# 2. Relationship between Sentiment Compound and Hours Played
plt.subplot(2, 2, 2)
# Filter out rows with missing hours_played
hours_data = df.dropna(subset=['hours_played'])
sns.scatterplot(x='hours_played', y='sentiment_compound', data=hours_data, hue='sentiment', palette={'positive': 'green', 'negative': 'red'})
plt.title('Sentiment Score vs. Hours Played', fontsize=14)
plt.xlabel('Hours Played')
plt.ylabel('Sentiment Compound Score')

# 3. Compare mentions of different issues
plt.subplot(2, 2, 3)
mentions = pd.DataFrame({
    'Issue': ['Cheaters', 'Servers', 'Matchmaking', 'Money'],
    'Count': [
        df['mentions_cheaters'].sum(),
        df['mentions_servers'].sum(),
        df['mentions_matchmaking'].sum(),
        df['mentions_money'].sum()
    ]
})
# Update the barplot to use 'hue' instead of just 'palette'
sns.barplot(x='Issue', y='Count', data=mentions, hue='Issue', palette='viridis', legend=False)
plt.title('Frequency of Issues Mentioned in Reviews', fontsize=14)
plt.ylabel('Number of Mentions')

# 4. Word Count Distribution by Sentiment
plt.subplot(2, 2, 4)
# Check the unique values in sentiment column and create a complete palette
sentiment_values = df['sentiment'].unique()
sentiment_palette = {}
for value in sentiment_values:
    if value == 'positive':
        sentiment_palette[value] = 'green'
    elif value == 'negative':
        sentiment_palette[value] = 'red'
    else:  # For neutral or any other category
        sentiment_palette[value] = 'gray'

# Use the complete palette
sns.boxplot(x='sentiment', y='word_count', data=df, hue='sentiment', palette=sentiment_palette, legend=False)
plt.title('Word Count Distribution by Sentiment', fontsize=14)
plt.xlabel('Sentiment')
plt.ylabel('Word Count')

# Adjust layout and save
plt.tight_layout()
plt.savefig('apex_reviews_visualization.png', dpi=300)
plt.show()

# Additional visualizations
plt.figure(figsize=(14, 10))

# 5. Sentiment components comparison (positive, negative, neutral)
plt.subplot(2, 2, 1)
# Create a DataFrame from the sentiment components for proper use with hue
sentiment_components = df[['sentiment_pos', 'sentiment_neg', 'sentiment_neu']].mean().reset_index()
sentiment_components.columns = ['Component', 'Value']
sns.barplot(x='Component', y='Value', data=sentiment_components, hue='Component', palette='Blues_d', legend=False)
plt.title('Average Sentiment Components Across All Reviews', fontsize=14)
plt.ylabel('Average Score')
plt.xlabel('Sentiment Component')

# 6. Cheaters mention vs Sentiment
plt.subplot(2, 2, 2)
cheaters_sentiment = df.groupby('mentions_cheaters')['sentiment_compound'].mean().reset_index()
cheaters_sentiment['mentions_cheaters'] = cheaters_sentiment['mentions_cheaters'].map({0: 'No', 1: 'Yes'})
sns.barplot(x='mentions_cheaters', y='sentiment_compound', data=cheaters_sentiment, hue='mentions_cheaters', palette='RdBu', legend=False)
plt.title('Average Sentiment Score by Mentions of Cheaters', fontsize=14)
plt.xlabel('Mentions Cheaters')
plt.ylabel('Average Sentiment Compound Score')

# 7. Correlation Heatmap
plt.subplot(2, 2, 3)
# Select only numeric columns for correlation
numeric_df = df.select_dtypes(include=[np.number])
correlation = numeric_df.corr()
mask = np.triu(np.ones_like(correlation, dtype=bool))
sns.heatmap(correlation, mask=mask, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, fmt='.2f')
plt.title('Correlation Between Numeric Features', fontsize=14)

# 8. Sentiment distribution by issue mentioned
plt.subplot(2, 2, 4)
# Create a new column that categorizes reviews by what they mention
def categorize_review(row):
    if row['mentions_cheaters'] == 1:
        return 'Cheaters'
    elif row['mentions_servers'] == 1:
        return 'Servers'
    elif row['mentions_matchmaking'] == 1:
        return 'Matchmaking'
    elif row['mentions_money'] == 1:
        return 'Money'
    else:
        return 'Other'

df['primary_issue'] = df.apply(categorize_review, axis=1)
sns.boxplot(x='primary_issue', y='sentiment_compound', data=df, palette='viridis')
plt.title('Sentiment Distribution by Primary Issue Mentioned', fontsize=14)
plt.xlabel('Primary Issue')
plt.ylabel('Sentiment Compound Score')
plt.xticks(rotation=45)

# Adjust layout and save
plt.tight_layout()
plt.savefig('apex_reviews_visualization_additional.png', dpi=300)
plt.show()

# Create a summary of findings
print("\n=== SUMMARY OF FINDINGS ===")
print(f"Total reviews analyzed: {len(df)}")
print(f"Positive reviews: {len(df[df['sentiment'] == 'positive'])} ({len(df[df['sentiment'] == 'positive'])/len(df)*100:.1f}%)")
print(f"Negative reviews: {len(df[df['sentiment'] == 'negative'])} ({len(df[df['sentiment'] == 'negative'])/len(df)*100:.1f}%)")
print(f"Average sentiment compound score: {df['sentiment_compound'].mean():.3f}")
print(f"Percentage of reviews mentioning cheaters: {df['mentions_cheaters'].mean()*100:.1f}%")
print(f"Percentage of reviews mentioning servers: {df['mentions_servers'].mean()*100:.1f}%")
print(f"Percentage of reviews mentioning matchmaking: {df['mentions_matchmaking'].mean()*100:.1f}%")
print(f"Percentage of reviews mentioning money issues: {df['mentions_money'].mean()*100:.1f}%")
print(f"Average word count: {df['word_count'].mean():.1f} words")

if 'hours_played' in df.columns and not df['hours_played'].isna().all():
    print(f"Average hours played: {df['hours_played'].dropna().mean():.1f} hours")