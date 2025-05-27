from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fabric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    uploaded_by = db.Column(db.String(50), nullable=True)
