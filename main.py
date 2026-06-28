import sqlite3
import pandas as pd
from datetime import datetime

df = pd.read_csv("hotel_bookings.csv")
conn = sqlite3.connect("hotel_bookings.db")
df.to_sql("bookings", conn, if_exists="replace", index=False)
print("Data loaded:", len(df), "rows")

checks = {
    "Null ADR (price) values": """
        SELECT COUNT(*) FROM bookings WHERE adr IS NULL
    """,
    "Duplicate bookings": """
        SELECT COUNT(*) FROM (
            SELECT reservation_status_date, hotel, arrival_date_year,
                   arrival_date_month, adults, COUNT(*) as cnt
            FROM bookings
            GROUP BY reservation_status_date, hotel,
                     arrival_date_year, arrival_date_month, adults
            HAVING cnt > 1
        )
    """,
    "Negative room price": """
        SELECT COUNT(*) FROM bookings WHERE adr < 0
    """,
    "Zero guests": """
        SELECT COUNT(*) FROM bookings
        WHERE adults = 0 AND children = 0 AND babies = 0
    """,
    "Invalid lead time": """
        SELECT COUNT(*) FROM bookings WHERE lead_time < 0
    """,
    "Room type mismatch": """
        SELECT COUNT(*) FROM bookings
        WHERE reserved_room_type != assigned_room_type
    """,
}

results = []
for check_name, query in checks.items():
    cursor = conn.execute(query)
    count = cursor.fetchone()[0]
    status = "FAIL" if count > 0 else "PASS"
    results.append({"check": check_name, "issues": count, "status": status})
    print(f"{'❌' if status == 'FAIL' else '✅'} {check_name}: {count} issues")

conn.close()

rows = ""
for r in results:
    color = "#ffe5e5" if r["status"] == "FAIL" else "#e5ffe5"
    rows += f"""
    <tr style="background:{color}">
        <td>{r['check']}</td>
        <td>{r['issues']}</td>
        <td>{'❌ FAIL' if r['status'] == 'FAIL' else '✅ PASS'}</td>
    </tr>"""

html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Hotel Booking Data Quality Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; background: #f9f9f9; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; background: white; }}
        th {{ background: #333; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
        .meta {{ color: #888; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>🏨 Hotel Booking Data Quality Report</h1>
    <p class="meta">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} |
    Dataset: hotel_bookings.csv | Total rows: {len(df)}</p>
    <table>
        <tr>
            <th>Check</th>
            <th>Issues Found</th>
            <th>Status</th>
        </tr>
        {rows}
    </table>
</body>
</html>"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Report saved as report.html")