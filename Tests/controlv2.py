import pump as press
import time
import CTkGUI.db as db 
import CTkGUI.appgui as App
from queue import Queue
from threading import Thread

class Control(Thread):
    def __init__(self, queue_from_gui, queue_to_gui):
        super().__init__()
        self.queue_from_gui = queue_from_gui
        self.queue_to_gui = queue_to_gui
        self.stop_event = False

    def run(self):
        while not self.stop_event:
            # Check if there are messages from GUI
            while not self.queue_from_gui.empty():
                gui_message = self.queue_from_gui.get()
                # Process GUI message, for example, print it
                print("Received message from GUI:", gui_message)

            # Perform backend tasks
            # Simulate backend work
            data = {"key": "value"}  # Example data with key
            self.queue_to_gui.put(data)

            # Simulate backend processing time
            time.sleep(1)

    def stop(self):
        self.stop_event = True


