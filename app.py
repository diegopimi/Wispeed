from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
import subprocess
import sched
import time
from datetime import datetime
from functionalities import periodic_reading, returnReading, returnAll, readingAt, scheduler
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
    # Query MongoDB to get the data
    cursor = mongo.db.WiSpeed.find({}, {'_id': 0, 'Download': 1, 'Upload': 1})

    # Extract x and y values from the query result
    x_values = []
    y_values = []
    for document in cursor:
        x_values.append(document['Download'])
        y_values.append(document['Upload'])

    # Create a Plotly line plot
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values))

    # Convert the Plotly figure to HTML
    html_output = fig.to_html(full_html=False)
    
    # pio.show(fig, renderer='browser')
    return render_template('graph_index.html', static_folder='static', plot_html=html_output)


if __name__ == '__main__':
    app.run(debug=True)