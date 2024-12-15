# visual.py

from flask import Flask, render_template_string
import csv

app = Flask(__name__)

list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

@app.route('/')
def display_csv():
    # Read the CSV file
    with open(list_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    
    # Generate HTML table
    table = '<table border="1">'
    for row in data:
        table += '<tr>'
        for cell in row:
            table += f'<td>{cell}</td>'
        table += '</tr>'
    table += '</table>'
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ATTENDANCE DATA</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }
                th {
                    background-color: #f4f4f4;
                }
            </style>
        </head>
        <body>
            <h1>ATTENDANCE DATA</h1>
            {{ table|safe }}
        </body>
        </html>
    ''', table=table)

if __name__ == '__main__':
    app.run(debug=True)
