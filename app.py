from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
import sqlite3
from auth import auth_bp
from datetime import datetime, timedelta 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        from auth import User
        user_obj = User()
        user_obj.id = user[0]
        return user_obj

    return None

def init_db():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()


init_db()



@app.route('/')
def index():
    if current_user.is_authenticated:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT posts.id, posts.title, posts.content, posts.created_at, users.username
            FROM posts
            JOIN users ON posts.user_id = users.id
            ORDER BY posts.created_at DESC
        ''')
        posts = cursor.fetchall()
        conn.close()
        return render_template('index.html', posts=posts)

    return render_template('login_register.html')
@app.route('/add_post', methods=['POST'])
@login_required
def add_post():
    if request.method == 'POST':
        content = request.form['content']

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)', ('', content, current_user.id))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute('INSERT INTO comments (post_id, content, user_id) VALUES (?, ?, ?)', (post_id, content, current_user.id))
        conn.commit()

    cursor.execute('''
        SELECT posts.id, posts.title, posts.content, posts.created_at, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    ''', (post_id,))
    post = cursor.fetchone()

    cursor.execute('''
        SELECT comments.id, comments.content, comments.created_at, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.created_at DESC
    ''', (post_id,))
    comments = cursor.fetchall()

    conn.close()
    return render_template('post.html', post=post, comments=comments, datetime=datetime)

if __name__ == '__main__':
    app.run(debug=True)
