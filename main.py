from flask import Flask, request, jsonify
from db import db
from models import Post
import os
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo_url = os.environ['MONGO_URL']

app.config["MONGO_URI"] = f"mongodb://${mongo_url:localhost}:27017/post_db"

mongo = PyMongo(app)

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    title = data.get("title")
    message = data.get("message")
    user_id = data.get("user_id")

    if not title or not message or not user_id:
        return jsonify({"error": "Title, message, and user_id are required."}), 400

    post = Post(title=title, message=message, user_id=user_id)
    mongo.db.posts.insert_one(post.__dict__)

    return jsonify({"message": "Post created successfully.", "post_id": str(post.id)}), 201

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = mongo.db.posts.find()
    result = []
    for post in posts:
        post["_id"] = str(post["_id"])
        result.append(post)
    return jsonify(result), 200