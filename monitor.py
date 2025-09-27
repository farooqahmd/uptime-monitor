import sqlite3
import requests
import time
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('uptime.db')
cursor = conn.cursor()

# Get all sites
cursor.execute("SELECT id, url FROM sites")
sites = cursor.fetchall()

# Check each site
for site_id, url in sites:
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        end = time.time()

        status_code = response.status_code
        is_up = response.ok
        response_time_ms = int((end - start) * 1000)
    except Exception as e:
        status_code = None
        is_up = False
        response_time_ms = None

    checked_at = datetime.utcnow().isoformat()

    # Insert log into uptime_logs
    cursor.execute("""
        INSERT INTO uptime_logs (site_id, status_code, is_up, response_time_ms, checked_at)
        VALUES (?, ?, ?, ?, ?)
    """, (site_id, status_code, is_up, response_time_ms, checked_at))

    print(f"[{checked_at}] {url} → {'UP ✅' if is_up else 'DOWN ❌'} ({response_time_ms} ms)")

# Save and close
conn.commit()
conn.close()