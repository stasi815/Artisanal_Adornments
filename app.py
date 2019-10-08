from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Flask is Cool!!')

items = [
    { 'title': 'Yawanawa Earrings', 'description': 'Blue and Green beads' },
    { 'title': 'Yawanawa Necklace', 'description': '6 inches long, red, yellow, black' }
]

@app.route('/items')
def playlists_index():
    """Show all items."""
    return render_template('items_index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)