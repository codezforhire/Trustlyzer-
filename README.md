# Trustlyzer 🧠📊

**Trustlyzer** is a lightweight Streamlit dashboard that scrapes up to 1,000 customer reviews from Trustpilot (e.g. Bookshop.org) and analyzes them using VADER sentiment analysis to provide real-time insights into customer feedback.

## 🚀 Features

- Web scraping of Trustpilot reviews
- Real-time sentiment analysis (Positive, Neutral, Negative)
- Interactive visualizations (Pie chart, Bar chart, Heatmap)
- Highlights examples of best and worst reviews
- Clean and responsive Streamlit UI

## 🛠 Built With

- Python
- Streamlit
- BeautifulSoup
- NLTK (VADER Sentiment Analyzer)
- Plotly / Seaborn
- Pandas / NumPy

 

## 📦 Installation

```bash
git clone https://github.com/yourusername/trustlyzer.git
cd trustlyzer
pip install -r requirements.txt
streamlit run trustpilot_sentiment_app.py
