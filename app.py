from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import subprocess
import sched
import time
from datetime import datetime
from functionalities import periodic_reading, returnReading, returnAll, readingAt, scheduler
from WiGraph.plot import graph_download, graph_upload
import plotly.graph_objs as go
import plotly.io as pio

scheduler = sched.scheduler(time.time, time.sleep)
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
        frequency = float(request.form['frequency'])
        max_occurrences = int(request.form['occurrences'])
        messages = periodic_reading(frequency, max_occurrences)
        return render_template('index.html', popup=messages)
    except subprocess.CalledProcessError as e:
        print("Error running periodic_reading.py:", e)
    return redirect(url_for('index', messages=messages, popup=messages))

@app.route('/return_dated', methods=['POST'])
def return_dated():
    try:    
        date = str(request.form['date'])          # Get date from the form
        readings=returnReading(date)              # Call the periodic_reading function with the values
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

@app.route('/run_dated', methods=['POST'])
def run_dated():
    try:    
        time_str = str(request.form['time'])
        readingAt(time_str)          # Call the periodic_reading function with the values
    except subprocess.CalledProcessError as e:
        print("Error running request:", e)
    return redirect(url_for('index'))

@app.route('/to_graph_index', methods=['GET'])
def to_graph_index():
    download_graph = graph_download()
    upload_graph = graph_upload()
    return render_template('graph_index.html', static_folder='static', plot_download=download_graph, plot_upload=upload_graph)

if __name__ == '__main__':
    app.run(debug=True)