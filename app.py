from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


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
    return render_template('shopping_lists_new.html', shopping_list={}, title='New Shopping List')

@app.route('/shopping_lists', methods=['POST'])
def shopping_lists_submit():
    """Submit a new Shopping List."""
    shopping_list = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'images': request.form.get('images').split()
    }
    shopping_list_id = shopping_lists.insert_one(shopping_list).inserted_id
    return redirect(url_for('shopping_lists_show', shopping_list_id=shopping_list_id))

@app.route('/shopping_lists/<shopping_list_id>')
def shopping_lists_show(shopping_list_id):
    """Show a single shopping list."""
    shopping_list = shopping_lists.find_one({'_id': ObjectId(shopping_list_id)})
    return render_template('shopping_lists_show.html', shopping_list=shopping_list)

@app.route('/shopping_lists/<shopping_list_id>/edit')
def shopping_lists_edit(shopping_list_id):
    """Show the edit form for a playlist."""
    shopping_list = shopping_lists.find_one({'_id': ObjectId(shopping_list_id)})
    return render_template('shopping_lists_edit.html', shopping_list=shopping_list, title='Edit Shopping List')

@app.route('/shopping_lists/<shopping_list_id>', methods=['POST'])
def shopping_lists_update(shopping_list_id):
    """Submit an edited playlist."""
    updated_shopping_list = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'images': request.form.get('images').split()
    }
    shopping_lists.update_one(
        {'_id': ObjectId(shopping_list_id)},
        {'$set': updated_shopping_list})
    return redirect(url_for('shopping_lists_show', shopping_list_id=shopping_list_id))

@app.route('/shopping_lists/<shopping_list_id>/delete', methods=['POST'])
def shopping_lists_delete(shopping_list_id):
    """Delete one playlist."""
    shopping_lists.delete_one({'_id': ObjectId(shopping_list_id)})
    return redirect(url_for('shopping_lists_index'))

if __name__ == '__main__':
    app.run(debug=True)