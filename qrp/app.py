from flask import Flask, render_template, request, redirect, url_for
import pyqrcode
import os
import csv
import datetime
import cv2

app = Flask(__name__)
list_file_path = "list.csv"
qr_code_dir = "student_qrcodes"
if not os.path.exists(qr_code_dir):
    os.makedirs(qr_code_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        num_students = int(request.form['num_students'])
        roll_numbers = [request.form[f'roll_number_{i}'].upper() for i in range(num_students)]

        with open(list_file_path, mode='r', newline='') as list_file:
            list_reader = csv.reader(list_file)
            existing_data = [row for row in list_reader]

        header = existing_data[0]
        existing_data_dict = {row[0]: row for row in existing_data[1:]}

        new_roll_numbers = []
        for roll_number in roll_numbers:
            if roll_number not in existing_data_dict:
                url = pyqrcode.create(roll_number)
                qr_code_path = f"{qr_code_dir}/{roll_number}.png"
                url.png(qr_code_path, scale=6)
                qr_code_hyperlink = f'=HYPERLINK("{qr_code_path}", "Image")'
                new_roll_numbers.append([roll_number, qr_code_hyperlink])
            else:
                print(f"Roll number {roll_number} already exists. Skipping QR code generation.")

        for new_row in new_roll_numbers:
            existing_data_dict[new_row[0]] = new_row

        def alphanumeric_sort_key(s):
            import re
            return [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', s)]

        sorted_roll_numbers = sorted(existing_data_dict.keys(), key=alphanumeric_sort_key)

        with open(list_file_path, mode='w', newline='') as list_file:
            list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            list_writer.writerow(header)
            for roll_number in sorted_roll_numbers:
                list_writer.writerow(existing_data_dict[roll_number])

        return redirect(url_for('index'))
    return render_template('generate_qr.html')

@app.route('/scan_qr')
def scan_qr():
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    if not os.path.isfile(list_file_path):
        print(f"No student list found at {list_file_path}")
        exit()

 
    with open(list_file_path, mode='r', newline='') as list_file:
        list_reader = csv.reader(list_file)
        header = next(list_reader)
        students_data = {row[0]: row for row in list_reader if row}  

    if current_date not in header:
        header.append(current_date)
        for roll_number in students_data:
            students_data[roll_number].append("A")

    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        list_writer.writerows(students_data.values())

    print(f"Added new column for date {current_date} and marked all as 'A'")

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            RollNumber = data.upper()
            if RollNumber in students_data:
                print(f"{RollNumber} - present")
                students_data[RollNumber][header.index(current_date)] = "P"
                print(f"Attendance marked for {RollNumber} on {current_date}")
                
                with open(list_file_path, mode='w', newline='') as list_file:
                    list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    list_writer.writerow(header)
                    list_writer.writerows(students_data.values())

        cv2.imshow('Show Your QR', img)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/view_data')
def view_data():
    with open(list_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)