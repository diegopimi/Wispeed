from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import subprocess
from functionalities import periodic_reading, returnReading, returnAll

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
        frequency = float(request.form['frequency'])          # Get frequency value from the form
        max_occurrences = int(request.form['occurrences'])    # Get max occurrences value from the form
        periodic_reading(frequency, max_occurrences)          # Call the periodic_reading function with the values
    except subprocess.CalledProcessError as e:
        print("Error running periodic_reading.py:", e)
    return redirect(url_for('index'))

@app.route('/return_dated', methods=['POST'])
def return_dated():
    try:    
        date = str(request.form['date'])          # Get date from the form
        readings=returnReading(date)          # Call the periodic_reading function with the values
        return render_template('index.html', data=readings)
    except subprocess.CalledProcessError as e:
        print("Error running request:", e)
    return redirect(url_for('index'))

@app.route('/return_all', methods=['POST'])
def return_all():
    try:    
        readings=returnAll()          # Call the periodic_reading function with the values
        return render_template('index.html', data=readings)
    except subprocess.CalledProcessError as e:
        print("Error running request:", e)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)