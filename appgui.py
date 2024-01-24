#Install Packages
from tkinter import *
import customtkinter
import tkinter.messagebox
import time
import sys
sys.path.append('./control.py')
import control as ctr


#Setup Gui
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class Controller():
    def __init__(self, app):
        self.app = app
    def buttonclicked(self):
        print("Oi")
        


class App(customtkinter.CTk):
    def __init__(self,master):
        super().__init__()
        
        self.master = master
        self.controller = Controller()

    # configure grid lay]out (4x4)
        self.grid_columnconfigure((0, 4), weight=0)
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10), weight=1)
        self.title("AutoMF")
        self.geometry("1000x600")
        self.resizable(False, False)
        #button = customtkinter.CTkButton(master=self,text="Ey")
        #button.place(relx=0.5, rely=0.5, anchor=CENTER)
        #self.mainloop()
    #sidebar frame left buttons
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=11, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=0)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="AutoMF", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.setup_button = customtkinter.CTkButton(self.sidebar_frame, text="Platform Setup", command=self.open_setup)
        self.setup_button.grid(row=1, column=0, padx=20, pady=10)
        self.setup_window = None
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load Experiments", command=self.open_AddExp)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.addexp_window = None
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Operation Settings", command=self.controller.buttonclicked)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

    #sidebar frame right queue
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame2.grid(row=0, column=4, rowspan=11, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(4, weight=0)
        self.queue_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Queue", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.queue_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Queued step
        #for x in     
        self.queued1 = customtkinter.CTkButton(self.sidebar_frame2, text="-", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued1.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.queued2 = customtkinter.CTkButton(self.sidebar_frame2, text="-", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued2.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.queued3 = customtkinter.CTkButton(self.sidebar_frame2, text="-", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued3.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.queued4 = customtkinter.CTkButton(self.sidebar_frame2, text="-", anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
        self.queued4.grid(row=4, column=0, padx=20, pady=(10, 0))

    # create main entry and button

        self.start_button_1 = customtkinter.CTkButton(text="Start",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),font=customtkinter.CTkFont(size=15, weight="bold"))
        self.start_button_1.grid(row=10, column=1,sticky="nsew",padx=20,pady=(0,20))
        self.stop_button_1 = customtkinter.CTkButton(text="Pause",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=customtkinter.CTkFont(size=15, weight="bold"))
        self.stop_button_1.grid(row=10, column=2, sticky="nsew",padx=20,pady=(0,20))
        self.next_button_1 = customtkinter.CTkButton(text="Next",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=customtkinter.CTkFont(size=15, weight="bold"))
        self.next_button_1.grid(row=10, column=3, sticky="nsew",padx=20,pady=(0,20))
        self.status_label = customtkinter.CTkLabel(master=self,text="Status:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=0, column=2, sticky="nsew",padx=20)
        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=1, column=1, columnspan=3, sticky="nsew",padx=(20,100),pady=10)
        self.status_label = customtkinter.CTkLabel(master=self,text="XXs")
        self.status_label.grid(row=1, column=3, sticky="e",padx=(0,60))

        #Ch1
        self.status_label = customtkinter.CTkLabel(master=self,text="Channel 1", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=2, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=3, column=1, sticky="nsew",padx=20)

        #Ch2
        self.status_label = customtkinter.CTkLabel(master=self,text="Channel 2", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=4, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=5, column=1, sticky="nsew",padx=20)

        #Ch3
        self.status_label = customtkinter.CTkLabel(master=self,text="Channel 3", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=6, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=7, column=1, sticky="nsew",padx=20)

        #Ch4
        self.status_label = customtkinter.CTkLabel(master=self,text="Channel 4", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=8, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=9, column=1, sticky="nsew",padx=20,pady=(0,20))

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    
    def open_setup(self):
        if self.setup_window is None or not self.setup_window.winfo_exists():
            self.setup_window = SetupWindow(self)
            self.setup_window.focus()  # if window exists focus it  
            print("test") # create window if its None or destroyed
        else:
            self.setup_window.focus()
            # if window exists focus it  
            print("test2") 

    def open_AddExp(self):
        if self.addexp_window is None or not self.addexp_window.winfo_exists():
            self.addexp_window = AddExpWindow(self)
            self.addexp_window.focus()  # if window exists focus it  
            print("test") # create window if its None or destroyed
        else:
            self.addexp_window.focus()
            # if window exists focus it  
            print("test2")     

    def sidebar_button_event(self):
        print("sidebar_button click")        

class SetupWindow(customtkinter.CTkToplevel):
    def __init__(setupself, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setupself.geometry("500x400")
        setupself.title("Setup")
        setupself.resizable(False, False)

        #setupself.grid_columnconfigure((0), weight=1)
        #setupself.grid_rowconfigure((0), weight=1)
        setupself.platform_label = customtkinter.CTkLabel(setupself, text="Setup", font=customtkinter.CTkFont(size=30, weight="bold"))
        setupself.platform_label.grid(row=0, column=0,sticky="nsew", columnspan=5)
        
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Pumps", font=customtkinter.CTkFont(size=20,weight="bold"))
        setupself.setup_pumps_label.grid(row=1,column=0, padx=(0,60))

        setupself.pump_init_button = customtkinter.CTkButton(setupself, text="Initialise", command=setupself.setup_calib_event)
        setupself.pump_init_button.grid(row=2, column=0, padx=20, pady=10)

        setupself.setup_calib_label = customtkinter.CTkLabel(setupself, text="Calibrate", font=customtkinter.CTkFont(size=20))
        setupself.setup_calib_label.grid(row=2,column=1, padx=(60,0)) 

        setupself.setup_calib_button = customtkinter.CTkSegmentedButton(setupself, values=["Default", "Load", "New"], command=setupself.segmented_button_callback)
        setupself.setup_calib_button.set("Default")
        setupself.setup_calib_button.grid(row=2,column=2)

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Inputs", font=customtkinter.CTkFont(size=20,weight="bold"))
        setupself.setup_pumps_label.grid(row=3,column=0, padx=(0,60), pady=(0,10))

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Reagents", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=0, padx=(0,40), sticky="e")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Concentration", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=1, padx=(0,15), sticky="e")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Volume", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=2, padx=(0,40), sticky="e")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 1", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=5,column=0, sticky="w", padx=(5), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 2", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=6,column=0, sticky="w", padx=(5), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 3", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=7,column=0, sticky="w", padx=(5), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 4", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=8,column=0, sticky="w", padx=(5), pady=(5))


        #Channel 1
        setupself.R1combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.R1combobox.grid(row=5,column=0, padx=(0,0),pady=(5),sticky="e")
        setupself.C1combobox = customtkinter.CTkEntry(setupself)
        setupself.C1combobox.grid(row=5,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V1combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.V1combobox.grid(row=5,column=2, padx=(5,0),pady=(5), sticky="e")

        #Channel 2#
        setupself.R2combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.R2combobox.grid(row=6,column=0, padx=(0,0), pady=(5),sticky="e")
        setupself.C2combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.C2combobox.grid(row=6,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V2combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.V2combobox.grid(row=6,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 3
        setupself.R3combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.R3combobox.grid(row=7,column=0, padx=(0,0), pady=(5),sticky="e")
        setupself.C3combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.C3combobox.grid(row=7,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V3combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.V3combobox.grid(row=7,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 4
        setupself.R4combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.R4combobox.grid(row=8,column=0, padx=(0,0), pady=(5),sticky="e")
        setupself.C4combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.C4combobox.grid(row=8,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V4combobox = customtkinter.CTkComboBox(setupself, values=["None", "option 2"],command=setupself.R1combo_callback)
        setupself.V4combobox.grid(row=8,column=2, padx=(5,0), pady=(5),sticky="e")
        #Add if load doesnt exist, then grey out

        setupself.save_button = customtkinter.CTkButton(setupself, text="Save", command=setupself.setup_save_event)
        setupself.save_button.grid(row=9, column=1, sticky="w", pady=(30), padx=(5,0))

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Error Message:")
        setupself.setup_pumps_label.grid(row=9,column=1, pady=(0,60),sticky="w")

    def sidebar_button_event(setupself):
        print("sidebar_button click") 
    
    def setup_calib_event(setupself):
        print("Noice")

    def segmented_button_callback(setupself, value):
        print("segmented button clicked:", value)

    def R1combo_callback(setupself, value):
        print("segmented button clicked:", value)

    def setup_save_event(setupself):
        print("exit")
        print(setupself.R1combobox.get())
        print(setupself.R2combobox.get())
        setupself.destroy()

class AddExpWindow(customtkinter.CTkToplevel):
    def __init__(setupself, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setupself.geometry("500x400")
        setupself.title("Setup")
        setupself.resizable(False, False)

        #setupself.grid_columnconfigure((0), weight=1)
        #setupself.grid_rowconfigure((0), weight=1)
        setupself.platform_label = customtkinter.CTkLabel(setupself, text="Add Experiment", font=customtkinter.CTkFont(size=30, weight="bold"))
        setupself.platform_label.grid(row=0, column=0,sticky="nsew",pady=(20,20),columnspan=4)

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Channel", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=0, padx=(20), sticky="nsew")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Reagent", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=1, padx=(20), sticky="nsew")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Flow Rate", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_pumps_label.grid(row=4,column=2, padx=(20), sticky="nsew")

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 1", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=5,column=0, sticky="nesw", padx=(10), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 2", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=6,column=0, sticky="nesw", padx=(10), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 3", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=7,column=0, sticky="nesw", padx=(10), pady=(5))
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Ch 4", font=customtkinter.CTkFont(size=15))
        setupself.setup_pumps_label.grid(row=8,column=0, sticky="nesw", padx=(10), pady=(5))


        #Channel 1
        setupself.R1label = customtkinter.CTkLabel(setupself, text="reagvar1")
        setupself.R1label.grid(row=5,column=1, padx=(0,0),pady=(5),sticky="nsew")
        setupself.F1entry = customtkinter.CTkEntry(setupself)
        setupself.F1entry.grid(row=5,column=2, padx=(5,0), pady=(5),sticky="e")


        #Channel 2#
        setupself.R2label = customtkinter.CTkLabel(setupself, text="reagvar2")
        setupself.R2label.grid(row=6,column=1, padx=(10,10),pady=(5),sticky="nsew")
        setupself.F2entry = customtkinter.CTkEntry(setupself)
        setupself.F2entry.grid(row=6,column=2, padx=(5,0), pady=(5),sticky="e")

        #Channel 3
        setupself.R3label = customtkinter.CTkLabel(setupself, text="reagvar3")
        setupself.R3label.grid(row=7,column=1, padx=(10,10),pady=(5),sticky="nsew")
        setupself.F3entry = customtkinter.CTkEntry(setupself)
        setupself.F3entry.grid(row=7,column=2, padx=(5,0), pady=(5),sticky="e")

        #Channel 4
        setupself.R4label = customtkinter.CTkLabel(setupself, text="reagvar4")
        setupself.R4label.grid(row=8,column=1, padx=(0,0),pady=(5),sticky="nsew")
        setupself.F4entry = customtkinter.CTkEntry(setupself)
        setupself.F4entry.grid(row=8,column=2, padx=(5,0), pady=(5),sticky="e")

        #Add if load doesnt exist, then grey out

        setupself.save_button = customtkinter.CTkButton(setupself, text="Add Single", command=setupself.setup_save_event)
        setupself.save_button.grid(row=5, column=3, sticky="nsew", pady=(30), padx=(10), rowspan=4)

    def sidebar_button_event(setupself):
        print("sidebar_button click") 
    
    def setup_calib_event(setupself):
        print("Noice")

    def segmented_button_callback(setupself, value):
        print("segmented button clicked:", value)

    def R1combo_callback(setupself, value):
        print("segmented button clicked:", value)

    def setup_save_event(setupself):
        print("exit")
        print(setupself.R1combobox.get())
        print(setupself.R2combobox.get())
        setupself.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
