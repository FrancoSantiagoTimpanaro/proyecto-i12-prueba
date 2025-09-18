from flask import Flask, render_template, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    "host": "aws-1-us-east-2.pooler.supabase.com",
    "database": "postgres",
    "user": "postgres.aibvvfplsvhmrkavxyth",   # cambiar por tu usuario
    "password": "i12pass"  # cambiar por tu contraseña
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Crear tabla si no existe
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        intersection VARCHAR(255),
        lat FLOAT,
        lng FLOAT
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

# Ruta principal
@app.route("/")
def index():
    return render_template("frontend.html")  # tu HTML con Leaflet

# Obtener todas las ubicaciones
@app.route("/locations")
def get_locations():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(locations)

# Agregar nueva ubicación
@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.get_json()
    name = data.get("name")
    intersection = data.get("intersection")
    lat = data.get("lat")
    lng = data.get("lng")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO locations (name, intersection, lat, lng) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, intersection, lat, lng)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "added": {"id": new_id, "name": name, "intersection": intersection, "lat": lat, "lng": lng}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)