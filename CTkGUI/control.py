import pump as press
import time
import CTkGUI.db as db 
import CTkGUI.appgui as App
from queue import Queue


pstate = False
reagents = ["None","DPPC","DOPC","LysoPC","Chol","Buffer"]
def main_loop():
    while True:
        print("main loop")
        time.sleep(1)

db.create_connection()
db.create_setups_table()
db.create_experiments_table()

def start_process():
    print("Starting")
    if db.is_experiments_table_empty() == True:
        print("No queued experiments - start")
    else:
        #if db.get_status_from_first_experiment() == "Paused":
        #    experiment_t  = db.get_time_remaining_for_first_experiment() 
        #else:
        #    
        experiment_t = 20
        next_exp = db.get_experiment_names_in_order()[0] #Check that this is getting creation order not alphabetical]
        next_exp_info = db.get_experiment_info(next_exp)
        start_t = time.time()
        db.change_status_of_first_experiment("Active")
        if pstate == True:
                #Set pump pressure
                press.set_flow1(1,next_exp_info[2])
                press.set_flow1(2,next_exp_info[3])
                press.set_flow1(3,next_exp_info[4])
                press.set_flow1(4,next_exp_info[5])
                print("Set flow - X")
                #Collect Experiment Data
        while True:
            #App.App.update(self)
            # Check if the elapsed time match the time limit
            if (time.time() - start_t) > experiment_t:
                break
            if db.get_status_from_first_experiment() == "Paused":
                db.set_time_remaining_for_first_experiment(experiment_t - time.time - start_t)
                remaining_t = experiment_t - time.time - start_t
                break 
                #Collect Experiment Dats
                #press.set_pressure()
        if pstate == True:
            #Set pump pressure
            press.set_flow1(1,0)
            press.set_flow1(2,0)
            press.set_flow1(3,0)
            press.set_flow1(4,0)
            print("Set flow - 0")
        db.change_status_of_first_experiment("Finished")        
        #if remaining_t <= 0:
        #    next_process()
        

def next_process():
    #Save experiment data to another database
    print("Next process")
    if db.is_experiments_table_empty() == True:
        print("No queued experiments - next")
        stop_process()
    else:
        prev_exp_id = db.get_experiment_ids_in_order()[0]
        print("Previous exp id:",prev_exp_id)
        print(db.get_experiment_info_with_id(prev_exp_id))
        prev_exp_setup_id = (db.get_experiment_info_with_id(prev_exp_id))[6]
        db.copy_setup_and_experiment_to_record(prev_exp_setup_id,prev_exp_id)
        print(db.get_records_info(prev_exp_id)) 
        #Remove from queue db
        db.delete_experiment_by_id(prev_exp_id)
        #Call start for next experiment
        start_process()

def stop_process():
    print("Stawwwwwp")
    db.change_status_of_first_experiment("Paused")

def setup_initiate():
    print("Initialising Setup")
    if pstate == True:
        press.pressure_init()
    #Grey out button after initalisation 

def setup_calib(calibsetting):
    print("Calibrate button clicked:", calibsetting)
    if pstate == True:
        press.pressure_calib(calibsetting)

