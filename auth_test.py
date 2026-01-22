import os
import json
import base64
import gspread
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from oauth2client.service_account import ServiceAccountCredentials

print("🐝 Starting Smart Beehive App...")

app = Flask(__name__)
CORS(app)

# ---------------- AUTH ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

try:
    if "GOOGLE_SERVICE_ACCOUNT_B64" in os.environ:
        print("🔐 Using Render credentials")
        json_str = base64.b64decode(
            os.environ["GOOGLE_SERVICE_ACCOUNT_B64"]
        ).decode("utf-8")
        service_account_info = json.loads(json_str)
    else:
        print("🔐 Using local credentials")
        with open("service_account.json", "r") as f:
            service_account_info = json.load(f)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        service_account_info, scope
    )
    client = gspread.authorize(creds)
    print("✅ Google authentication successful")

except Exception as e:
    print("❌ Auth Error:", e)
    raise e

# ---------------- SHEET ----------------
SHEET_ID = "1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo"

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    print("✅ Google Sheet connected")
except Exception as e:
    print("❌ Sheet Error:", e)
    raise e

# ---------------- ROUTES ----------------
@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/data")
def data():
    try:
        rows = sheet.get_all_values()

        # If only header exists
        if len(rows) < 2:
            return jsonify({"error": "No data available"})

        latest = rows[-1]

        return jsonify({
            "timestamp": latest[0] if len(latest) > 0 else "",
            "hive_id": latest[1] if len(latest) > 1 else "",
            "status": latest[2] if len(latest) > 2 else "",
            "temperature": latest[3] if len(latest) > 3 else "",
            "humidity": latest[4] if len(latest) > 4 else "",
            "weight1": latest[5] if len(latest) > 5 else "",
            "weight2": latest[6] if len(latest) > 6 else "",
            "total_weight": latest[7] if len(latest) > 7 else "",
            "latitude": latest[8] if len(latest) > 8 else "",
            "longitude": latest[9] if len(latest) > 9 else ""
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
