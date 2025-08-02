from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os, sys

from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to my application"

@app.route("/train")
def train_route():
    try:
        print(">>> /train endpoint called")
        lg.info(">>> /train endpoint called")
        
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        print(">>> Training completed successfully.")
        lg.info(">>> Training completed successfully.")

        return "Training Completed."
    except Exception as e:
        print(">>> Exception occurred in /train:", str(e))
        lg.error(">>> Exception occurred in /train: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_detail = prediction_pipeline.run_pipeline()

            lg.info(">>> Prediction completed. Sending prediction file.")

            return send_file(
                prediction_file_detail.prediction_file_path,
                download_name=prediction_file_detail.prediction_file_name,
                as_attachment=True
            )
        else:
            return render_template('upload_file.html')
    except Exception as e:
        print(">>> Exception occurred in /predict:", str(e))
        lg.error(">>> Exception occurred in /predict: %s", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(">>> Starting Flask server on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
