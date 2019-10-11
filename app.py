from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Artisanal_Adornments')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
shopping_lists = db.shopping_lists
inventory = db.inventory

inventory.drop()
inventory.insert_many([
    {"name":"Long Rainbow Serpent", "category":"necklace", "price":"$200.00", "images":"static/colar3.jpg"},
    {"name":"Rainbow Supernova", "category":"necklace", "price":"$160.00", "images":"static/necklace1.jpg"},
    {"name":"Green Serpent", "category":"necklace", "price":"$160.00", "images":"static/necklace2.jpeg"},
    {"name":"Fire Lizard", "category":"wristband", "price":"$125.00", "images":"static/wristband1.jpg"},
    {"name":"Fire Tide", "category":"wristband", "price":"$125.00", "images":"static/wristband2.jpg"},
    {"name":"Amazon Sunset", "category":"earrings", "price":"$100.00", "images":"static/yawanawa_brinco2.jpg"},
    {"name":"Wacomaya", "category":"earrings", "price":"$100.00", "images":"static/yawanawaearrings1.jpg"}
    ])


app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to the shop!!')

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
        'items': []
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

@app.route('/inventory')
def inventory_index():
    """Show inventory."""
    return render_template('inventory.html', inventory=inventory.find(), shopping_lists=shopping_lists.find())

@app.route('/add', methods=['POST'])
def add_item_to_list():
    """Add inventory item to selected list"""
    item = {
        'name': request.form.get('name'),
        'category': request.form.get('category'),
        'price': request.form.get('price'),
        'images': request.form.get('images')
    }
    shopping_list_id = request.form.get('shopping_list')

    shopping_lists.update_one(
        {'_id': ObjectId(shopping_list_id)},
        {'$set': {'items': [item]}})
    return redirect(url_for('shopping_lists_show', shopping_list_id=shopping_list_id))



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
