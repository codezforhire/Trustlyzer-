import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Download VADER data
nltk.download('vader_lexicon')

# Init analyzer
sid = SentimentIntensityAnalyzer()

# Basic scraping function
def extract_trustpilot_reviews(base_url, max_reviews=1000):
    reviews = []
    page = 1
    headers = {'User-Agent': 'Mozilla/5.0'}

    with st.spinner("Scraping reviews..."):
        while len(reviews) < max_reviews:
            url = f"{base_url}?page={page}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                st.warning(f"Stopped at page {page}. Status: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            review_elements = soup.find_all('p', {'data-service-review-text-typography': 'true'})
            if not review_elements:
                break

            for r in review_elements:
                if len(reviews) < max_reviews:
                    reviews.append(r.text.strip())
                else:
                    break

            page += 1
            time.sleep(1.5)  # avoid 403

    return reviews

# Sentiment logic
def get_sentiment(text):
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.4:
        return 'Positive'
    elif compound <= -0.2:
        return 'Negative'
    else:
        return 'Neutral'

# App UI
st.set_page_config(page_title="Trustpilot Review Analyzer", layout="wide")
st.title("📊 Trustpilot Review Analysis Dashboard")
st.markdown("This is a dashboard for analyzing Trustpilot reviews using simple NLP logic.")

url = st.text_input("Enter the Trustpilot review page URL:", "https://www.trustpilot.com/review/bookshop.org")
if st.button("Start Analysis"):
    raw_reviews = extract_trustpilot_reviews(url, max_reviews=1000)

    if raw_reviews:
        df = pd.DataFrame(raw_reviews, columns=['review'])
        df['sentiment'] = df['review'].apply(get_sentiment)

        # Show stats
        st.success("✅ Scraping complete!")
        st.subheader("📋 Raw Reviews")
        st.dataframe(df.head(10))

        sentiment_counts = df['sentiment'].value_counts()

        # Examples
        st.subheader("🔍 Example Reviews by Sentiment")
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            example = df[df['sentiment'] == sentiment]['review'].head(1).values
            if len(example) > 0:
                st.markdown(f"**{sentiment} Example:** {example[0]}")

        # Charts
        st.subheader("📈 Sentiment Distribution")
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(sentiment_counts)

        with col2:
            fig, ax = plt.subplots()
            sns.countplot(data=df, x='sentiment', palette='Set2', order=['Positive', 'Neutral', 'Negative'])
            ax.set_title("Review Sentiment Counts")
            st.pyplot(fig)

    else:
        st.error("No reviews found or unable to scrape.")
