from flask import Flask, request, jsonify
from pymongo import MongoClient

# create a new Flask application
app = Flask(__name__)

# create a MongoClient instance to connect to the MongoDB server
client = MongoClient("mongodb://mongo:27017")

# database instance
db = client["mydatabase"]

# collection instance
todos = db["Todos"]


# API endpoint to get todos data
@app.route('/todos', methods=['GET'])
def get_todos():
    todos_data = []
    for todo_element in todos.find():
        todos_data.append({
            "id": str(todo_element["_id"]),
            "name": todo_element["name"],
            "description": todo_element["description"],
            "status": todo_element["status"],
            "tags": todo_element["tags"]
        })
    return jsonify(todos_data), 200


# API endpoint to add customer data
@app.route('/todos', methods=['POST'])
def add_todos():
    new_todo = {
        "name": request.json["name"],
        "description": request.json["description"],
        "status": request.json["status"],
        "tags": request.json["tags"]
    }
    x = todos.insert_one(new_todo)
    return jsonify({"id": str(x.inserted_id)}), 201


# API default endpoint
@app.route('/', methods=['GET'])
def default():
    return "Welcome to the Todo API!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)