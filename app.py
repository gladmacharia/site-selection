import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
db_url = os.getenv("DB_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
@app.route('/')
def home():
    return render_template('index.html')


def home():

    return "Welcome to the Smart Site Selection API for Nairobi! Use the endpoints to access healthcare facilities and road network data."

@app.route('/api/nearest_hospital/<lat>/<lon>')
def nearest_hospital(lat,lon):
    try:
        flat = float(lat)
        flon = float(lon)
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT name, amenity_type,
        ST_Distance(geometry::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) as distance_m,
        ST_Y(ST_Centroid(geometry)) as hospital_lat,
        ST_X(ST_Centroid(geometry)) as hospital_lon
        FROM healthcare_facilities

        ORDER BY geometry <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
        LIMIT 1;
    """
        cursor.execute(query, (flon, flat, flon, flat))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            hosp_name = str(result[0])
            hosp_type = str(result[1])
            dist = float(result[2])
            hosp_lat = float(result[3])
            hosp_lon = float(result[4])

            return jsonify(
                {
                    "status": "success",
                    "hospital_name" : hosp_name,
                    "type": hosp_type,
                    "distance_meters": round(dist, 2),
                    "hospital_latitude": hosp_lat,
                    "hospital_longitude": hosp_lon
                }
            )
        else:
            return jsonify({"status": "error", "message": "No hospital found."})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':

    app.run(debug=True, port=5000)