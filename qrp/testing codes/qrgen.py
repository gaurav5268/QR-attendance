import pyqrcode
import png
import csv
import os
import re

list_file_path = "C:\\Users\\Gravity\\Desktop\\qrp\\list.csv"

def generate_qr():
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
            qr_code_hyperlink = f'=HYPERLINK("{qr_code_path}", "Image")'
            print("QR Generated Successfully")
            new_roll_numbers.append([RollNumber, qr_code_hyperlink])
        else:
            print(f"Roll number {RollNumber} already exists. Skipping QR code generation.")

    # Merge new roll numbers into existing data
    for new_row in new_roll_numbers:
        existing_data_dict[new_row[0]] = new_row

    def alphanumeric_sort_key(s):
        # Split the string into a list of integers and non-integer parts
        return [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', s)]

    # Sort the roll numbers using the custom alphanumeric sort key
    sorted_roll_numbers = sorted(existing_data_dict.keys(), key=alphanumeric_sort_key)

    # Write back all data including new and existing sorted by roll number
    with open(list_file_path, mode='w', newline='') as list_file:
        list_writer = csv.writer(list_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        list_writer.writerow(header)
        for roll_number in sorted_roll_numbers:
            list_writer.writerow(existing_data_dict[roll_number])

if __name__ == "__main__":
    generate_qr()
