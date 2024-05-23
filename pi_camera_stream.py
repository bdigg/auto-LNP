import cv2
import socket
import struct
import numpy as np

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('146.169.153.135', 8080))

# Receive data from the socket
data = b""
payload_size = struct.calcsize("L")

while True:
    try:
        # Receive frame size
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet: 
                break
            data += packet

        if len(data) == payload_size:
            packed_msg_size = data
            data = b""
        else:
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

        # Unpack frame size
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Receive frame data
        while len(data) < msg_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet

        if len(data) == msg_size:
            frame_data = data
            data = b""
        else:
            frame_data = data[:msg_size]
            data = data[msg_size:]

        # Deserialize frame
        frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((1080, 1920, 3))

        # Display frame
        cv2.imshow('Video Stream', frame)
        cv2.waitKey(1)

    except Exception as e:
        print("Error:", e)
        break


