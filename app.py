
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ai_engine import analyze_video, find_highlights, create_clip
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "ClipGenius AI Backend is Running!"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video uploaded"}), 400

        video = request.files["video"]

        if video.filename == "":
            return jsonify({"error": "No video selected"}), 400

        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        result = analyze_video(video_path)

        return jsonify({
            "success": True,
            "analysis": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/find-highlights", methods=["POST"])
def find_video_highlights():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video uploaded"}), 400

        video = request.files["video"]

        if video.filename == "":
            return jsonify({"error": "No video selected"}), 400

        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        highlights = find_highlights(video_path)

        generated_clips = []

        for index, moment in enumerate(highlights, start=1):
            start = float(moment["start"])
            end = float(moment["end"])

            output_filename = f"smart_clip_{index}.mp4"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)

            create_clip(video_path, start, end, output_path)

            generated_clips.append({
                "title": moment["title"],
                "start": start,
                "end": end,
                "reason": moment["reason"],
                "video_url": f"http://127.0.0.1:5001/clips/{output_filename}"
            })

        return jsonify({
            "success": True,
            "clips": generated_clips
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
@app.route("/clips/<filename>")
def serve_clip(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
