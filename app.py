from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Artisanal_Adornments
shopping_lists = db.shopping_lists

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to the shop!!')

# items = [
#     { 'title': 'Yawanawa Earrings', 'description': 'Blue and Green beads' },
#     { 'title': 'Yawanawa Necklace', 'description': '6 inches long, red, yellow, black' }
# ]

@app.route('/shopping_lists')
def shopping_lists_index():
    """Show all shopping_lists."""
    return render_template('shopping_lists_index.html', shopping_lists=shopping_lists.find())

@app.route('/shopping_lists/new')
def shopping_lists_new():
    """Create a new Shopping List."""
    return render_template('shopping_lists_new.html')

@app.route('/shopping_lists', methods=['POST'])
def shopping_lists_submit():
    """Submit a new Shopping List."""
    shopping_list = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'images': request.form.get('images').split()
    }
    shopping_lists.insert_one(shopping_list)
    print(request.form.to_dict())
    return redirect(url_for('shopping_lists_index'))

if __name__ == '__main__':
    app.run(debug=True)