#Install Packages
from tkinter import *
import customtkinter
import tkinter.messagebox
import time


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

    # configure grid layout (4x4)
        self.grid_columnconfigure((0, 4), weight=0)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.title("AutoMF")
        self.geometry("1280x720")
        self.setup_button = customtkinter.CTkButton(self.sidebar_frame, text="Platform Setup", command=self.open_setup)
        self.setup_button.grid(row=1, column=0, padx=20, pady=10)


class SetupWindow(customtkinter.CTkToplevel):
    def __init__(setupself, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setupself.geometry("800x600")
        setupself.title("Setup")
        #setupself.grid_columnconfigure((0), weight=1)
        #setupself.grid_rowconfigure((0), weight=1)