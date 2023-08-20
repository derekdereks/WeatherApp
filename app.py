import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/weather")
def get_weather():
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?hourly=temperature_2m&latitude=38.8951&longitude=-77.0364"
    )
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Cannot fetch weather data"}), 500


if __name__ == "__main__":
    app.run(port=5000)
