from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://arun:1234@cluster1.v5dye5b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["app"]

# Get the bids collection
bids_collection = db["bid"]

# Sample bids to insert
bids = [
    {
        "bid_id": 1,
        "buyer_id": 101,
        "quantity": 10,
        "product": "Steel Rods",
        "properties": "Length: 12ft, Diameter: 10mm"
    },
    {
        "bid_id": 2,
        "buyer_id": 102,
        "quantity": 5,
        "product": "bricks",
        "properties": "Red, Durable, 10x20cm"
    },
    {
        "bid_id": 3,
        "buyer_id": 103,
        "quantity": 15,
        "product": "cement",
        "properties": "High Strength, 50kg Bag"
    }
]

# Insert the sample bids
result = bids_collection.insert_many(bids)

# Print the inserted IDs
print("Inserted bid IDs:", result.inserted_ids)
