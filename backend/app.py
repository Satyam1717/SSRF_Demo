from flask import Flask, request, jsonify, Response 
import mysql.connector
import requests
import time

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host="db",
                user="labuser",
                password="labpassword",
                database="ssrflab"
            )
            return conn
        except mysql.connector.Error as err:
            retries -= 1
            time.sleep(2)
    return None

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "username": user['username']}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/posts', methods=['GET', 'POST'])
def manage_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO posts (username, title, content, url) VALUES (%s, %s, %s, %s)",
            (data['username'], data['title'], data['content'], data.get('url', ''))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Post created successfully"}), 201

    if request.method == 'GET':
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()
        conn.close()
        return jsonify(posts), 200

@app.route('/api/preview', methods=['GET'])
def preview_url():
    url = request.args.get('url')
    if not url:
        return "URL is required", 400
    
    # VULNERABILITY: Fetching external resources without validation
    try:
        response = requests.get(url, timeout=5)
        # We return the raw content and headers so the iframe can render it as a webpage
        return Response(
            response.content, 
            status=response.status_code, 
            content_type=response.headers.get('Content-Type', 'text/html')
        )
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)