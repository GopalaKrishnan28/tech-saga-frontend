from flask import Flask, jsonify, request,send_file,session
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from bson.objectid import ObjectId
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Connect to MongoDB using the credentials
client = MongoClient("mongodb+srv://arun:1234@cluster1.v5dye5b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["app"]

# Define collections
sellers_collection = db["sellers"]
items_collection = db["items"]
transaction_collection=db["transaction"]
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
    
# Helper function to convert ObjectId to string
def convert_objectid_to_str(data):
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

@app.route('/completed_transactions/<int:seller_id>', methods=['GET'])
def get_completed_transactions(seller_id):
    # Fetch transactions where accept = 'yes' and item_reached = 'yes'
    completed_bids = after_bid_collection.find({
        "seller_id": seller_id,
        "accept": "yes",
        "item_reached": "yes"
    })

    transactions_data = []
    for bid in completed_bids:
        # Get bid details from the "bid" table using bid_id
        bid_details = bids_collection.find_one({"bid_id": bid["bid_id"]})
        
        if bid_details:
            # Prepare transaction data
            transaction_data = {
                "transaction_id": bid["_id"],  # Leave ObjectId here for now
                "product": bid_details["product"],
                "quantity": bid_details["quantity"],
                "price": bid["price"],
                "properties": bid_details["properties"],
                "buyer_id": bid_details["buyer_id"],
                "seller_id": bid["seller_id"]
            }

            # Insert into the "transaction" table
            transaction_collection.insert_one(transaction_data)
            transactions_data.append(transaction_data)

    # Convert all ObjectId fields to string before returning the response
    return jsonify(convert_objectid_to_str(transactions_data))

@app.route('/download_invoice/<transaction_id>', methods=['GET'])
def download_invoice(transaction_id):
    try:
        # Convert the string transaction_id to ObjectId
        transaction_object_id = ObjectId(transaction_id)
    except Exception as e:
        return jsonify({"error": f"Invalid transaction ID format: {e}"}), 400

    # Fetch the transaction details from the "transaction" table
    print(transaction_object_id)
    transaction = transaction_collection.find_one({"transaction_id": transaction_object_id})
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    
    # Create a PDF to represent the invoice
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add transaction details to the PDF
    c.drawString(100, height - 40, f"Invoice for Transaction {transaction['_id']}")
    c.drawString(100, height - 80, f"Product: {transaction['product']}")
    c.drawString(100, height - 100, f"Quantity: {transaction['quantity']}")
    c.drawString(100, height - 120, f"Price: {transaction['price']}")
    c.drawString(100, height - 140, f"Properties: {transaction['properties']}")
    c.drawString(100, height - 160, f"Buyer ID: {transaction['buyer_id']}")
    c.drawString(100, height - 180, f"Seller ID: {transaction['seller_id']}")
    
    # Save the PDF to the buffer
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{transaction['_id']}.pdf", mimetype='application/pdf')
@app.route('/upload_bid', methods=['POST'])
def upload_bid():
    try:
        data = request.json
        product = data['product']
        quantity = int(data['quantity'])
        deadline = data['deadline']
        properties = data['properties']
        buyer_id = data['buyer_id']

        # Insert the new bid into the "bid" table
        bid_data = {
            "buyer_id": buyer_id,
            "quantity": quantity,
            "deadline": deadline,
            "product": product,
            "properties": properties
        }
        result = bids_collection.insert_one(bid_data)
        return jsonify({"message": "Bid uploaded successfully", "bid_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to upload bid: {str(e)}"}), 500
@app.route('/confirm_bidder', methods=['POST'])
def confirm_bidder():
    try:
        data = request.json
        after_bid_id = data.get("after_bid_id")

        # Update the 'accept' field to 'yes' for the selected bidder
        result = after_bid_collection.update_one(
            {"_id": ObjectId(after_bid_id)},
            {"$set": {"accept": "yes"}}
        )

        if result.modified_count > 0:
            return jsonify({"message": "Bidder confirmed successfully."}), 200
        else:
            return jsonify({"error": "Bidder confirmation failed."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/bids_with_bidders', methods=['GET'])
def get_bids_with_bidders():
    try:
        # Simulating session buyer_id (replace with actual session logic)
        session_buyer_id = 1

        # Find all bids created by the buyer from the "bid" table
        bids = list(bids_collection.find({"buyer_id": session_buyer_id}))

        result = []

        for bid in bids:
            # Fetch bidders for this bid from the "after_bid" table
            bidders = list(after_bid_collection.find({"bid_id": bid["bid_id"]}))
            
            # Prepare each bid with its bidders
            bid_data = {
                "bid_id": bid["bid_id"],
                "buyer_id": bid["buyer_id"],
                "product": bid["product"],
                "quantity": bid["quantity"],
                "properties": bid["properties"],
                "deadline": bid["deadline"],
                "bidders": [
                    {
                        "after_bid_id": str(bidder["_id"]),
                        "price": bidder["price"],
                        "seller_id": bidder["seller_id"],
                        "accept": bidder["accept"]
                    }
                    for bidder in bidders
                ]
            }
            result.append(bid_data)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/pending_deliveries/<int:buyer_id>', methods=['GET'])
def get_pending_deliveries(buyer_id):
    try:
        # Fetch records from after_bid where accept = "yes", item_reached = "no", and buyer_id matches
        pending_deliveries = list(
            after_bid_collection.find({"accept": "yes", "item_reached": "no", "buyer_id": buyer_id})
        )
        
        # For each record, fetch additional product details from the bid table
        deliveries = []
        for delivery in pending_deliveries:
            bid = bids_collection.find_one({"bid_id": delivery["bid_id"]})
            if bid:
                delivery_data = {
                    "bid_id": delivery["bid_id"],
                    "price": delivery["price"],
                    "buyer_id": delivery["buyer_id"],
                    "seller_id": delivery["seller_id"],
                    "product": bid.get("product"),
                    "quantity": bid.get("quantity"),
                    "properties": bid.get("properties"),
                }
                deliveries.append(delivery_data)

        return jsonify(deliveries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/confirm_delivery/<int:buyer_id>/<bid_id>', methods=['POST'])
def confirm_delivery(buyer_id, bid_id):
    try:
        bid_id=int(bid_id)
        buyer_id=int(buyer_id)
     
        # Update item_reached to "yes" in after_bid table for the given bid_id and buyer_id
        result = after_bid_collection.update_one(
            {"bid_id": bid_id, "accept": "yes", "item_reached": "no", "buyer_id": buyer_id},
            {"$set": {"item_reached": "yes"}}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Delivery confirmed successfully"}), 200
        else:
            return jsonify({"error": "Delivery confirmation failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
