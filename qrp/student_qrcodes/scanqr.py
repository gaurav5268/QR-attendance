import cv2
import datetime
import csv
import os

list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

def scan_qr():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
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
        for roll_number in students_data:
            students_data[roll_number].append("")

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
                if len(students_data[RollNumber]) < len(header):  # If new date column was added
                    students_data[RollNumber].append("P")
                else:
                    students_data[RollNumber][header.index(current_date)] = "P"  # Mark as present
                print(f"Attendance marked for {RollNumber} on {current_date}")

        cv2.imshow('Show Your QR', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Write back all data with the current date column
    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        list_writer.writerows(students_data.values())

if __name__ == "__main__":
    scan_qr()
