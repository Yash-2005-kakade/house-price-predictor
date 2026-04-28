from flask import Flask, request, jsonify, send_file
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
    return send_file("index.html")

# 🔹 Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate fields
        for col in EXPECTED_COLUMNS:
            if col not in data or data[col] is None:
                return jsonify({"error": f"Missing or invalid field: {col}"}), 400

        # Convert numeric
        data["house_size_sqft"] = float(data["house_size_sqft"])
        data["num_bedrooms"] = int(data["num_bedrooms"])
        data["age_of_house_years"] = int(data["age_of_house_years"])

        # Normalize text
        data["location"] = str(data["location"]).capitalize()
        data["house_type"] = str(data["house_type"]).capitalize()
        data["condition"] = str(data["condition"]).capitalize()
        data["furnishing"] = str(data["furnishing"]).replace("-", " ").title()

        # Predict
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_price_usd": float(prediction)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# 🔹 Run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
