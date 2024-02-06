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
db.create_records_table()


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
        self.clear_queue_button = customtkinter.CTkButton(self.sidebar_frame2, text="Clear Queue", command=self.clear_queue)
        self.clear_queue_button.grid(row=9, column=0, sticky="wes", padx=20, pady=(10, 0))


    # create main entry and button
        self.after(1000, self.update_main)

        self.start_button_1 = customtkinter.CTkButton(text="Start",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),font=customtkinter.CTkFont(size=15, weight="bold"), command=ctr.start_process)
        self.start_button_1.grid(row=10, column=1,sticky="nsew",padx=20,pady=(0,20))
        self.stop_button_1 = customtkinter.CTkButton(text="Pause",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=customtkinter.CTkFont(size=15, weight="bold"), command=ctr.stop_process)
        self.stop_button_1.grid(row=10, column=2, sticky="nsew",padx=20,pady=(0,20))
        self.next_button_1 = customtkinter.CTkButton(text="Next",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=customtkinter.CTkFont(size=15, weight="bold"), command=ctr.next_process)
        self.next_button_1.grid(row=10, column=3, sticky="nsew",padx=20,pady=(0,20))
        self.status_label = customtkinter.CTkLabel(master=self,text="Status:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.status_label.grid(row=0, column=1, sticky="nsew",padx=20, columnspan=3)
        self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=1, column=1, columnspan=3, sticky="nsew",padx=(20,100),pady=10)
        self.time_label = customtkinter.CTkLabel(master=self,text="XXs")
        self.time_label.grid(row=1, column=3, sticky="e",padx=(0,60))

        #Ch1
        self.Ch1_label = customtkinter.CTkLabel(master=self,text=("Channel 1"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Ch1_label.grid(row=2, column=1, sticky="nsew",padx=20)
        self.Ch1FR_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.Ch1FR_label.grid(row=3, column=1, sticky="nsew",padx=20)

        #Ch2
        self.Ch2_label = customtkinter.CTkLabel(master=self,text=("Channel 2"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Ch2_label.grid(row=4, column=1, sticky="nsew",padx=20)
        self.Ch2FR_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.Ch2FR_label.grid(row=5, column=1, sticky="nsew",padx=20)

        #Ch3
        self.Ch3_label = customtkinter.CTkLabel(master=self,text=("Channel 3"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Ch3_label.grid(row=6, column=1, sticky="nsew",padx=20)
        self.Ch3FR_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.Ch3FR_label.grid(row=7, column=1, sticky="nsew",padx=20)

        #Ch4
        self.Ch4_label = customtkinter.CTkLabel(master=self,text=("Channel 4"), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Ch4_label.grid(row=8, column=1, sticky="nsew",padx=20)
        self.Ch4FR_label = customtkinter.CTkLabel(master=self,text="Flow Rate")
        self.Ch4FR_label.grid(row=9, column=1, sticky="nsew",padx=20,pady=(0,20))

    def update_main(self):
        #Update status 
        if db.is_experiments_table_empty() == True:
            self.status_label.configure(text = "Status: No Experiments Queued")
        else:
            Exp_name = (db.get_first_experiment_name())
            status = ("Status:", Exp_name)
            self.status_label.configure(text = status)
        #Update Input
            
        #Update Flow Rate and Pressure
        #Update time bar
        #Update activation of buttons
        

    def update_right_sidebar(self):
        for widget in self.sidebar_frame2.winfo_children():
            widget.destroy()
        for self.i, self.exp_name in enumerate(db.get_experiment_names_in_order()):  
            self.queued1 = customtkinter.CTkButton(self.sidebar_frame2, text=self.exp_name, anchor="center", fg_color="transparent", corner_radius=0, border_color="white")
            self.queued1.grid(row=self.i+1, column=0, padx=20, pady=(10, 0))
        self.clear_queue_button = customtkinter.CTkButton(self.sidebar_frame2, text="Clear Queue", command=self.clear_queue)
        self.clear_queue_button.grid(row=9, column=0, sticky="wes", padx=20, pady=(10, 0))
        self.queue_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Queue", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.queue_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #Update left sidebar - activations
        self.after(1000, self.update_main)


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
        self.update_right_sidebar()
        
        print("Queue Cleared")

    def comm_test(self):
        print("Communication Active")

# ---------------------------------------------------------------------------------------------SETUP ----------------------------------------------------------------------
class SetupWindow(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app
        self.app.comm_test(app)
        #self.App = App()
        self.geometry("500x400")
        self.title("Setup")
        self.resizable(False, False)

        #self.grid_columnconfigure((0), weight=1)
        #self.grid_rowconfigure((0), weight=1)
        self.platform_label = customtkinter.CTkLabel(self, text="Setup", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.platform_label.grid(row=0, column=0,sticky="nsew", columnspan=5,padx=(0,0),pady=(5,0))
        
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Pumps", font=customtkinter.CTkFont(size=20,weight="bold"))
        self.setup_pumps_label.grid(row=1,column=0, padx=(0,60))

        self.pump_init_button = customtkinter.CTkButton(self, text="Initialise", command=ctr.setup_initiate)
        self.pump_init_button.grid(row=2, column=0, padx=20, pady=10)

        self.setup_calib_label = customtkinter.CTkLabel(self, text="Calibrate", font=customtkinter.CTkFont(size=20))
        self.setup_calib_label.grid(row=2,column=1, padx=(60,0)) 

        self.setup_calib_button = customtkinter.CTkSegmentedButton(self, values=["Default", "Load", "New"])
        self.setup_calib_button.set("Default")
        self.setup_calib_button.grid(row=2,column=2)

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Inputs", font=customtkinter.CTkFont(size=20,weight="bold"))
        self.setup_pumps_label.grid(row=3,column=0, padx=(0,60), pady=(0,10))

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Reagents", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_pumps_label.grid(row=4,column=0, padx=(0,40), sticky="e")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Concentration", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_pumps_label.grid(row=4,column=1, padx=(0,15), sticky="e")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Volume", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_pumps_label.grid(row=4,column=2, padx=(0,40), sticky="e")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 1", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=5,column=0, sticky="w", padx=(5), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 2", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=6,column=0, sticky="w", padx=(5), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 3", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=7,column=0, sticky="w", padx=(5), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 4", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=8,column=0, sticky="w", padx=(5), pady=(5))


        #Channel 1
        self.R1combobox = customtkinter.CTkComboBox(self, values=ctr.reagents,command=self.R1combo_callback)
        self.R1combobox.grid(row=5,column=0, padx=(0,0),pady=(5),sticky="e")
        global R1comboboxstate
        R1comboboxstate = "normal"
        self.C1combobox = customtkinter.CTkEntry(self,state=R1comboboxstate)
        self.C1combobox.grid(row=5,column=1, padx=(5,0), pady=(5),sticky="e")
        self.V1combobox = customtkinter.CTkEntry(self, state=R1comboboxstate)
        self.V1combobox.grid(row=5,column=2, padx=(5,0),pady=(5), sticky="e")

        #Channel 2#
        self.R2combobox = customtkinter.CTkComboBox(self, values=ctr.reagents, command=self.R1combo_callback)
        self.R2combobox.grid(row=6,column=0, padx=(0,0), pady=(5),sticky="e")
        global R2comboboxstate
        R2comboboxstate = "normal"
        self.C2combobox = customtkinter.CTkEntry(self,state=R2comboboxstate)
        self.C2combobox.grid(row=6,column=1, padx=(5,0), pady=(5),sticky="e")
        self.V2combobox = customtkinter.CTkEntry(self,state=R2comboboxstate)
        self.V2combobox.grid(row=6,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 3
        self.R3combobox = customtkinter.CTkComboBox(self, values=ctr.reagents, command=self.R1combo_callback)
        self.R3combobox.grid(row=7,column=0, padx=(0,0), pady=(5),sticky="e")
        global R3comboboxstate
        R3comboboxstate = "normal"
        self.C3combobox = customtkinter.CTkEntry(self,state=R3comboboxstate)
        self.C3combobox.grid(row=7,column=1, padx=(5,0), pady=(5),sticky="e")
        self.V3combobox = customtkinter.CTkEntry(self,state=R3comboboxstate)
        self.V3combobox.grid(row=7,column=2, padx=(5,0), pady=(5),sticky="e")
        #Channel 4
        self.R4combobox = customtkinter.CTkComboBox(self, values=ctr.reagents, command=self.R1combo_callback)
        self.R4combobox.grid(row=8,column=0, padx=(0,0), pady=(5),sticky="e")
        global R4comboboxstate
        R4comboboxstate = "normal"
        self.C4combobox = customtkinter.CTkEntry(self,state=R4comboboxstate)
        self.C4combobox.grid(row=8,column=1, padx=(5,0), pady=(5),sticky="e")
        self.V4combobox = customtkinter.CTkEntry(self,state=R4comboboxstate)
        self.V4combobox.grid(row=8,column=2, padx=(5,0), pady=(5),sticky="e")
        #Add if load doesnt exist, then grey out

        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.setup_save_event)
        self.save_button.grid(row=9, column=2, sticky="w", pady=(30), padx=(5,0))
        self.setup_name_entry = customtkinter.CTkEntry(self, placeholder_text= "Setup Name")
        self.setup_name_entry.grid(row=9, column=0, sticky="we", pady=(30), padx=(5,0), columnspan=2)

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Error Message:")
        self.setup_pumps_label.grid(row=9,column=1, pady=(0,60),sticky="w")

    def sidebar_button_event(self):
        print("sidebar_button click") 
    
    def setup_calib_event(self):
        print("Noice")

    def segmented_button_callback(self, value):
        print("segmented button clicked:", value)

    def R1combo_callback(self, value):
        if value != "None":
            print("unlock")
            R1comboboxstate = "normal"
        else:
            print("lock")
            R1comboboxstate = "disabled"
            
    def R2combo_callback(self, value):
        print("segmented button clicked:", value)
    def R3combo_callback(self, value):
        print("segmented button clicked:", value)
    def R4combo_callback(self, value):
        print("segmented button clicked:", value)


    def setup_save_event(self):
        print("exit")
        ctr.setup_calib(self.setup_calib_button.get())
        db.create_setups_table()
        global setup_name
        setup_name = self.setup_name_entry.get() #Change this to an input   
        db.create_setup(setup_name, self.R1combobox.get(), self.R2combobox.get(), self.R3combobox.get(), self.R4combobox.get())
        print("Database row:", db.get_setup_info(setup_name))
        self.destroy()


#----------------------------------------------------------------------------------ADD EXPERIMENT------------------------------------------------------------------------------------

class AddExpWindow(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("375x450")
        self.title("Setup")
        self.resizable(False, False)
        self.app = app

        self.platform_label = customtkinter.CTkLabel(self, text="Add Experiment", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.platform_label.grid(row=0, column=0,sticky="nsew",pady=(20,20),columnspan=4)


        self.setup_exp_label = customtkinter.CTkLabel(self, text="Channel", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_exp_label.grid(row=4,column=0, padx=(20), sticky="nsew")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Reagent", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_pumps_label.grid(row=4,column=1, padx=(20), sticky="nsew")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Flow Rate", font=customtkinter.CTkFont(size=15,weight="bold"))
        self.setup_pumps_label.grid(row=4,column=2, padx=(20), sticky="nsew")

        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 1", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=5,column=0, sticky="nesw", padx=(10), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 2", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=6,column=0, sticky="nesw", padx=(10), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 3", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=7,column=0, sticky="nesw", padx=(10), pady=(5))
        self.setup_pumps_label = customtkinter.CTkLabel(self, text="Ch 4", font=customtkinter.CTkFont(size=15))
        self.setup_pumps_label.grid(row=8,column=0, sticky="nesw", padx=(10), pady=(5))


        #Channel 1
        self.R1label = customtkinter.CTkLabel(self, text="-")
        self.R1label.grid(row=5,column=1, padx=(0,0),pady=(5),sticky="nsew")
        self.F1entry = customtkinter.CTkEntry(self)
        self.F1entry.grid(row=5,column=2, padx=(5,0), pady=(5))


        #Channel 2#
        self.R2label = customtkinter.CTkLabel(self, text="-")
        self.R2label.grid(row=6,column=1, padx=(10,10),pady=(5),sticky="nsew")
        self.F2entry = customtkinter.CTkEntry(self)
        self.F2entry.grid(row=6,column=2, padx=(5,0), pady=(5))

        #Channel 3
        self.R3label = customtkinter.CTkLabel(self, text="-")
        self.R3label.grid(row=7,column=1, padx=(10,10),pady=(5),sticky="nsew")
        self.F3entry = customtkinter.CTkEntry(self)
        self.F3entry.grid(row=7,column=2, padx=(5,0), pady=(5))

        #Channel 4
        self.R4label = customtkinter.CTkLabel(self, text="-")
        self.R4label.grid(row=8,column=1, padx=(0,0),pady=(5),sticky="nsew")
        self.F4entry = customtkinter.CTkEntry(self)
        self.F4entry.grid(row=8,column=2, padx=(5,0), pady=(5))

        #Add if load doesnt exist, then grey out

        self.save_button = customtkinter.CTkButton(self, text="Add Single", command=self.addexp_save_event)
        self.save_button.grid(row=10, column=0, sticky="nsew", pady=(5), padx=(10), columnspan=4)

        self.selection = customtkinter.CTkOptionMenu(self, values = (db.get_all_setup_names()), command=self.update_text)
        self.selection.grid(row=1, column=0,sticky="nsew",padx=(50,50),pady=(0,20),columnspan=4)

        self.setup_name_entry = customtkinter.CTkEntry(self, placeholder_text= "Experiment Name")
        self.setup_name_entry.grid(row=9, column=0, sticky="we", pady=(30), padx=(10,0), columnspan=2)
        self.autofill_button = customtkinter.CTkButton(self, text="Auto", command=self.autofill_name)
        self.autofill_button.grid(row=9, column=2, sticky="nsew", pady=(30), padx=(10), columnspan=1)

    def sidebar_button_event(self):
        print("sidebar_button click") 
    
    def setup_calib_event(self):
        print("Noice")

    def segmented_button_callback(self, value):
        print("segmented button clicked:", value)

    def R1combo_callback(self, value):
        print("segmented button clicked:", value)

    def addexp_save_event(self):
        print("Add")
        if self.F1entry.get() != None:
            ctr.exp_ch1(self.F1entry.get())
        if self.F2entry.get() != None:
            ctr.exp_ch2(self.F2entry.get())
        if self.F3entry.get() != None:
            ctr.exp_ch3(self.F3entry.get())
        if self.F4entry.get() != None:
            ctr.exp_ch4(self.F4entry.get())

        self.app
        self.destroy()    

    def update_text(self, choice):
        self.R1label.configure(text = db.get_setup_info(choice)[2])
        self.R2label.configure(text = db.get_setup_info(choice)[3])
        self.R3label.configure(text = db.get_setup_info(choice)[4])
        self.R4label.configure(text = db.get_setup_info(choice)[5])


    def addexp_save_event(self):
        print("save exp")
        db.create_experiments_table()
        experiment_name = self.setup_name_entry.get() #Change this to an input   setup_id, Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow
        db.create_experiment((db.get_setup_id_by_name(self.selection.get())), experiment_name, self.F1entry.get(), self.F2entry.get(), self.F3entry.get(), self.F4entry.get())
        print("Database row:", db.get_experiment_info(experiment_name))
        
    def exit_exp(self):  
        self.destroy()    
    
    def autofill_name(self):
        self.setup_name_entry.delete(0)
        self.setup_name_entry.insert(0,"Experiment A")

if __name__ == "__main__":
    app = App()
    app.mainloop()
