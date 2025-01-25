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
bids_collection = db["bid"]
after_bid_collection = db["after_bid"]

# Route to fetch current bids
@app.route('/current_bids/<int:seller_id>', methods=['GET'])
def get_current_bids(seller_id):
    current_bids = list(after_bid_collection.find({"seller_id": seller_id, "accept": "no", "item_reached": "no"}))
    # Remove _id field from the response
    for bid in current_bids:
        bid["_id"] = str(bid["_id"])
    return jsonify(current_bids), 200

# Route to fetch available bids
@app.route('/available_bids', methods=['GET'])
def get_available_bids():
    available_bids = []
    bids = list(bids_collection.find())
    for bid in bids:
        # Check if this bid is already in the "after_bid" collection
        exists = after_bid_collection.find_one({"bid_id": bid["bid_id"]})
        if not exists:
            available_bids.append(bid)
    # Remove _id field from the response
    for bid in available_bids:
        bid["_id"] = str(bid["_id"])
    return jsonify(available_bids), 200

# Route to confirm a bid and move it to the "after_bid" table
@app.route('/confirm_bid', methods=['POST'])
def confirm_bid():
    data = request.json
    bid_id = data["bid_id"]
    price = data["price"]
    seller_id = data["seller_id"]
    
    # Check if the bid exists in the "bid" table
    bid = bids_collection.find_one({"bid_id": bid_id})
    
    if not bid:
        return jsonify({"error": "Bid not found"}), 404
    
    # Retrieve buyer_id from the bid
    buyer_id = bid['buyer_id']

    # Prepare data for the "after_bid" table
    after_bid_data = {
        "bid_id": bid_id,
        "price": price,
        "seller_id": seller_id,
        "buyer_id": buyer_id,  # Add buyer_id here
        "accept": "no",  # Default value
        "item_reached": "no"  # Default value
    }
    
    # Insert into the "after_bid" table
    result = after_bid_collection.insert_one(after_bid_data)
    
    # Update the response with inserted ID
    if result.inserted_id:
        return jsonify({"message": "Bid confirmed and moved to after_bid table"}), 201
    else:
        return jsonify({"error": "Failed to confirm bid"}), 500
@app.route('/successful_bids/<int:seller_id>', methods=['GET'])
def get_successful_bids(seller_id):
    # Fetch successful bids where accept = 'yes'
    successful_bids = after_bid_collection.find({"seller_id": seller_id, "accept": "yes"})
    
    successful_bids_data = []
    for bid in successful_bids:
        # Get bid details from the "bid" table using bid_id
        bid_details = bids_collection.find_one({"bid_id": bid["bid_id"]})
        
        if bid_details:
            # Combine the data from both collections
            successful_bids_data.append({
                "bid_id": bid["bid_id"],
                "price": bid["price"],
                "quantity": bid_details.get("quantity"),
                "properties": bid_details.get("properties"),
                "buyer_id": bid_details.get("buyer_id")
            })

    return jsonify(successful_bids_data)


@app.route('/unsuccessful_bids/<int:seller_id>', methods=['GET'])
def get_unsuccessful_bids(seller_id):
    # Fetch unsuccessful bids where accept = 'no'
    unsuccessful_bids = after_bid_collection.find({"seller_id": seller_id, "accept": "none"})
    
    unsuccessful_bids_data = []
    for bid in unsuccessful_bids:
        # Get bid details from the "bid" table using bid_id
        bid_details = bids_collection.find_one({"bid_id": bid["bid_id"]})
        
        if bid_details:
            # Combine the data from both collections
            unsuccessful_bids_data.append({
                "bid_id": bid["bid_id"],
                "price": bid["price"],
                "quantity": bid_details.get("quantity"),
                "properties": bid_details.get("properties"),
                "buyer_id": bid_details.get("buyer_id")
            })

    return jsonify(unsuccessful_bids_data)
    

if __name__ == '__main__':
    app.run(debug=True)
