from flask import Flask, jsonify

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

