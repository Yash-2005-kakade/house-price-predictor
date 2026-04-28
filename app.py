from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("model.pkl")

EXPECTED_COLUMNS = [
    "house_size_sqft",
    "num_bedrooms",
    "age_of_house_years",
    "location",
    "house_type",
    "condition",
    "furnishing"
]

# 🔹 Serve frontend
@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")

# 🔹 Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        missing = [col for col in EXPECTED_COLUMNS if col not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_price_usd": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Run for deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)