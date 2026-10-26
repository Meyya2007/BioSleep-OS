import re

file = "biosleep_platform.py"

with open(file, "r") as f:
    code = f.read()

new_dashboard = r'''@app.route("/")
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

    if microbial_index >= 80:
        status = "CRITICAL"
    elif microbial_index >= 50:
        status = "WARNING"
    else:
        status = "NORMAL"

    return f"""
    <html>
    <head>
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

'''

pattern = r'@app\.route\("/"\)\s*def dashboard\(\):.*?(?=\nif __name__ == "__main__":)'

code = re.sub(pattern, new_dashboard.rstrip(), code, flags=re.S)

with open(file, "w") as f:
    f.write(code)

print("Dashboard updated successfully!")
