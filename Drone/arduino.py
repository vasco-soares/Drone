import serial

# Configure the serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Update the port and baud rate based on your setup

# Prompt for two numbers
number1 = int(input("Enter number 1: "))
number2 = int(input("Enter number 2: "))

# Send the numbers to the Arduino
ser.write(str(number1).encode())
ser.write(b'\n')  # Send a newline character to mark the end of the number
ser.write(str(number2).encode())
ser.write(b'\n')

			# Wait for the Arduino's response
			response = ser.readline().decode().strip()
			print("Arduino response:", response)

# Close the serial connection
ser.close()
