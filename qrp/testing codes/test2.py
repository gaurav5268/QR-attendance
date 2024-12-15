import pyqrcode
import png
import cv2
import datetime
import csv
import os
import base64

list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

print("Hi-----")
print("1) To generate a QR for New Student")
print("2) To scan a QR from the Student")
print("----")

userinput = input("Select a Number: ")

def save_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def save_base64_as_image(encoded_string, image_path):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    with open(image_path, "wb") as image_file:
        image_file.write(decoded_bytes)

if userinput == "1":
    no_of_students = int(input("Enter No. of Students: "))
    if not os.path.isfile(list_file_path):
        with open(list_file_path, mode='w', newline='') as list_file:
            list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            list_writer.writerow(["ROLL NO", "QR CODE", "ATTENDANCE"])
    
    with open(list_file_path, mode='r+', newline='') as list_file:
        list_reader = csv.reader(list_file)
        existing_data = {row[0]: row for row in list_reader}
        
        new_roll_numbers = []
        for i in range(no_of_students):
            RollNumber = input("Enter Student RollNumber: ").upper()
            if RollNumber not in existing_data:
                url = pyqrcode.create(RollNumber)
                qr_code_path = f"C:\\Users\\Gravity\\Desktop\\qrp\\student_qrcodes\\{RollNumber}.png"
                url.png(qr_code_path, scale=6)
                qr_code_base64 = save_image_as_base64(qr_code_path)
                print("QR Generated Successfully")
                new_roll_numbers.append((RollNumber, qr_code_base64, ""))
            else:
                print(f"Roll number {RollNumber} already exists. Skipping QR code generation.")
                
        for roll_number, qr_code_base64, _ in new_roll_numbers:
            existing_data[roll_number] = [roll_number, qr_code_base64, ""]
        
        sorted_data = sorted(existing_data.values(), key=lambda x: x[0])
        
        list_file.seek(0)
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(["ROLL NO", "QR CODE", "ATTENDANCE"])
        list_writer.writerows(sorted_data)
        list_file.truncate()
            
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

else:
    print("Select a valid number")
