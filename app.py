import jwt
from flask import jsonify, request, Response
from BookModel import *
import json
import datetime
from settings import *

books = Book.get_all_books()

DEFAULT_PAGE_LIMIT = 3

app.config['SECRET_KEY'] = 'joker'


@app.route('/login')
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route('/')
def home():
    return "check_api"


@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


def validBookObject(bookObject):
    if "code" in bookObject and "name" in bookObject and "price" in bookObject and "author" in bookObject:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['author'], request_data['price'],  request_data['code'],)
        response = Response("", "201", mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['code'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object",
            "helpString": "Please pass with proper object format"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:code>', methods=['POST'])
def get_book_by_code(code):
    result = Book.get_book(code)
    return jsonify(result)


@app.route('/books/<int:code>', methods=['PUT'])
def replace_book(code):
    request_data = request.get_json()

    Book.replace_book(code, request_data['name'], request_data['author'], request_data['price'])
    response = Response("", status=204)
    return response


@app.route('/books/<int:code>', methods=['PATCH'])
def update_book(code):
    request_data = request.get_json()
    if "name" in request_data:
        Book.update_book_name(code, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(code, request_data['price'])
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(code)
    return response


@app.route('/books/<int:code>', methods=['DELETE'])
def delete_book(code):
    if(Book.delete_book(code)):
        return Response("", status=204)

    invalidDeleteRequestErrorMsg = {
        "error": "Invalid book object",
        "helpString": "Please pass with proper object format"
    }
    response = Response(json.dumps(invalidDeleteRequestErrorMsg), status=400, mimetype='application/json')
    return response


app.run(port=5000)

