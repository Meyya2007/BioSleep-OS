from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "biosleep.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            microbial_index INTEGER,
            dna_status TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/sensor", methods=["POST"])
def receive_sensor():
    data = request.json

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = data.get("temperature")
    microbial_index = data.get("microbial_index")
    dna_status = data.get("dna_status")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data
        (timestamp, temperature, microbial_index, dna_status)
        VALUES (?, ?, ?, ?)
    """, (timestamp, temperature, microbial_index, dna_status))

    conn.commit()
    conn.close()

    print("\n[BIO PLATFORM] DATA STORED")
    print("Time            :", timestamp)
    print("Temperature     :", temperature)
    print("Microbial Index :", microbial_index)
    print("DNA Status      :", dna_status)

    return jsonify({"status": "stored"})


@app.route("/analytics", methods=["GET"])
def analytics():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sensor_data")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_data WHERE dna_status='NORMAL'"
    )
    normal = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_data WHERE dna_status='WARNING'"
    )
    warning = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM sensor_data WHERE dna_status='CRITICAL'"
    )
    critical = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(temperature) FROM sensor_data")
    avg_temperature = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(microbial_index) FROM sensor_data")
    max_microbe = cursor.fetchone()[0]

    cursor.execute("""
        SELECT temperature, microbial_index, dna_status
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
    """)
    latest = cursor.fetchone()

    conn.close()

    return jsonify({
        "total_readings": total,
        "normal_events": normal,
        "warning_events": warning,
        "critical_events": critical,
        "average_temperature": round(avg_temperature, 2)
            if avg_temperature else 0,
        "highest_microbial_index": max_microbe or 0,
        "latest": {
            "temperature": latest[0],
            "microbial_index": latest[1],
            "status": latest[2]
        } if latest else None
    })


@app.route("/")
def dashboard():
    return """
    <html>
    <head>
        <title>BioSleep OS</title>
        <style>
            body {
                font-family: Arial;
                background: #0b132b;
                color: white;
                text-align: center;
                padding: 40px;
            }
            h1 { color: #00e5ff; }
            .card {
                display: inline-block;
                background: #1c2541;
                padding: 25px;
                margin: 15px;
                border-radius: 15px;
                min-width: 180px;
            }
            .critical { color: #ff4d4d; }
            .normal { color: #00ff99; }
        </style>
    </head>
    <body>
        <h1>BIOSLEEP OS</h1>
        <h2>Passive Thermal Defense Operating System</h2>

        <div class="card">
            <h3>Temperature</h3>
            <h2>37.7 °C</h2>
        </div>

        <div class="card">
            <h3>Microbial Index</h3>
            <h2>92</h2>
        </div>

        <div class="card">
            <h3>System Status</h3>
            <h2 class="critical">CRITICAL</h2>
        </div>

        <div class="card">
            <h3>Total Readings</h3>
            <h2>10</h2>
        </div>

        <div class="card">
            <h3>Normal Events</h3>
            <h2 class="normal">6</h2>
        </div>

        <div class="card">
            <h3>Warning Events</h3>
            <h2>2</h2>
        </div>

        <div class="card">
            <h3>Critical Events</h3>
            <h2 class="critical">2</h2>
        </div>

        <h2 class="critical">⚠ CRITICAL GENETIC MUTATION DETECTED!</h2>

    </body>
    </html>
    """
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
