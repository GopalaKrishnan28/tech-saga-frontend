from pymongo import MongoClient

# Updated connection string with new credentials
uri = "mongodb+srv://arun:1234@cluster1.v5dye5b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

# Connecting to MongoDB using the URI
client = MongoClient(uri)

# Accessing the "app" database
db = client["app"]

# Define collections
sellers_collection = db["sellers"]
items_collection = db["items"]

# Sample data for sellers collection
sellers_data = [
    {
        "seller_id": 1,
        "name": "ABC Construction",
        "email": "abc@construction.com",
        "password": "securepassword",
        "contact_no": "1234567890",
        "address": "123 Main St, City, Country",
        "logo": "https://www.bing.com/images/search?view=detailV2&ccid=QD8aRC6s&id=C9A70F193943AF8C1A1744AED53F830066373A87&thid=OIP.QD8aRC6seM0ht0xv2ewENwHaHa&mediaurl=https%3a%2f%2fi.etsystatic.com%2f40317824%2fr%2fil%2f339134%2f4827441773%2fil_fullxfull.4827441773_887m.jpg&exph=2048&expw=2048&q=image+link&simid=608039388660043845&FORM=IRPRST&ck=A709DB53ED960C3E884DEB9CEAF89D7C&selectedIndex=0&itb=0"
    },
    {
        "seller_id": 2,
        "name": "XYZ Builders",
        "email": "xyz@builders.com",
        "password": "password123",
        "contact_no": "9876543210",
        "address": "456 Park Avenue, City, Country",
        "logo": "https://via.placeholder.com/150"
    }
]

# Sample data for items collection
items_data = [
    {
        "seller_id": 1,
        "productName": "Bricks",
        "properties": "Red, Durable, 10x20cm"
    },
    {
        "seller_id": 1,
        "productName": "Cement",
        "properties": "High Strength, 50kg Bag"
    },
    {
        "seller_id": 2,
        "productName": "Steel Rods",
        "properties": "Length: 12ft, Diameter: 10mm"
    },
    {
        "seller_id": 2,
        "productName": "Concrete Mix",
        "properties": "Ready to use, 40kg Bag"
    }
]

# Insert sample data into the collections
sellers_collection.insert_many(sellers_data)
items_collection.insert_many(items_data)

print("Sample data inserted successfully.")
