from flask import Flask, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# ---------------- AUTH ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)

client = gspread.authorize(creds)

# ---------------- OPEN SHEET ----------------
SHEET_ID = "1gjlu4F-iNqhjrT57mpU7vGQOgXtjMer6i2Z3dDRbrFo"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route("/data")
def get_latest_data():
    rows = sheet.get_all_values()

    if len(rows) < 2:
        return jsonify({"error": "No data found"})

    latest = rows[-1]

    return jsonify({
        "timestamp": latest[0],
        "hive_id": latest[1],
        "status": latest[2],
        "temperature": latest[3],
        "humidity": latest[4],
        "weight1": latest[5],
        "weight2": latest[6],
        "total_weight": latest[7],
        "latitude": latest[8],
        "longitude": latest[9]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
