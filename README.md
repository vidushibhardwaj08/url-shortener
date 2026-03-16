# URL Shortener Service

A RESTful URL shortener built using Python, Flask, and SQLite.

## Features

- Generate short URLs
- Redirect short URLs to original URLs
- Collision-safe short code generation
- URL validation
- Click tracking
- Analytics endpoint

## Tech Stack

- Python
- Flask
- SQLite

## API Endpoints

### Create Short URL

POST /shorten

Request:
{
"url": "https://google.com"
}

Response:
{
"original_url": "https://google.com",
"short_code": "Ab12Xy",
"short_url": "http://127.0.0.1:5000/Ab12Xy"
}

### Redirect

GET /<short_code>

### Analytics

GET /stats/<short_code>

Example response:
{
"short_code": "Ab12Xy",
"original_url": "https://google.com",
"clicks": 5
}

## Run Locally

Install dependencies:

pip install -r requirements.txt

Run the server:

python app.py
