import sqlite3
from sqlite3.dbapi2 import Cursor, connect
import logging, sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import __init__

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    __init__.db_counter += 1
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s %(message)s',datefmt='%m/%d/%Y, %I:%M:%S')
logger.setLevel(logging.INFO)
handler_debug_formatter = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s', datefmt='%m/%d/%Y, %I:%M:%S,')
handler_debug = logging.StreamHandler(sys.stdout)
handler_debug.setLevel(logging.INFO)
handler_debug.setFormatter(handler_debug_formatter)

handler_err = logging.StreamHandler(sys.stderr)
handler_err.setLevel(logging.ERROR)
handler_err.setFormatter(handler_debug_formatter)
# handler_2 = logging.StreamHandler(sys.stderr)
# handler_2.setLevel(logging.ERROR)

logger.addHandler(handler_debug)


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      logger.info("Article "+"\""+post['title']+"\" retrieved!")
      return render_template('post.html', post=post)

##Standout Suggesion 1
@app.route('/healthz')
def health_check():
    connection = get_db_connection()
    try:
        len(connection.execute('SELECT * FROM posts').fetchall())
        message = "OK - healthy!"
        status_code=200
    except:
        status_code=500
        message = "ERROR - unhealthy"
    response = app.response_class(
        response=json.dumps({"result":message}),
        status=status_code,
        mimetype = 'application/json'
    )
    return response

@app.route('/metrics')
def get_metrics():
    connection = get_db_connection()
    posts = len(connection.execute('SELECT * FROM posts').fetchall())
    response=app.response_class(
        response=json.dumps({"db_connections":__init__.db_counter,"posts": posts}),
        status=200,
        mimetype = 'application/json'
    )
    connection.close()
    return response

@app.errorhandler(404)
def no_page_found(e):
    # logger.error("A non-existing article is accessed and 404 is returned")
    return render_template('404.html'), 404

# Define the About Us page
@app.route('/about')
def about():
    logger.info('The "About us " page is accessed')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            logger.info('New Page with title '+title+ ' created')
            connection.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
