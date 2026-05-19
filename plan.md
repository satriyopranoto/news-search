# News Search by Ticker - Plan

## Overview
Flask webapp untuk search berita berdasarkan ticker stock yang diberikan user menggunakan `pygooglenews` sebagai interface ke Google News RSS.

## Tech Stack
- **Backend**: Flask
- **News API**: pygooglenews (RSS-based, no API key required)
- **Frontend**: HTML + Bootstrap 5 (CDN)

## Fitur Utama
1. Input form untuk ticker (contoh: AAPL, BBCA, GOTO)
2. Ambil berita dari 4 kombinasi region/language:
   - `en` + `US` (English - US)
   - `en` + `ID` (English - Indonesia)
   - `id` + `ID` (Bahasa Indonesia)
   - `id` + `US` (Bahasa Indonesia - US)
3. Tampilkan hasil berita dengan:
   - Judul berita (link ke sumber)
   - Tanggal publikasi
   - Sumber/Publisher
   - Deskripsi singkat

## Project Structure
```
newssearch/
├── app.py              # Flask app utama
├── templates/
│   └── index.html      # Frontend HTML
├── requirements.txt    # Dependencies
└── README.md
```

## Dependencies
- flask
- pygooglenews>=0.1.3
- feedparser (dependency pygooglenews)

## API / Flow
1. User input ticker di form
2. Loop 4 kombinasi (lang, country)
3. Untuk masing-masing: `gn.search(ticker)`
4. Combine & deduplicate hasil
5. Render ke template

## Default Time Range
- `when='7d'` (7 hari terakhir)

## Running
```bash
pip install -r requirements.txt
python app.py
# Buka http://127.0.0.1:5000
```
