
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename  # <-- to safely save uploaded files
from main import apply_fabric_to_garment
from models import db, Fabric

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

UPLOAD_FOLDER = "uploads"
ASSETS_FOLDER = "assets"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/apply-fabric", methods=["POST"])
def apply_fabric():
    print("FILES RECEIVED:", request.files)
    print("FORM RECEIVED:", request.form)

    fabric_file = request.files.get("fabric")
    garment_name = request.form.get("garment")  # e.g., "wts.png"

    print("Received file:", fabric_file)
    print("Received garment:", garment_name)

    if not fabric_file or not garment_name:
        return jsonify({"error": "Missing fabric image or garment name"}), 400

    # Secure filename to avoid directory traversal attacks
    safe_filename = secure_filename(fabric_file.filename)
    if safe_filename == '':
        return jsonify({"error": "Invalid fabric filename"}), 400

    # Save fabric image to uploads folder
    fabric_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    try:
        fabric_file.save(fabric_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save fabric image: {str(e)}"}), 500

    # Compose paths for garment & output
    garment_path = os.path.join(ASSETS_FOLDER, garment_name)
    output_file = f"{os.path.splitext(safe_filename)[0]}_on_{garment_name}.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_file)

    try:
        # Call your image processing function
        result_path = apply_fabric_to_garment(garment_path, fabric_path, output_path)
        
        # Save record to database
        record = Fabric(filename=safe_filename, uploaded_by="User1")
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

    # Return output image URL (adjust if needed)
    return jsonify({"message": "✅ Success", "output": f"/output/{os.path.basename(result_path)}"})

@app.route("/fabrics", methods=["GET"])
def get_fabrics():
    fabrics = Fabric.query.all()
    return jsonify([
        {"id": f.id, "filename": f.filename, "uploaded_by": f.uploaded_by}
        for f in fabrics
    ])

@app.route("/output/<filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensures tables are created
    app.run(host="0.0.0.0", debug=True, port=5000)

