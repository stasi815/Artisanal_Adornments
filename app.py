from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to the shop!!')

# items = [
#     { 'title': 'Yawanawa Earrings', 'description': 'Blue and Green beads' },
#     { 'title': 'Yawanawa Necklace', 'description': '6 inches long, red, yellow, black' }
# ]

@app.route('/items')
def playlists_index():
    """Show all items."""
    return render_template('items_index.html', items=items.find())

if __name__ == '__main__':
    app.run(debug=True)