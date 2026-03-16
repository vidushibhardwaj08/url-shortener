from flask import Flask, request, jsonify, redirect
import sqlite3
import random
import string
from urllib.parse import urlparse

app = Flask(__name__)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "URL Shortener is running!"

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    # Validate input
    if not data or "url" not in data:
        return jsonify({"error":"URL is required"}), 400
    
    original_url = data.get("url")

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Connect to database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Generate unique short code
    while True:
        short_code = generate_short_code()

        cursor.execute(
            "SELECT id FROM urls WHERE short_code = ?",
            (short_code,)
        )

        existing = cursor.fetchone()

        if not existing:
            break


    try:
        cursor.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, short_code)
        )

        conn.commit()
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Short code collision occurred"}), 500
    
    finally:
        conn.close()

    short_url = f"http://127.0.0.1:5000/{short_code}"
    
    return jsonify({
    "original_url": original_url,
    "short_code": short_code,
    "short_url": short_url
    }), 201

@app.route("/stats/<short_code>")
def get_stats(short_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url, clicks FROM urls WHERE short_code = ?",
        (short_code,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        original_url = result[0]
        clicks = result[1]

        return jsonify({
            "short_code": short_code,
            "original_url":original_url,
            "clicks":clicks
        })
    
    else:
        return jsonify({"error": "Short URL not found"}), 404

@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url, clicks FROM urls WHERE short_code = ?",
        (short_code,)
    )

    result = cursor.fetchone()
    
    if result:
        original_url = result[0]

        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )

        conn.commit()
        conn.close()

        return redirect(original_url)
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)