#Install Packages
from tkinter import *
import customtkinter
import tkinter.messagebox
import time
import sys
sys.path.append('./control.py')
import Tests.controlv2 as ctr
from Tests.controlv2 import Control
import threading
import db 
from queue import Queue

#Setup Gui
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

"""def Func(host,cursor,db):
    try:
        lock.acquire(True)
        res = cursor.execute('''...''',(host,))
        # do something
    finally:
        lock.release()"""


class Controller():
    def __init__(self, app, queue_to_control):
        self.app = app
        self.queue_to_control = queue_to_control

    def buttonclicked(self):
        print("Oi")
        # Example of sending message to control
        self.queue_to_control.put("Button clicked")


class App(customtkinter.CTk):
    def __init__(self, queue_to_control, queue_from_control):
        super().__init__()
        self.queue_to_control = queue_to_control
        self.queue_from_control = queue_from_control

        self.label = customtkinter.CTkLabel(self, text="Waiting for message from backend")
        self.label.pack()

        self.controller = Controller(self, self.queue_to_control)
        self.controller.buttonclicked()

        # Start checking queue from control
        self.after(100, self.check_queue)

        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 4), weight=0)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10), weight=1)
        self.title("AutoMF")
        self.geometry("1000x600")
        self.resizable(False, False)

    def check_queue(self):
        while not self.queue_from_control.empty():
            message = self.queue_from_control.get()
            # Process message received from control
            self.label.config(text=message)
        self.after(100, self.check_queue)

class SetupWindow(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

        # Assuming you want to send a message from setup to control
        self.app.queue_to_control.put("Message from Setup Window")

        self.geometry("500x400")
        self.title("Setup")
        self.resizable(False, False)

if __name__ == "__main__":
    # Create queues for communication
    gui_to_control_queue = Queue()
    control_to_gui_queue = Queue()

    # Create GUI and Control instances, passing queues
    app = App(gui_to_control_queue, control_to_gui_queue)
    control = Control(control_to_gui_queue, gui_to_control_queue)

    # Start Control thread
    control.start()

    # Start GUI main loop
    app.mainloop()
