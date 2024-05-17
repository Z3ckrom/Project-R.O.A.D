from flask import Flask, render_template, jsonify, send_from_directory, current_app, send_file
import subprocess
import pymysql
from datetime import datetime
import os


app = Flask(__name__, template_folder='/var/www/html', static_folder='/var/www/html')

file_directory = '/PATH/TO/SHARED/FOLDER/'

# Database configuration
db_host = "localhost"
db_user = "USER"
db_password = "USER_PASS"
db_name = "ROV_DATA"

def connect_to_database():
    return pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Function to query database and get today's data as dictionaries
def get_data_for_today():
    connection = connect_to_database()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Get today's date
            today_date = datetime.now().strftime("%Y-%m-%d")
            
            # SQL query to fetch data for today
            sql = f"SELECT Test_Num, Voltage, pH, Temp, AirQuality, DATE_FORMAT(Date, '%Y-%m-%d') as Date FROM ROV_DATA WHERE DATE(Date) = '{today_date}'"
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
    finally:
        connection.close()

# Function to calculate averages
def calculate_averages(data):
    if data:
        num_rows = len(data)
        avg_pH = sum(row['pH'] for row in data) / num_rows
        avg_temp = sum(row['Temp'] for row in data) / num_rows
        avg_air_quality = sum(row['AirQuality'] for row in data) / num_rows
    else:
        avg_pH = avg_temp = avg_air_quality = 0
    return avg_pH, avg_temp, avg_air_quality


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line_chart_data')
def get_line_chart_data():
    data = get_data_for_today()
    if data:
        # Extract numerical values and date from each row
        formatted_data = [[row['AirQuality'], row['Date'], row['Temp'], row['Test_Num'], row['Voltage'], row['pH']] for row in data]
        return jsonify(formatted_data)
    else:
        return jsonify({'error': 'No data found for today.'})

@app.route('/pie_chart_averages')
def get_pie_chart_averages():
    pie_chart_data = get_data_for_today()
    if pie_chart_data:
        avg_pH, avg_temp, avg_air_quality = calculate_averages(pie_chart_data)
        return jsonify({'avg_pH': avg_pH, 'avg_temp': avg_temp, 'avg_air_quality': avg_air_quality})
    else:
        return jsonify({'error': 'No data found for today.'})

@app.route('/start_script')
def open_script():
    script_name = "/var/www/html/ROV.py"
    subprocess.Popen(["python", script_name])
    return 'Script opened'

@app.route('/stop_script')
def close_script():
    script_name = "/var/www/html/ROV.py"
    subprocess.Popen(["pkill", "-f", script_name])
    return 'Script closed'
    
@app.route('/download')
def download_file():
    today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f'{file_directory}{today_date}.csv'
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found"
        
        

if __name__ == '__main__':
    app.run(host='10.42.0.1', port=5001)
