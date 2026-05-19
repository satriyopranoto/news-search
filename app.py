import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, jsonify
from pygooglenews import GoogleNews
from openai import OpenAI
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# LLM Configuration
SENTIMENT_ANALYSIS_ENABLED = os.getenv("SENTIMENT_ANALYSIS_ENABLED", "true").lower() == "true"
SENTIMENT_MODE = os.getenv("SENTIMENT_MODE", "generative").lower()
API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

# Light Model Configuration
LIGHT_MODEL_NAME = os.getenv("LIGHT_MODEL_NAME", "lxyuan/distilbert-base-multilingual-cased-sentiments-student")

client = OpenAI(base_url=API_BASE, api_key=API_KEY)

# Initialize Light Model if needed
light_pipeline = None
if SENTIMENT_ANALYSIS_ENABLED and SENTIMENT_MODE == "light":
    print(f"Loading light model: {LIGHT_MODEL_NAME}...")
    try:
        light_pipeline = pipeline("sentiment-analysis", model=LIGHT_MODEL_NAME)
        print("Light model loaded successfully.")
    except Exception as e:
        print(f"Error loading light model: {e}")
        SENTIMENT_MODE = "generative" # Fallback

def analyze_sentiment(title):
    """Analyze news sentiment using the selected mode."""
    if SENTIMENT_MODE == "light" and light_pipeline:
        return analyze_sentiment_light(title)
    else:
        return analyze_sentiment_generative(title)


def analyze_sentiment_generative(title):
    """Analyze news sentiment using LLM."""
    prompt = f"Analyze the sentiment of this stock news title: \"{title}\". Respond with exactly one word: BULLISH, BEARISH, or NEUTRAL."
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        sentiment = response.choices[0].message.content.strip().upper()
        if "BULLISH" in sentiment: return "BULLISH"
        if "BEARISH" in sentiment: return "BEARISH"
        return "NEUTRAL"
    except Exception as e:
        print(f"Error analyzing sentiment (generative) for '{title}': {e}")
        return "NEUTRAL"


def analyze_sentiment_light(title):
    """Analyze news sentiment using a light-weight transformer model."""
    try:
        results = light_pipeline(title)
        if not results:
            return "NEUTRAL"
        
        # Mapping for lxyuan/distilbert-base-multilingual-cased-sentiments-student
        # Typically returns: positive, negative, neutral
        label = results[0]['label'].lower()
        if "positive" in label: return "BULLISH"
        if "negative" in label: return "BEARISH"
        return "NEUTRAL"
    except Exception as e:
        print(f"Error analyzing sentiment (light) for '{title}': {e}")
        return "NEUTRAL"


def search_news(ticker, time_range='7d'):
    regions = [
        ('en', 'US', 'English - US'),
        ('en', 'ID', 'English - Indonesia'),
        ('id', 'ID', 'Bahasa Indonesia'),
        ('id', 'US', 'Bahasa Indonesia - US'),
    ]

    all_entries = []
    seen_titles = set()

    for lang, country, region_name in regions:
        try:
            gn = GoogleNews(lang=lang, country=country)
            results = gn.search(ticker, when=time_range)
            entries = results.get('entries', [])

            for entry in entries:
                title = entry.get('title', '').strip()
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    published = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M')
                        except:
                            published = entry.get('published', 'N/A')

                    all_entries.append({
                        'title': title,
                        'link': entry.get('link', '#'),
                        'source': entry.get('author', entry.get('source', {}).get('title', 'Unknown')),
                        'published': published,
                        'region': region_name,
                        'lang': lang,
                        'country': country,
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error searching {region_name}: {e}")
            continue

    all_entries.sort(key=lambda x: x['published'] or '', reverse=True)
    return all_entries


@app.route('/')
def index():
    return render_template('index.html', sentiment_enabled=SENTIMENT_ANALYSIS_ENABLED)


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    ticker = data.get('ticker', '').strip()

    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400

    time_range = data.get('time_range', '7d')

    try:
        print(f"Searching news for ticker: {ticker}...")
        results = search_news(ticker, time_range)
        print(f"Found {len(results)} articles.")
        
        return jsonify({
            'ticker': ticker,
            'count': len(results),
            'results': results
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    title = data.get('title', '').strip()
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    print(f"--- Communicating with LLM for: {title[:50]}...")
    sentiment = analyze_sentiment(title)
    print(f"--- Sentiment: {sentiment}")
    
    return jsonify({'sentiment': sentiment})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
