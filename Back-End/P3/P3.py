from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    data = [{
        'Name': 'John Doe',
        'Work': 'Software Engineer',
        'Message': 'Hello World! and i accept free food for a basic coding task'

    }]
    return make_response(jsonify(data), 200)

@app.route('/employees', methods=['GET', 'POST', 'PUT', 'DELETE'])

def employees():
    try:
        if request.method == 'GET':
            data = [{
                'Name': 'John Doe GET',
                'Work': 'Software Engineer',
                'Message': 'Hello World! and i accept free food for a basic coding task'

            }]
        elif request.method == 'POST':
            data = [{
                'Name': 'John Doe POST',
                'Work': 'Software Engineer',
                'Message': 'Hello World! and i accept free food for a basic coding task'

            }]
        elif request.method == 'PUT':
            data = [{
                'Name': 'John Doe PUT',
                'Work': 'Software Engineer',
                'Message': 'Hello World! and i accept free food for a basic coding task'

            }]
        else:
            data = [{
                'Name': 'John Doe DELETE',
                'Work': 'Software Engineer',
                'Message': 'Hello World! and i accept free food for a basic coding task'

            }]
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    return make_response(jsonify(data), 200)

if __name__ == '__main__':
    app.run(debug=True)
    

