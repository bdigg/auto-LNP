#Install Packages
from tkinter import *
import customtkinter
import tkinter.messagebox
import time


#Setup Gui
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

    # configure grid layout (4x4)
        self.grid_columnconfigure((0, 4), weight=0)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.title("AutoMF")
        self.geometry("1280x720")
        #button = customtkinter.CTkButton(master=self,text="Ey")
        #button.place(relx=0.5, rely=0.5, anchor=CENTER)
        #self.mainloop()
    #sidebar frame left buttons
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="AutoMF", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.setup_button = customtkinter.CTkButton(self.sidebar_frame, text="Platform Setup", command=self.open_setup)
        self.setup_button.grid(row=1, column=0, padx=20, pady=10)
        self.setup_window = None
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load Experiments", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Operation Settings", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
    #Tab view
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.tabview.add("tab 1")  # add tab at the end
        self.tabview.add("tab 2")  # add tab at the end
        self.tabview.set("tab 2")  # set currently visible tab

        self.button = customtkinter.CTkButton(master=self.tabview.tab("tab 1"))
        self.button.pack(padx=20, pady=20)

    #sidebar frame right queue
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame2.grid(row=0, column=4, rowspan=4, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(4, weight=0)
        self.queue_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Queue", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.queue_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Queued step
        #for x in     
        self.queued1 = customtkinter.CTkButton(self.sidebar_frame2, text="12X13Y28Z", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued1.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.queued2 = customtkinter.CTkButton(self.sidebar_frame2, text="12X13Y28Z", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued2.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.queued3 = customtkinter.CTkButton(self.sidebar_frame2, text="12X13Y28Z", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued3.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.queued4 = customtkinter.CTkButton(self.sidebar_frame2, text="12X13Y28Z", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued4.grid(row=4, column=0, padx=20, pady=(10, 0))

    # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=2, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    
    def open_setup(self):
        if self.setup_window is None or not self.setup_window.winfo_exists():
            self.setup_window = SetupWindow(self)
            self.setup_window.focus()  # if window exists focus it  
            print("test") # create window if its None or destroyed
        else:
            self.setup_window.focus()  # if window exists focus it  
            print("test2") 


    def sidebar_button_event(self):
        print("sidebar_button click")        



class SetupWindow(customtkinter.CTkToplevel):
    def __init__(setupself, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setupself.geometry("800x600")
        setupself.title("Setup")
        #setupself.grid_columnconfigure((0), weight=1)
        #setupself.grid_rowconfigure((0), weight=1)
        setupself.platform_label = customtkinter.CTkLabel(setupself, text="Setup", font=customtkinter.CTkFont(size=30, weight="bold"))
        setupself.platform_label.grid(row=0, column=0,sticky="ew", columnspan=4)
        
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Pumps", font=customtkinter.CTkFont(size=20))
        setupself.setup_pumps_label.grid(row=1,column=0, padx=20)

        setupself.pump_init_button = customtkinter.CTkButton(setupself, text="Initialise", command=setupself.setup_calib_event)
        setupself.pump_init_button.grid(row=2, column=0, padx=20, pady=10)

        setupself.setup_calib_label = customtkinter.CTkLabel(setupself, text="Calibrate", font=customtkinter.CTkFont(size=20))
        setupself.setup_calib_label.grid(row=2,column=2, padx=20) 

        setupself.setup_calib_button = customtkinter.CTkSegmentedButton(setupself, values=["Default", "Load", "New"], command=setupself.segmented_button_callback)
        setupself.setup_calib_button.set("Default")
        
        setupself.setup_calib_button.grid(row=2,column=3)

        #Add if load doesnt exist, then grey out

    def sidebar_button_event(setupself):
        print("sidebar_button click") 
    
    def setup_calib_event(setupself):
        print("Noice")

    def segmented_button_callback(setupself, value):
        print("segmented button clicked:", value)


if __name__ == "__main__":
    app = App()
    app.mainloop()
