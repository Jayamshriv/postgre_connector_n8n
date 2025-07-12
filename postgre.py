from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Fallback static niches
STATIC_NICHES = {
    'productivity_tools': {'avg_commission': 25, 'search_volume': 50000},
    'ai_software': {'avg_commission': 30, 'search_volume': 80000},
    'crypto_tools': {'avg_commission': 40, 'search_volume': 120000},
    'marketing_automation': {'avg_commission': 35, 'search_volume': 60000},
    'dev_tools': {'avg_commission': 20, 'search_volume': 40000}
}

@app.route("/top-niches")
def top_niches():
    try:
        conn = psycopg2.connect(
          'postgres://avnadmin:AVNS_hBv5Kw4EtMNgdR5NOQK@pg-30f45208-abarakadabara698-7bd8.j.aivencloud.com:10038/defaultdb?sslmode=require'
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT niche, AVG(affiliate_clicks) AS avg_clicks, AVG(conversion_rate) AS avg_conversion
            FROM performance
            WHERE created_at > NOW() - INTERVAL '7 days'
            GROUP BY niche
            ORDER BY AVG(affiliate_clicks) * AVG(conversion_rate) DESC
            LIMIT 3;
        """)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        if not rows:
            return jsonify({
                "source": "static",
                "data": STATIC_NICHES
            })

        result = [
            {"niche": row[0], "avg_clicks": row[1], "avg_conversion": row[2]}
            for row in rows
        ]

        return jsonify({
            "source": "database",
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")
