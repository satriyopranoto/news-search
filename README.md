# News Search with Sentiment Analysis

A Python Flask-based web application that aggregates stock/financial news from Google News across multiple regions (US, Indonesia) and provides optional sentiment analysis (Bullish, Bearish, or Neutral) for each news headline.

## Features

- **Multi-region News Search:** Fetches news using `pygooglenews` from US and Indonesian sources.
- **Sentiment Analysis Dashboard:** Evaluates headlines as Bullish, Bearish, or Neutral.
- **Toggleable Features:** Easily turn sentiment analysis on or off via configuration.
- **Multiple Sentiment Modes:**
  - **Generative Mode:** Uses Large Language Models (LLMs) via an OpenAI-compatible API (e.g., local Ollama with Llama 3.2 or OpenAI's GPT models).
  - **Light Mode:** Uses lightweight Hugging Face transformer models (e.g., `distilbert-base-multilingual-cased`) for faster, local inference without external LLM dependencies.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) (Optional, if using local Generative mode)

## Installation

1. **Clone the repository or navigate to the folder:**
   ```bash
   cd newssearch
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy the example environment file and update it according to your preferences.
   ```bash
   cp .env_example .env
   ```
   *Edit `.env` to configure the Sentiment Analysis mode and API keys.*

## Configuration (`.env`)

You can customize the application behavior by modifying the `.env` file:

- `SENTIMENT_ANALYSIS_ENABLED`: Set to `true` or `false` to toggle the sentiment analysis feature.
- `SENTIMENT_MODE`: Set to `generative` (for LLMs) or `light` (for transformers).
- `OPENAI_API_BASE`: The API base URL (e.g., `http://localhost:11434/v1` for local Ollama).
- `OPENAI_API_KEY`: Your API key (or `ollama` for local usage).
- `MODEL_NAME`: The name of the LLM to use (e.g., `llama3.2`).
- `LIGHT_MODEL_NAME`: The Hugging Face model identifier for light mode.

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5001
   ```

3. Enter a stock ticker symbol (e.g., `AAPL`, `BBCA`) and select a time range, then click "Search" to view the news and their sentiment analysis.
