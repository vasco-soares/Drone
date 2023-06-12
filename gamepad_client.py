import socket
import json
import pygame
import time
import sys

pygame.init()
pygame.joystick.init()

# Get the first connected joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.64', 10001)
print('connecting to {} port {}'.format(*server_address))
try:
    sock.connect(server_address)
except ConnectionRefusedError:
    print('Connection refused. Please check the server address and port.')
    exit()

# Initialization
pygame.init()
pygame.joystick.init()

# Get count of joysticks
joystick_count = pygame.joystick.get_count()
print('Found ' + str(joystick_count) + ' joysticks.')

# Check if joystick is connected
if joystick_count == 0:
    print('No joystick found. Please connect a joystick and try again.')
    exit()

# init joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Get the name from the OS for the controller/joystick
joystick_name = joystick.get_name()
print('Connected to ' + joystick_name)

while True:
     # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    try:
        # Get the axis values from joystick 1
        axis0_1 = joystick.get_axis(0)
        axis1_1 = joystick.get_axis(1)

        # Get the axis values from joystick 2
        axis0_2 = joystick.get_axis(2)
        axis1_2 = joystick.get_axis(3)

        # Get the trigger values
        lt = joystick.get_axis(2)
        rt = joystick.get_axis(5)

        # Get the button values
        a_button = joystick.get_button(0)
        b_button = joystick.get_button(1)
        x_button = joystick.get_button(2)
        y_button = joystick.get_button(3)
        lb_button = joystick.get_button(4)
        rb_button = joystick.get_button(5)
        back_button = joystick.get_button(6)
        start_button = joystick.get_button(7)

        # Print the axis values
        #print("Joystick 1 - Axis 0:", axis0_1)
        #print("Joystick 1 - Axis 1:", axis1_1)
        #print("Joystick 2 - Axis 2:", axis0_2)
        #print("Joystick 2 - Axis 3:", axis1_2)
        #print("LT:", lt)
        #print("RT:", rt)
        #print("A button:", a_button)
        #print("B button:", b_button)
        #print("X button:", x_button)
        #print("Y button:", y_button)
        #print("LB button:", lb_button)
        #print("RB button:", rb_button)
        #print("Back button:", back_button)
        #print("Start button:", start_button)
        # Create a dictionary with the joystick inputs
        joystick_data = {
            'axis0_1': axis0_1,
            'axis1_1': axis1_1,
            'axis0_2': axis0_2,
            'axis1_2': axis1_2,
            'lt': lt,
            'rt': rt,
            'a_button': a_button,
            'b_button': b_button,
            'x_button': x_button,
            'y_button': y_button,
            'lb_button': lb_button,
            'rb_button': rb_button,
            'back_button': back_button,
            'start_button': start_button
        }

        # Convert the dictionary to a JSON string
        joystick_json = json.dumps(joystick_data)

        # Send the JSON string to the server
        sock.sendall(joystick_json.encode())

        # Wait for a short time before sending the next update
        time.sleep(0.1)

    except:
        print('Error getting the inputs')
