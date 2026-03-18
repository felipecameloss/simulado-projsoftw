import uuid
from db import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
