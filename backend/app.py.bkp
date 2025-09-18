from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        conn = psycopg2.connect(
            host="postgres",
            dbname="i12db",
            user="i12user",
            password="i12pass"
        )
        conn.close()
        return "Hello from Flask! ✅ Connected to Postgres"
    except Exception as e:
        return f"Error connecting to Postgres: {e}"