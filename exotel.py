from flask import Flask, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection (can use Atlas)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["nektech_db"]
collection = db["callers"]

@app.route("/save-caller", methods=["POST"])
def save_caller():
    caller_number = request.form.get("From")  # Exotel sends this field
    
    if caller_number:
        if not collection.find_one({"number": caller_number}):
            collection.insert_one({"number": caller_number})
            return "Number saved successfully", 200
        else:
            return "Number already exists", 200
    else:
        return "Caller number not found in request", 400

@app.route("/", methods=["GET"])
def home():
    return "Nektech IVR API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
