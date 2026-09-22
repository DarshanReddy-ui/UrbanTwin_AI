from flask import Flask, render_template, request, jsonify
from traffic_pipeline import analyze_traffic
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "dataset/test_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "trafficFile" not in request.files:
        return jsonify({
            "success": False,
            "message": "No file uploaded"
        })

    file = request.files["trafficFile"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        })

    extension = os.path.splitext(file.filename)[1]

    filename = str(uuid.uuid4()) + extension

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(file_path)

    try:

        result = analyze_traffic(file_path)

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })


@app.route("/health")
def health():

    return jsonify({
        "status": "UrbanTwin AI backend is running"
    })


if __name__ == "__main__":
    app.run(debug=True)