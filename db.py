#r".\Experiments.db"
#Setup Database
# importing sqlite3 module
import sqlite3

# create connection by using object
# to connect with hotel_data database
conn = sqlite3.connect('MFDatabase.db')
 
cursor = conn.cursor()

# Create setups table
def initiate_setups():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Setups (
            setup_id FIND INTEGER PRIMARY KEY,
            setup_name TEXT NOT NULL,
            Ch1_Reag TEXT,
            Ch2_Reag TEXT,
            Ch3_Reag TEXT,
            Ch4_Reag TEXT
        )
    ''')

#cursor.execute('''
#    CREATE TABLE IF NOT EXISTS Experiments (
#        experiment_id FIND INTEGER PRIMARY KEY,
#        experiment_name TEXT,
#        Ch1_Flow INTEGER,
#        Ch2_Flow INTGER,
#        Ch3_Flow INTEGER,
#        Ch4_Flow INTEGER.
#        setup_id INTEGER,
#        FOREIGN KEY (setup_id) REFERENCES Setups (setup_id)
#    )
#''')

def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect('MFDatabase.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_setup(setup_name, Ch1_Reag, Ch2_Reag, Ch3_Reag, Ch4_Reag):
    """
    Create a new setup row in the Setups table.
    """
    cursor.execute('''
        INSERT INTO Setups (setup_name, Ch1_Reag, Ch2_Reag, Ch3_Reag, Ch4_Reag) VALUES (?, ?, ?, ?, ?)
    ''', (setup_name, Ch1_Reag, Ch2_Reag, Ch3_Reag, Ch4_Reag))
    conn.commit()

def add_description_to_setup(setup_id, new_description):
    """
    Add a description to an existing setup row in the Setups table.
    """
    cursor.execute('''
        UPDATE Setups SET description = ? WHERE setup_id = ?
    ''', (new_description, setup_id))
    conn.commit()
    
def get_setup_info(setup_name):
    """
    Retrieve information about a setup from the Setups table.
    """
    cursor.execute('SELECT * FROM Setups WHERE setup_name = ?', (setup_name,))
    setup_info = cursor.fetchone()
    return setup_info

if __name__ == '__main__':
    create_connection()