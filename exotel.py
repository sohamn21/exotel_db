from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB (Atlas or local)
client = MongoClient("mongodb+srv://techno899:Sohamns21@cluster0ex.tbr0kn7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0ex")
db = client["nektech_db"]
collection = db["callers"]

@app.route("/save-caller", methods=["GET", "POST"])
def save_caller():
    # Exotel may send GET or POST, handle both
    if request.method == "POST":
        caller_number = request.form.get("From")
    else:
        caller_number = request.args.get("From")

    if caller_number:
        # Check if already saved
        existing = collection.find_one({"number": caller_number})
        if not existing:
            collection.insert_one({"number": caller_number})
            return "Number saved successfully", 200
        else:
            return "Number already exists", 200
    else:
        return "Caller number not found in request", 400

if __name__ == "__main__":
    app.run(port=5000)
