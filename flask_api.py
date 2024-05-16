from flask import Flask, request, jsonify
from pymongo import MongoClient

# create a new Flask application
app = Flask(__name__)

# create a MongoClient instance to connect to the MongoDB server
client = MongoClient("mongodb://mongo:27017")

# database instance
db = client["mydatabase"]

# collection instance
customers = db["customers"]


# API endpoint to get customer data
@app.route('/customers', methods=['GET'])
def get_customers():
    customer_data = []
    for customer in customers.find():
        customer_data.append({
            "id": str(customer["_id"]),
            "name": customer["name"],
            "age": customer["age"],
            "address": customer["address"]
        })
    return jsonify(customer_data), 200


# API endpoint to add customer data
@app.route('/customers', methods=['POST'])
def add_customer():
    new_customer = {
        "name": request.json["name"],
        "age": request.json["age"],
        "address": request.json["address"]
    }
    x = customers.insert_one(new_customer)
    return jsonify({"id": str(x.inserted_id)}), 201


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)