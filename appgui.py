#Install Packages
from tkinter import *
import customtkinter
import tkinter.messagebox
import time
import sys
sys.path.append('./control.py')
import control as ctr
import threading
import db 

#Setup Gui
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

#Preset Vars

db.create_connection()
db.create_setups_table()
db.create_experiments_table()


class Controller():
    def __init__(self, app):
        self.app = app
    def buttonclicked(self):
        print("Oi")
        


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.controller = Controller(self)
        self.controller.buttonclicked()

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
        loadexpstate, opsetstate = "normal","disabled"
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load Experiments", command=self.open_AddExp, state=loadexpstate)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.addexp_window = None
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Operation Settings", command=self.controller.buttonclicked, state=opsetstate)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

    #sidebar frame right queue
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame2.grid(row=0, column=4, rowspan=11, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(4, weight=0)
        self.queue_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Queue", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.queue_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Queued step
        for self.i, self.exp_name in enumerate(db.get_experiment_names_in_order()):  
            self.queued1 = customtkinter.CTkButton(self.sidebar_frame2, text=self.exp_name, anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
            self.queued1.grid(row=self.i+1, column=0, padx=20, pady=(10, 0))

        print(db.get_experiment_names_in_order())
        self.clear_queue_button = customtkinter.CTkButton(self.sidebar_frame2, text="Clear Queue", command=self.clear_queue)
        self.clear_queue_button.grid(row=9, column=0, sticky="wes", padx=20, pady=(10, 0))


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
        self.status_label = customtkinter.CTkLabel(master=self,text=("Channel 1"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=2, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=3, column=1, sticky="nsew",padx=20)

        #Ch2
        self.status_label = customtkinter.CTkLabel(master=self,text=("Channel 2"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=4, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=5, column=1, sticky="nsew",padx=20)

        #Ch3
        self.status_label = customtkinter.CTkLabel(master=self,text=("Channel 3"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=6, column=1, sticky="nsew",padx=20)
        self.status_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.status_label.grid(row=7, column=1, sticky="nsew",padx=20)

        #Ch4
        self.status_label = customtkinter.CTkLabel(master=self,text=("Channel 4"), font=customtkinter.CTkFont(size=20, weight="bold"))
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

    def rename_setups():
        print("oi")

    def clear_queue(self):
        db.delete_all_experiments()
        
        print("Queue Cleared")

# ---------------------------------------------------------------------------------------------SETUP ----------------------------------------------------------------------
class SetupWindow(customtkinter.CTkToplevel):
    def __init__(setupself, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #setupself.App = App()
        setupself.geometry("500x400")
        setupself.title("Setup")
        setupself.resizable(False, False)

        #setupself.grid_columnconfigure((0), weight=1)
        #setupself.grid_rowconfigure((0), weight=1)
        setupself.platform_label = customtkinter.CTkLabel(setupself, text="Setup", font=customtkinter.CTkFont(size=30, weight="bold"))
        setupself.platform_label.grid(row=0, column=0,sticky="nsew", columnspan=5,padx=(0,0),pady=(5,0))
        
        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Pumps", font=customtkinter.CTkFont(size=20,weight="bold"))
        setupself.setup_pumps_label.grid(row=1,column=0, padx=(0,60))

        setupself.pump_init_button = customtkinter.CTkButton(setupself, text="Initialise", command=ctr.setup_initiate)
        setupself.pump_init_button.grid(row=2, column=0, padx=20, pady=10)

        setupself.setup_calib_label = customtkinter.CTkLabel(setupself, text="Calibrate", font=customtkinter.CTkFont(size=20))
        setupself.setup_calib_label.grid(row=2,column=1, padx=(60,0)) 

        setupself.setup_calib_button = customtkinter.CTkSegmentedButton(setupself, values=["Default", "Load", "New"])
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
        setupself.R1combobox = customtkinter.CTkComboBox(setupself, values=ctr.reagents,command=setupself.R1combo_callback)
        setupself.R1combobox.grid(row=5,column=0, padx=(0,0),pady=(5),sticky="e")
        global R1comboboxstate
        R1comboboxstate = "normal"
        setupself.C1combobox = customtkinter.CTkEntry(setupself,state=R1comboboxstate)
        setupself.C1combobox.grid(row=5,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V1combobox = customtkinter.CTkEntry(setupself, state=R1comboboxstate)
        setupself.V1combobox.grid(row=5,column=2, padx=(5,0),pady=(5), sticky="e")

        #Channel 2#
        setupself.R2combobox = customtkinter.CTkComboBox(setupself, values=ctr.reagents, command=setupself.R1combo_callback)
        setupself.R2combobox.grid(row=6,column=0, padx=(0,0), pady=(5),sticky="e")
        global R2comboboxstate
        R2comboboxstate = "normal"
        setupself.C2combobox = customtkinter.CTkEntry(setupself,state=R2comboboxstate)
        setupself.C2combobox.grid(row=6,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V2combobox = customtkinter.CTkEntry(setupself,state=R2comboboxstate)
        setupself.V2combobox.grid(row=6,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 3
        setupself.R3combobox = customtkinter.CTkComboBox(setupself, values=ctr.reagents, command=setupself.R1combo_callback)
        setupself.R3combobox.grid(row=7,column=0, padx=(0,0), pady=(5),sticky="e")
        global R3comboboxstate
        R3comboboxstate = "normal"
        setupself.C3combobox = customtkinter.CTkEntry(setupself,state=R3comboboxstate)
        setupself.C3combobox.grid(row=7,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V3combobox = customtkinter.CTkEntry(setupself,state=R3comboboxstate)
        setupself.V3combobox.grid(row=7,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 4
        setupself.R4combobox = customtkinter.CTkComboBox(setupself, values=ctr.reagents, command=setupself.R1combo_callback)
        setupself.R4combobox.grid(row=8,column=0, padx=(0,0), pady=(5),sticky="e")
        global R4comboboxstate
        R4comboboxstate = "normal"
        setupself.C4combobox = customtkinter.CTkEntry(setupself,state=R4comboboxstate)
        setupself.C4combobox.grid(row=8,column=1, padx=(5,0), pady=(5),sticky="e")
        setupself.V4combobox = customtkinter.CTkEntry(setupself,state=R4comboboxstate)
        setupself.V4combobox.grid(row=8,column=2, padx=(5,0), pady=(5),sticky="e")
        #Add if load doesnt exist, then grey out

        setupself.save_button = customtkinter.CTkButton(setupself, text="Save", command=setupself.setup_save_event)
        setupself.save_button.grid(row=9, column=2, sticky="w", pady=(30), padx=(5,0))
        setupself.setup_name_entry = customtkinter.CTkEntry(setupself, placeholder_text= "Setup Name")
        setupself.setup_name_entry.grid(row=9, column=0, sticky="we", pady=(30), padx=(5,0), columnspan=2)

        setupself.setup_pumps_label = customtkinter.CTkLabel(setupself, text="Error Message:")
        setupself.setup_pumps_label.grid(row=9,column=1, pady=(0,60),sticky="w")

    def sidebar_button_event(setupself):
        print("sidebar_button click") 
    
    def setup_calib_event(setupself):
        print("Noice")

    def segmented_button_callback(setupself, value):
        print("segmented button clicked:", value)

    def R1combo_callback(setupself, value):
        if value != "None":
            print("unlock")
            R1comboboxstate = "normal"
        else:
            print("lock")
            R1comboboxstate = "disabled"
            
    def R2combo_callback(setupself, value):
        print("segmented button clicked:", value)
    def R3combo_callback(setupself, value):
        print("segmented button clicked:", value)
    def R4combo_callback(setupself, value):
        print("segmented button clicked:", value)


    def setup_save_event(setupself):
        print("exit")
        ctr.setup_calib(setupself.setup_calib_button.get())
        db.create_setups_table()
        global setup_name
        setup_name = setupself.setup_name_entry.get() #Change this to an input   
        db.create_setup(setup_name, setupself.R1combobox.get(), setupself.R2combobox.get(), setupself.R3combobox.get(), setupself.R4combobox.get())
        print("Database row:", db.get_setup_info(setup_name))
        setupself.destroy()

#----------------------------------------------------------------------------------ADD EXPERIMENT------------------------------------------------------------------------------------

class AddExpWindow(customtkinter.CTkToplevel):
    def __init__(setupself, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setupself.geometry("375x450")
        setupself.title("Setup")
        setupself.resizable(False, False)

        setupself.platform_label = customtkinter.CTkLabel(setupself, text="Add Experiment", font=customtkinter.CTkFont(size=30, weight="bold"))
        setupself.platform_label.grid(row=0, column=0,sticky="nsew",pady=(20,20),columnspan=4)


        setupself.setup_exp_label = customtkinter.CTkLabel(setupself, text="Channel", font=customtkinter.CTkFont(size=15,weight="bold"))
        setupself.setup_exp_label.grid(row=4,column=0, padx=(20), sticky="nsew")

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
        setupself.R1label = customtkinter.CTkLabel(setupself, text="-")
        setupself.R1label.grid(row=5,column=1, padx=(0,0),pady=(5),sticky="nsew")
        setupself.F1entry = customtkinter.CTkEntry(setupself)
        setupself.F1entry.grid(row=5,column=2, padx=(5,0), pady=(5))


        #Channel 2#
        setupself.R2label = customtkinter.CTkLabel(setupself, text="-")
        setupself.R2label.grid(row=6,column=1, padx=(10,10),pady=(5),sticky="nsew")
        setupself.F2entry = customtkinter.CTkEntry(setupself)
        setupself.F2entry.grid(row=6,column=2, padx=(5,0), pady=(5))

        #Channel 3
        setupself.R3label = customtkinter.CTkLabel(setupself, text="-")
        setupself.R3label.grid(row=7,column=1, padx=(10,10),pady=(5),sticky="nsew")
        setupself.F3entry = customtkinter.CTkEntry(setupself)
        setupself.F3entry.grid(row=7,column=2, padx=(5,0), pady=(5))

        #Channel 4
        setupself.R4label = customtkinter.CTkLabel(setupself, text="-")
        setupself.R4label.grid(row=8,column=1, padx=(0,0),pady=(5),sticky="nsew")
        setupself.F4entry = customtkinter.CTkEntry(setupself)
        setupself.F4entry.grid(row=8,column=2, padx=(5,0), pady=(5))

        #Add if load doesnt exist, then grey out

        setupself.save_button = customtkinter.CTkButton(setupself, text="Add Single", command=setupself.addexp_save_event)
        setupself.save_button.grid(row=10, column=0, sticky="nsew", pady=(5), padx=(10), columnspan=4)

        setupself.selection = customtkinter.CTkOptionMenu(setupself, values = (db.get_all_setup_names()), command=setupself.update_text)
        setupself.selection.grid(row=1, column=0,sticky="nsew",padx=(50,50),pady=(0,20),columnspan=4)

        setupself.setup_name_entry = customtkinter.CTkEntry(setupself, placeholder_text= "Experiment Name")
        setupself.setup_name_entry.grid(row=9, column=0, sticky="we", pady=(30), padx=(10,0), columnspan=2)
        setupself.autofill_button = customtkinter.CTkButton(setupself, text="Auto", command=setupself.autofill_name)
        setupself.autofill_button.grid(row=9, column=2, sticky="nsew", pady=(30), padx=(10), columnspan=1)


    def sidebar_button_event(setupself):
        print("sidebar_button click") 
    
    def setup_calib_event(setupself):
        print("Noice")

    def segmented_button_callback(setupself, value):
        print("segmented button clicked:", value)

    def R1combo_callback(setupself, value):
        print("segmented button clicked:", value)

    def addexp_save_event(setupself):
        print("Add")
        if setupself.F1entry.get() != None:
            ctr.exp_ch1(setupself.F1entry.get())
        if setupself.F2entry.get() != None:
            ctr.exp_ch2(setupself.F2entry.get())
        if setupself.F3entry.get() != None:
            ctr.exp_ch3(setupself.F3entry.get())
        if setupself.F4entry.get() != None:
            ctr.exp_ch4(setupself.F4entry.get())

        setupself.app
        setupself.destroy()    

    def update_text(setupself, choice):
        setupself.R1label.configure(text = db.get_setup_info(choice)[2])
        setupself.R2label.configure(text = db.get_setup_info(choice)[3])
        setupself.R3label.configure(text = db.get_setup_info(choice)[4])
        setupself.R4label.configure(text = db.get_setup_info(choice)[5])


    def addexp_save_event(setupself):
        print("save exp")
        db.create_experiments_table()
        experiment_name = setupself.setup_name_entry.get() #Change this to an input   setup_id, Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow
        db.create_experiment((db.get_setup_id_by_name(setupself.selection.get())), experiment_name, setupself.F1entry.get(), setupself.F2entry.get(), setupself.F3entry.get(), setupself.F4entry.get())
        print("Database row:", db.get_experiment_info(experiment_name))
        
    def exit_exp(setupself):  
        setupself.destroy()    
    
    def autofill_name(setupself):
        setupself.setup_name_entry.delete(0)
        setupself.setup_name_entry.insert(0,"Experiment A")

if __name__ == "__main__":
    app = App()
    app.mainloop()
