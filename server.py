from flask import Flask, jsonify, request, g, render_template, session
from flask_cors import CORS
from controllers import weiland
from werkzeug import exceptions
from db import get_db
import hashlib

server = Flask(__name__)
CORS(server)
server.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@server.route('/')
def home():
    return jsonify({'message': 'Hello from Flask!'}), 200


## NEW CODE FOR REGISTER AND LOGIN ##
def hash_function(input):
    return hashlib.sha256(input.encode()).hexdigest()


@server.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with server.app_context():
        db = get_db()
        with server.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@server.route("/register", methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # Check whether the passwords match
        if password1 != password2:
            message = "Passwords do not match"
            return render_template("register.html", message=message)

        # Check whether anyone with this username has already registered
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE username=?", (username, ))
        count = cursor.fetchone()[0]
        if count > 0:
            message = "User with username already exists"
            return render_template("register.html", message=message)

        hashed_password = hash_function(password1)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        message = "Successfully registered"
    return render_template("register.html", message=message)


@server.route("/login", methods=['GET', 'POST'])
def login():
    message = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE username=?", (username, ))
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.execute(
                "SELECT password FROM users WHERE username=?", (username, ))
            password_in_database = cursor.fetchone()[0]
            if hash_function(password) == password_in_database:
                session['authenticated'] = True
                message = "You have successfully logged in"
            else:
                message = "Incorrect password"
        else:
            message = "No user with that username"

    return render_template("login.html", message=message)


@server.route("/private")
def private():
    if not "authenticated" in session:
        return "You are not allowed here"

    return "Put weiland db here"


@server.route("/logout")
def logout():
    del session['authenticated']
    return "Thank you for visiting"


#####################################

@server.route("/weiland", methods=['GET', 'POST'])
def new_student():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form["name"]
        status = request.form["status"]
        cursor.execute(
            "INSERT INTO weiland (name, status) VALUES (?, ?);",
            (name, status)
        )
        db.commit()

    cursor.execute("SELECT * from weilands;")
    weiland = cursor.fetchall()

    return render_template("weiland.html", table=weiland)


# @app.route("/new", methods=['GET', 'POST'])
# def new_trees():
#     db = get_db()
#     cursor = db.cursor()

#     if request.method == 'POST':
#         name = request.form['name']
#         species = request.form['species']
#         cursor.execute(
#             "INSERT INTO trees (id, name, species) VALUES (?, ?, ?);",
#             (2, name, species)
#         )
#         db.commit()

#     cursor.execute("SELECT * from trees")
#     trees = cursor.fetchall()

#     return render_template("new.html", trees=trees)

################################


# @server.route('/weiland')
# def all_weiland():
#     return jsonify({'weiland': weiland.index()})


# @server.route('/weiland', methods=['POST'])
# def new_student():
#     return weiland.create(request)


# @server.route('/weiland/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
# def id_weiland(id):
#     fn = {
#         'GET': weiland.show,
#         'PATCH': weiland.update,
#         'DELETE': weiland.destroy
#     }
#     resp, code = fn[request.method](request, id)
#     return jsonify(resp), code


@server.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@server.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


if __name__ == "__main__":
    server.run(debug=True)
