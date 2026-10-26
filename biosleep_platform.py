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
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM sensor_data")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE dna_status='NORMAL'")
    normal = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE dna_status='WARNING'")
    warning = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE dna_status='CRITICAL'")
    critical = cur.fetchone()[0]

    cur.execute("SELECT AVG(temperature) FROM sensor_data")
    avg_temperature = cur.fetchone()[0]

    cur.execute("SELECT MAX(microbial_index) FROM sensor_data")
    max_microbe = cur.fetchone()[0]

    cur.execute("""
        SELECT temperature, microbial_index, dna_status, timestamp
        FROM sensor_data
        ORDER BY rowid DESC
        LIMIT 1
    """)
    latest = cur.fetchone()

    conn.close()

    if latest:
        latest_temp, latest_microbe, latest_status, latest_time = latest
    else:
        latest_temp, latest_microbe, latest_status, latest_time = 0, 0, "NO DATA", "-"

    status_class = latest_status.lower()

    html = """
<!DOCTYPE html>
<html>
<head>
<title>BioSleep OS - Analytics</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #071525;
    color: white;
}

.header {
    text-align: center;
    padding: 30px 20px 20px;
}

.header h1 {
    margin: 0;
    color: #00e5ff;
    font-size: 38px;
}

.header p {
    color: #b8c7d9;
    font-size: 18px;
}

.container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 20px;
}

.card {
    background: #142b45;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.card h3 {
    margin-top: 0;
    color: #b8c7d9;
    font-size: 17px;
}

.value {
    font-size: 34px;
    font-weight: bold;
    margin-top: 12px;
}

.normal {
    color: #00ff99;
}

.warning {
    color: #ffd166;
}

.critical {
    color: #ff5c5c;
}

.latest {
    margin-top: 25px;
}

.latest-box {
    background: #10243b;
    border-left: 5px solid #00e5ff;
    border-radius: 15px;
    padding: 25px;
    font-size: 18px;
    line-height: 2;
}

.footer {
    text-align: center;
    color: #8193a8;
    margin-top: 35px;
    padding-bottom: 25px;
}
</style>
<meta http-equiv="refresh" content="2">
</head>

<body>

<div class="header">
    <h1>BIOSLEEP OS</h1>
    <p>Passive Thermal Defense Operating System — Analytics</p>
</div>

<div class="container">

<div class="grid">

<div class="card">
    <h3>Total Sensor Readings</h3>
    <div class="value">{{TOTAL}}</div>
</div>

<div class="card">
    <h3>Average Temperature</h3>
    <div class="value">{{AVG}} °C</div>
</div>

<div class="card">
    <h3>Highest Microbial Index</h3>
    <div class="value">{{MAXMICROBE}}</div>
</div>

<div class="card">
    <h3>Normal Events</h3>
    <div class="value normal">{{NORMAL}}</div>
</div>

<div class="card">
    <h3>Warning Events</h3>
    <div class="value warning">{{WARNING}}</div>
</div>

<div class="card">
    <h3>Critical Events</h3>
    <div class="value critical">{{CRITICAL}}</div>
</div>

</div>

<div class="latest">

<div class="card">
    <h2>Latest Sensor Reading</h2>

    <div class="latest-box">
        <b>Temperature:</b> {{LATEST_TEMP}} °C<br>
        <b>Microbial Index:</b> {{LATEST_MICROBE}}<br>
        <b>DNA Status:</b>
        <span class="{{STATUS_CLASS}}"><b>{{LATEST_STATUS}}</b></span><br>
        <b>Timestamp:</b> {{LATEST_TIME}}
    </div>

</div>

</div>

<div class="footer">
    BioSleep OS • Passive Thermal Defense Monitoring
</div>

</div>

</body>
</html>
"""

    html = html.replace("{{TOTAL}}", str(total))
    html = html.replace("{{AVG}}", str(round(avg_temperature, 2) if avg_temperature else 0))
    html = html.replace("{{MAXMICROBE}}", str(max_microbe or 0))
    html = html.replace("{{NORMAL}}", str(normal))
    html = html.replace("{{WARNING}}", str(warning))
    html = html.replace("{{CRITICAL}}", str(critical))
    html = html.replace("{{LATEST_TEMP}}", str(latest_temp))
    html = html.replace("{{LATEST_MICROBE}}", str(latest_microbe))
    html = html.replace("{{LATEST_STATUS}}", str(latest_status))
    html = html.replace("{{LATEST_TIME}}", str(latest_time))
    html = html.replace("{{STATUS_CLASS}}", status_class)

    return html


@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT temperature, microbial_index, dna_status FROM sensor_data ORDER BY rowid DESC LIMIT 1")
    latest = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM sensor_data")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE microbial_index < 50")
    normal = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE microbial_index >= 50 AND microbial_index < 80")
    warning = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE microbial_index >= 80")
    critical = cur.fetchone()[0]

    conn.close()

    temperature = latest[0] if latest else 0
    microbial_index = latest[1] if latest else 0

    if microbial_index >= 80 or temperature >= 50:
        status = "CRITICAL"
    elif microbial_index >= 50 or temperature >= 40:
        status = "WARNING"
    else:
        status = "NORMAL"

    return f"""
    <html>
    <head>
    <meta http-equiv="refresh" content="2">
        <title>BioSleep OS</title>
        <style>
            body {{
                font-family: Arial;
                background: #0b132b;
                color: white;
                text-align: center;
                padding: 40px;
            }}
            h1 {{ color: #00e5ff; }}
            .card {{
                display: inline-block;
                background: #1c2541;
                padding: 25px;
                margin: 15px;
                border-radius: 15px;
                min-width: 180px;
            }}
            .critical {{ color: #ff4d4d; }}
            .warning {{ color: orange; }}
            .normal {{ color: #00ff99; }}
        </style>
    </head>

    <body>
        <h1>BIOSLEEP OS</h1>
        <h2>Passive Thermal Defense Operating System</h2>

        <div class="card">
            <h3>Temperature</h3>
            <h2>{temperature} °C</h2>
        </div>

        <div class="card">
            <h3>Microbial Index</h3>
            <h2>{microbial_index}</h2>
        </div>

        <div class="card">
            <h3>System Status</h3>
            <h2 class="{'critical' if status == 'CRITICAL' else 'warning' if status == 'WARNING' else 'normal'}">{status}</h2>
        </div>

        <div class="card">
            <h3>Total Readings</h3>
            <h2>{total}</h2>
        </div>

        <div class="card">
            <h3>Normal Events</h3>
            <h2 class="normal">{normal}</h2>
        </div>

        <div class="card">
            <h3>Warning Events</h3>
            <h2 class="warning">{warning}</h2>
        </div>

        <div class="card">
            <h3>Critical Events</h3>
            <h2 class="critical">{critical}</h2>
        </div>

        <h2 class="critical">
            {'⚠ CRITICAL GENETIC MUTATION DETECTED!' if status == 'CRITICAL' else 'SYSTEM STATUS: ' + status}
        </h2>

    </body>
    </html>
    """
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
