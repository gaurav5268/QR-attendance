import pyqrcode
import png
import cv2
import datetime
import csv
import os
import subprocess


list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

print("Hi-----")
print("1) To generate a QR for New Student")
print("2) To scan a QR from the Student")
print("----")

userinput = input("Select a Number: ")

if userinput == "1":
    no_of_students = int(input("Enter No. of Students: "))

    # Open the file in read mode to get the existing data
    with open(list_file_path, mode='r', newline='') as list_file:
        list_reader = csv.reader(list_file)
        existing_data = [row for row in list_reader]

    # Extract the header and data separately
    header = existing_data[0]
    existing_data_dict = {row[0]: row for row in existing_data[1:]}

    new_roll_numbers = []
    for i in range(no_of_students):
        RollNumber = input("Enter Student RollNumber: ").upper()
        if RollNumber not in existing_data_dict:
            url = pyqrcode.create(RollNumber)
            qr_code_path = f"C:\\Users\\Gravity\\Desktop\\qrp\\student_qrcodes\\{RollNumber}.png"
            url.png(qr_code_path, scale=6)
            qr_code_hyperlink = f'=HYPERLINK({qr_code_path}, "Image")'
            print("QR Generated Successfully")
            new_roll_numbers.append([RollNumber, qr_code_hyperlink])
        else:
            print(f"Roll number {RollNumber} already exists. Skipping QR code generation.")

    # Merge new roll numbers into existing data
    for new_row in new_roll_numbers:
        existing_data_dict[new_row[0]] = new_row

    def alphanumeric_sort_key(s):
        # Split the string into a list of integers and non-integer parts
        import re
        return [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', s)]

    # Sort the roll numbers using the custom alphanumeric sort key
    sorted_roll_numbers = sorted(existing_data_dict.keys(), key=alphanumeric_sort_key)

    # Write back all data including new and existing sorted by roll number
    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        for roll_number in sorted_roll_numbers:
            list_writer.writerow(existing_data_dict[roll_number])


elif userinput == "2":
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    if not os.path.isfile(list_file_path):
        print(f"No student list found at {list_file_path}")
        exit()

    # Open the file in read mode to get the existing data
    with open(list_file_path, mode='r', newline='') as list_file:
        list_reader = csv.reader(list_file)
        header = next(list_reader)
        students_data = {row[0]: row for row in list_reader if row}  # Ensure non-empty rows are read

    # Check if today's date column exists, if not add it
    if current_date not in header:
        header.append(current_date)

    # Write back the updated data with the new date column
    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        list_writer.writerows(students_data.values())

    print(f"Added new column for date {current_date}")
        
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            RollNumber = data.upper()
            if RollNumber in students_data:
                print(f"{RollNumber} - present")
                if len(students_data[RollNumber]) < len(header):
                    students_data[RollNumber].append("P")
                else:
                    students_data[RollNumber][header.index(current_date)] = "P"
                print(f"Attendance marked")
                
                with open(list_file_path, mode='w', newline='') as list_file:
                    list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    list_writer.writerow(header)
                    list_writer.writerows(students_data.values())
                    
            else:
                print(f"{RollNumber} not found in the list.")

        cv2.imshow('Show Your QR', img)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    # Close camera and windows
    cap.release()
    cv2.destroyAllWindows()

elif userinput == "3":
    # Run the Flask app to show the CSV data
    print("Starting Flask server to display CSV data...")
    subprocess.run(["python", "visual.py"])

else:
    print("Select a valid number")
