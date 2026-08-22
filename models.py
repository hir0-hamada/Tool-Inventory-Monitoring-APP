from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tool(db.Model):
    # Added autoincrement=False to allow manual ID entry
    id = db.Column(db.String(50), primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.png')
    status = db.Column(db.String(20), nullable=False, default='Available')
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Tool {self.name}>'