from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/weiss')
def hello_world():
    return '<h1>This is python running a flask server, be aware it is not secure</h1>'


# @app.route('/hello/<name>')
# def hello_name(name):
#     return f'Hello {name}'

# @app.route('/cek_angka/<int:num>')
# def number(num):
#     if num % 2 == 0:
#         return f'Angka {num} ini genap'
#     else:
#         return f'Angka {num} ini ganjil'

# @app.route('/cek/<name>/')
# def cek(name):
#     if name == 'dzaky':
#         return f'{name} merupakan hama'
#     else:
#         return f'{name} bukan hama'
        
# @app.route('/login/<username>/<password>')

# @app.route('/login/<username>/<password>')
# def login(username, password):
#     if username == 'test' and password == '123':
#         return render_template('index.html', username=username)

#     return render_template('index.html', error='username or password invalid')


@app.route('/login', methods=['GET'])
def login_get():
    if request.method == 'GET':
        username = request.args.get('user')
        password = request.args.get('pass')

        if not username or not password:
            return render_template('index.html')

        if username == 'test' and password == '123':
            return render_template('index.html', username=username)

        return render_template('index.html', error='username or password invalid')
    else:
        return f'Method {request.method} not allowed'


app.run(debug=True)
