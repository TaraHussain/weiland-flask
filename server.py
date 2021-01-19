from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import weiland
from werkzeug import exceptions

server = Flask(__name__)
CORS(server)


@server.route('/')
def home():
    return jsonify({'message': 'Hello from Flask!'}), 200


@server.route('/weiland')
def all_weiland():
    return jsonify({'weiland': weiland.index()})


@server.route('/weiland', methods=['POST'])
def new_student():
    return weiland.create(request)


@server.route('/weiland/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def id_weiland(id):
    fn = {
        'GET': weiland.show,
        'PATCH': weiland.update,
        'DELETE': weiland.destroy
    }
    resp, code = fn[request.method](request, id)
    return jsonify(resp), code


@server.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@server.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


if __name__ == "__main__":
    server.run(debug=True)
