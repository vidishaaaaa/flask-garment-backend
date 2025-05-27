from models import db, Fabric
from app import app

with app.app_context():
    records = Fabric.query.all()
    for record in records:
        print(f"ID: {record.id}, Filename: {record.filename}, Uploaded By: {record.uploaded_by}")
