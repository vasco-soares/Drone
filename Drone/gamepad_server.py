import os
import socket
import time
import datetime
import subprocess
import serial

# Serial port configuration
# serial_port = '/dev/ttyUSB0'
# baud_rate = 9600

# Open the serial connection
# try:
#     arduino = serial.Serial(serial_port, baud_rate)
#     print('Serial connection established')
# except serial.SerialException as e:
#     print('Failed to open serial port {}: {}'.format(serial_port, e))
#     exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.1.64', 10000)
print('Starting up on {} port {}'.format(*server_address))

sock.bind(('192.168.1.64', 10000))

# Open a new terminal window to display inputs
subprocess.Popen(['gnome-terminal', '-x', 'python', 'input_display.py'])

# Listen for incoming connections
sock.listen(1)

while True:
    print('Waiting for drone to connect...')
    connection, client_address = sock.accept()
    try:
        print('Client connected from', client_address)
        while True:
            message_from_gamepad = connection.recv(5000)
            if not message_from_gamepad:
                break
            string_commands = message_from_gamepad.decode('utf-8')
            # print('Received input:', string_commands)

            # Save input with timestamp
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            file_path = '/home/firecopter/Desktop/fire/inputs.txt'
            with open(file_path, 'a+') as file:
                file.write(f"{timestamp} - {string_commands}\n")
                file.flush()

            # Check if the received message is a reboot command
            if string_commands.strip() == 'reboot':
                print('Reboot command received. Rebooting Raspberry Pi...')
                # Perform the reboot by executing the reboot command
                os.system('sudo reboot')

            # Check if the received message is "visao"
            if string_commands.strip() == 'visao':
                print('Received "visao" command. Starting visao.py...')
                # Send a response message to the client
                response_msg = 'Starting visao.py...'
                connection.sendall(response_msg.encode())
                # Start the visao.py script
                subprocess.Popen(['python', '/home/firecopter/Desktop/fire/visao.py'])

            # Send the input to Arduino
            # arduino.write(string_commands.encode())
            # time.sleep(0.1)
            # arduino.write('\n'.encode())  # Send a newline character to indicate the end of the input

    except Exception as e:
        print('Error:', e)
    finally:
        connection.close()
