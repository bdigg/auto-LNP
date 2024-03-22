from queue import Queue
from threading import Thread
import time  # Importing time for sleep function
import Tests.appguiv2 as appguiv2

class Backend(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.gui_queue = Queue()  # Queue for sending messages to the GUI
        self.stop_event = False

    def run(self):
        while not self.stop_event:
            # Simulate backend work
            data = {"key": "value"}  # Example data with key
            self.queue.put(data)

            # Check if there are messages to send to the GUI
            while not self.gui_queue.empty():
                gui_message = self.gui_queue.get()
                # Process GUI message, for example, print it
                print("Received message from GUI:", gui_message)

            # Simulate backend processing time
            time.sleep(1)

    def send_to_gui(self, message):
        self.gui_queue.put(message)

    def stop(self):
        self.stop_event = True
