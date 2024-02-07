from flask import Flask, request, jsonify, g
from datetime import datetime
from os import getenv, path, makedirs
from sqlite3 import connect
from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
db_dir = '/opt/db'

# Creating 'db' directory if it doesn't exist
if not path.exists(db_dir):
    makedirs(db_dir)
    
store_type = getenv("store")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect(path.join(db_dir, 'database.db'))
    return db

@app.before_request
def before_request():
    if store_type == "sqlite":
        db = get_db()
        with db:
            db.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, date TEXT)')

# Define the metrics
REQUESTS_TOTAL = Counter('requests_total', 'Total Request Count', ['method', 'endpoint'])


@app.route('/hello', methods=['GET'])
def hello():
    REQUESTS_TOTAL.labels(method='GET', endpoint='/hello').inc()
    return "Hello page", 200

@app.route('/user', methods=['POST', 'GET'])
def user():
    name = request.args.get('name')
    if request.method == 'POST':
        REQUESTS_TOTAL.labels(method='POST', endpoint='/user').inc()
        if store_type == "sqlite":
            db = get_db()
            with db:
                db.execute("INSERT INTO users (name, date) VALUES (?, ?)", (name, datetime.now().strftime("%H:%M:%S - %d.%m.%Y")))
        else:
            with open(path.join(db_dir, f'{name}.txt'), 'a') as f:
                f.write(f'{name}: {datetime.now().strftime("%H:%M:%S - %d.%m.%Y")}\n')
        return f"{name} saved!", 200
    elif request.method == 'GET':
        REQUESTS_TOTAL.labels(method='GET', endpoint='/user').inc()
        if store_type == "sqlite":
            db = get_db()
            with db:
                cur = db.cursor()
                cur.execute("SELECT * FROM users WHERE name=?", (name,))
                data = cur.fetchall()
        else:
            file_path = path.join(db_dir, f'{name}.txt')
            if not path.exists(file_path):
                return jsonify({"error": "User not found"}), 404
            with open(file_path, 'r') as f:
                data = f.readlines()
        return jsonify(data), 200

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
