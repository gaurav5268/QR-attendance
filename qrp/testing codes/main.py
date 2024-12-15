import pyqrcode
import png
import cv2
import datetime
import csv
import os

list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

print("Hi-----")
print("1) To generate a QR for New Student")
print("2) To scan a QR from the Student")
print("----")

userinput = input("Select a Number: ")

if userinput == "1":
    no_of_students = int(input("Enter No. of Students: "))
    if not os.path.isfile(list_file_path):
        with open(list_file_path, mode='w', newline='') as list_file:
            list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            list_writer.writerow(["ROLL NO", "QR CODE"])
    
    with open(list_file_path, mode='r+', newline='') as list_file:
        list_reader = csv.reader(list_file)
        existing_data = {row[0]: row for row in list_reader if row}  # Ensure non-empty rows are read
        
        new_roll_numbers = []
        for i in range(no_of_students):
            RollNumber = input("Enter Student RollNumber: ").upper()
            if RollNumber not in existing_data:
                url = pyqrcode.create(RollNumber)
                qr_code_path = f"C:\\Users\\Gravity\\Desktop\\qrp\\student_qrcodes\\{RollNumber}.png"
                url.png(qr_code_path, scale=6)
                qr_code_hyperlink = f'=HYPERLINK("{qr_code_path}", "Image")'
                print("QR Generated Successfully")
                new_roll_numbers.append([RollNumber, qr_code_hyperlink])
            else:
                print(f"Roll number {RollNumber} already exists. Skipping QR code generation.")
                
        for new_row in new_roll_numbers:
            existing_data[new_row[0]] = new_row
        
        sorted_data = sorted(existing_data.values(), key=lambda x: x[0])
        
        list_file.seek(0)
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(["ROLL NO", "QR CODE"])
        list_writer.writerows(sorted_data)
        list_file.truncate()
            
elif userinput == "2":
    if not os.path.isfile(list_file_path):
        print(f"No student list found at {list_file_path}")
        exit()

    with open(list_file_path, mode='r', newline='') as list_file:
        list_reader = csv.reader(list_file)
        header = next(list_reader)
        students_data = {row[0]: row for row in list_reader if row}  # Ensure non-empty rows are read

    # Check if today's date column exists, if not add it
    today_date = datetime.datetime.now().strftime("%d-%m-%Y")
    if today_date not in header:
        header.append(today_date)
        for roll_number in students_data:
            students_data[roll_number].append("")

    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            RollNumber = data.upper()
            if RollNumber in students_data:
                print(f"{RollNumber} - present")
                if len(students_data[RollNumber]) < len(header):  # If new date column was added
                    students_data[RollNumber].append("P")
                else:
                    students_data[RollNumber][header.index(today_date)] = "P"  # Mark as present
                print(f"Attendance marked for {RollNumber} on {today_date}")
        
        cv2.imshow('Show Your QR', img)
        
        if cv2.waitKey(1) == ord('q'):
            break

    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        list_writer.writerows(students_data.values())

    cap.release()
    cv2.destroyAllWindows()

else:
    print("Select a valid number")
