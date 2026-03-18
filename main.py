# app.py
from flask import Flask, request, jsonify
import os
from flask_pymongo import PyMongo
from bson import ObjectId
import uuid
from datetime import datetime

app = Flask(__name__)

mongo_host = os.environ.get("MONGO_URL", "localhost")
app.config["MONGO_URI"] = f"mongodb://{mongo_host}:27017/post_db"

mongo = PyMongo(app)

def validate_uuid(u):
    try:
        uuid.UUID(str(u))
        return True
    except Exception:
        return False

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    message = data.get("message")
    user_id = data.get("user_id")

    if not title or not message or not user_id:
        return jsonify({"error": "Title, message, and user_id are required."}), 400

    if not validate_uuid(user_id):
        return jsonify({"error": "user_id must be a valid UUID string."}), 400

    post = {
        "title": title,
        "message": message,
        "user_id": str(user_id),
        "created_at": datetime.now(),
        "post_id": str(uuid.uuid4())
    }

    res = mongo.db.posts.insert_one(post)
    return jsonify({
        "message": "Post created successfully.",
        "post_id": post["post_id"],
        "mongo_id": str(res.inserted_id)
    }), 201

@app.route("/posts", methods=["GET"])
def get_posts():
    posts_cursor = mongo.db.posts.find().sort("created_at", -1)
    result = []
    for p in posts_cursor:
        p_out = {
            "mongo_id": str(p.get("_id")),
            "post_id": p.get("post_id"),
            "title": p.get("title"),
            "message": p.get("message"),
            "user_id": p.get("user_id"),
            "created_at": p.get("created_at").isoformat() if p.get("created_at") else None
        }
        result.append(p_out)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)