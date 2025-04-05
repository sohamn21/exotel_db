from flask import Flask, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection (Atlas URI from Render env var)
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["nektech_db"]
collection = db["callers"]

@app.route("/save-caller", methods=["POST", "GET"])
def save_caller():
    if request.method == "GET":
        return "GET not allowed here. Use POST only.", 405

    print("Received POST data:", request.form)

    caller_number = request.form.get("From")  # This is the key Exotel should send

    if caller_number:
        if not collection.find_one({"number": caller_number}):
            collection.insert_one({"number": caller_number})
            print(f"Number {caller_number} saved")
            return "Number saved successfully", 200
        else:
            print(f"Number {caller_number} already exists")
            return "Number already exists", 200
    else:
        print("Caller number not found in request")
        return "Caller number not found in request", 400

@app.route("/", methods=["GET"])
def home():
    return "Nektech IVR API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
