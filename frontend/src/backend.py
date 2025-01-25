from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Connect to MongoDB using the credentials
client = MongoClient("mongodb+srv://arun:1234@cluster1.v5dye5b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["app"]

# Define collections
sellers_collection = db["sellers"]
items_collection = db["items"]

# Fetch seller profile by user_id
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    seller = sellers_collection.find_one({"seller_id": user_id})
    if seller:
        # Return profile info (exclude password for security)
        seller_data = {
            "name": seller["name"],
            "email": seller["email"],
            "contact_no": seller["contact_no"],
            "address": seller["address"],
            "logo": seller["logo"]
        }
        return jsonify(seller_data), 200
    else:
        return jsonify({"error": "Seller not found"}), 404

# Fetch items for the given seller
@app.route('/items/<int:user_id>', methods=['GET'])
def get_items(user_id):
    items = items_collection.find({"seller_id": user_id})
    items_list = []
    for item in items:
        items_list.append({
            "productName": item["productName"],
            "properties": item["properties"]
        })
    return jsonify(items_list), 200

# Add a new item for the given seller
@app.route('/add_item/<int:user_id>', methods=['POST'])
def add_item(user_id):
    new_item = request.json
    new_item["seller_id"] = user_id
    result = items_collection.insert_one(new_item)

    if result.inserted_id:
        return jsonify({"message": "Item added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add item"}), 500

if __name__ == '__main__':
    app.run(debug=True)
