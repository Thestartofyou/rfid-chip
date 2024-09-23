import serial
import csv
import time

# Serial port settings (adjust these as per your RFID reader specs)
SERIAL_PORT = '/dev/ttyUSB0'  # Change this to your port (e.g., COM3 for Windows)
BAUD_RATE = 9600

# CSV file to store the RFID data
CSV_FILE = 'herd_data.csv'

# Function to check if an RFID tag is already logged
def is_tag_logged(rfid_tag):
    with open(CSV_FILE, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if rfid_tag in row:
                return True
    return False

# Function to log RFID tag to the CSV
def log_rfid_tag(rfid_tag):
    if not is_tag_logged(rfid_tag):
        with open(CSV_FILE, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            csv_writer.writerow([rfid_tag, timestamp])
            print(f"RFID tag {rfid_tag} logged at {timestamp}.")
    else:
        print(f"RFID tag {rfid_tag} is already logged.")

def read_rfid():
    # Set up serial connection to RFID reader
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Connected to RFID reader.")
    
    try:
        while True:
            # Read RFID tag from serial
            rfid_tag = ser.readline().decode('utf-8').strip()
            if rfid_tag:
                print(f"RFID tag detected: {rfid_tag}")
                log_rfid_tag(rfid_tag)
                
    except KeyboardInterrupt:
        print("Stopping RFID reader.")
    finally:
        ser.close()

if __name__ == "__main__":
    # Create the CSV file if it doesn't exist
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['RFID Tag', 'Timestamp'])
            print(f"Created new log file: {CSV_FILE}")
    except FileExistsError:
        print(f"Log file {CSV_FILE} already exists. Appending new entries.")

    # Start reading from the RFID reader
    read_rfid()
