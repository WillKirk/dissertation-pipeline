from flask import Blueprint, request, jsonify
import subprocess
import os
from app import db
from app.models import File

files_bp = Blueprint("files", __name__, url_prefix="/files")


@files_bp.route("/upload", methods=["POST"])
def upload_file():
    data = request.get_json()
    filename = data.get("filename")
    uploaded_by = data.get("user_id")

    file_record = File(filename=filename, uploaded_by=uploaded_by)
    db.session.add(file_record)
    db.session.commit()

    return jsonify({"message": "File record created", "id": file_record.id}), 201


@files_bp.route("/process", methods=["POST"])
def process_file():
    data = request.get_json()
    filename = data.get("filename")

    result = subprocess.run(
        "file " + filename,
        shell=True,
        capture_output=True,
        text=True
    )

    return jsonify({
        "filename": filename,
        "output": result.stdout,
        "error": result.stderr
    }), 200


@files_bp.route("/list", methods=["GET"])
def list_files():
    files = File.query.all()
    return jsonify([{
        "id": f.id,
        "filename": f.filename,
        "uploaded_by": f.uploaded_by
    } for f in files]), 200


@files_bp.route("/delete/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file_record = File.query.get(file_id)
    if not file_record:
        return jsonify({"error": "File not found"}), 404

    db.session.delete(file_record)
    db.session.commit()
    return jsonify({"message": "File deleted successfully"}), 200