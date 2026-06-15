"""
app.py — Flask backend for Project Dashboard.
Run:  python app.py
Then open:  http://localhost:5000
"""
import os
from flask import Flask, render_template, jsonify
from pdf_parser import load_all_pdfs, compute_metrics

app = Flask(__name__)

# Default: ./pdfs  |  Override: set PDF_FOLDER env variable to any path
PDF_FOLDER = os.environ.get("PDF_FOLDER", "pdfs")


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/data")
def api_data():
    try:
        raw   = load_all_pdfs(PDF_FOLDER)
        stats = compute_metrics(raw)
        return jsonify({"success": True, "data": stats, "pdf_folder": PDF_FOLDER})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "pdf_folder": PDF_FOLDER})


if __name__ == "__main__":
    print(f"Reading PDFs from: {os.path.abspath(PDF_FOLDER)}")
    print("Dashboard -> http://localhost:5000")
    app.run(debug=True, port=5000)
