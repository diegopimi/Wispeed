from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import subprocess

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/DBPimi'
mongo = PyMongo(app)

@app.route('/')
def index():
    data = mongo.db.WiSpeed.find()
    return render_template('index.html', data=data)


@app.route('/run_main', methods=['POST'])
def run_main():
    try:
        subprocess.run(["python", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running main.py:", e)
    return redirect(url_for('index'))

@app.route('/run_periodical', methods=['POST'])
def run_periodical():
    try:
        from functionalities import periodic_reading
        periodic_reading(2, 4)  # Call the periodic_reading function directly
    except subprocess.CalledProcessError as e:
        print("Error running periodic_reading.py:", e)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)