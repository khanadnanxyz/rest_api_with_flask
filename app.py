from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'id': 1,
        'name': 'book 1',
        'price': 9,
        'author': 'sherlock'
    },
    {
        'id': 2,
        'name': 'book2',
        'price': 19,
        'author': 'moriarty'
    }
]

@app.route('/')
def home():
    return "check_api"

@app.route('/books')
def get_books():
    return jsonify({'books': books})


def validBookObject(bookObject):
    if ("id" in bookObject and "name" in bookObject and "price" in bookObject and "author" in bookObject):
        return True
    else:
        return False


@app.route('/books', methods =['POST'])
def add_book():
    request_data = request.get_json();
    if (validBookObject(request_data)):
        new_book = {
            "id": request_data['id'],
            "name": request_data['name'],
            "price": request_data['price'],
            "author": request_data['author']
        }
        books.insert(0, new_book)
        response = Response("", "201", mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['id'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object",
            "helpString": "Please pass with proper object format"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:id>')
def get_book_by_id(id):
    result = {}
    for book in books:
        if book['id'] == id:
            result = {
                'name': book['name'],
                'price': book['price']
            }

    return jsonify(result)


app.run(port=5000)

