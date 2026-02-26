from flask import Flask, request, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
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
    original_url = data.get("url")

    return jsonify({
        "message": "URL received",
        "original_url": original_url
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)