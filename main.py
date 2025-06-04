from app import app
from flask import request, jsonify
from db.functions import create_user

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        create_user(username=username, password=password)

        return jsonify({'message': 'deu boa', "username": username, "password": password})
    
    except Exception as e:

        return jsonify({"message": "deu ruim", "error": e})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]

        return jsonify({'message': 'deu boa', "username": username, "password": password})
    
    except:
        return jsonify({"message": "deu ruim"})

@app.route('/get_data', methods=['POST'])
def get_data():
    return 'b'

app.run(port=8890)