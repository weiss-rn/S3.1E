from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/', methods=['GET'])
def get_users():
    data = load_data()
    return jsonify(data)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    data = load_data()
    user = next((u for u in data if u['id'] == user_id), None)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)