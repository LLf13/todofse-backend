from datetime import datetime

from bson import ObjectId
from flask import Flask, request, jsonify, g
from pymongo import MongoClient

from flask_user_management import user_management, login_manager, bcrypt


# create a new Flask application

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_management)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    return app


def get_db():
    if 'db' not in g:
        g.db = MongoClient("mongodb://mongo:27017").get_database("mydatabase")
        return g.db


app = create_app()

db = get_db()
# collection instance
todos = db["Todos"]


# API endpoint to get todos data
@app.route('/todos', methods=['GET'])
def get_todos():
    all_todos = todos.find()

    result = []
    for todo in all_todos:
        item = {
            "id": str(todo['_id']),
            "user_id": todo['user_id'],
            "title": todo['title'],
            "description": todo['description'],
            "created_at": todo['created_at'].strftime('%Y-%m-%d %H:%M:%S') if todo.get('created_at') else None,
            "updated_at": todo['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if todo.get('updated_at') else None,
            "due_date": todo['due_date'].strftime('%Y-%m-%d %H:%M:%S') if todo.get('due_date') else None,
            "completed": todo['completed'],
            "priority": todo['priority'],
        }
        result.append(item)
    return jsonify(result), 200


@app.route('/todos/<id>', methods=['GET'])
def get_todo(_id):
    todo = todos.find_one({'_id': ObjectId(_id)})
    if todo:
        # Do data processing here and return the data
        return_data = {
            "id": str(todo.get('_id')),
            "user_id": todo.get('user_id'),
            "title": todo.get('title'),
            "description": todo.get('description'),
            "created_at": todo.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if todo.get('created_at') else None,
            "updated_at": todo.get('updated_at').strftime('%Y-%m-%d %H:%M:%S') if todo.get('updated_at') else None,
            "due_date": todo.get('due_date').strftime('%Y-%m-%d %H:%M:%S') if todo.get('due_date') else None,
            "completed": todo.get('completed'),
            "priority": todo.get('priority'),
        }
        return jsonify(return_data), 200
    else:
        # Return not found if no Todo_element with that ID is found
        return jsonify({'error': 'Todo not found'}), 404


# API endpoint to add todos
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = {
        'user_id': data.get('user_id'),  # Get user_id from the request data
        'title': data.get('title'),
        'description': data.get('description', ''),  # Default to empty string if no description provided
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'due_date': datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None,
        # Convert string date to datetime
        'completed': data.get('completed', False),  # Default to False if no completion status provided
        'priority': data.get('priority', 'Medium'),  # Default to Medium if no priority level provided
    }
    x = todos.insert_one(new_todo)
    return jsonify({"id": str(x.inserted_id)}), 201


# API default endpoint
@app.route('/', methods=['GET'])
def default():
    return "Welcome to the Todo API!"


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
