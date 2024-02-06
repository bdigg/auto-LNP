#r".\Experiments.db"
#Setup Database
# importing sqlite3 module
import sqlite3

# create connection by using object
# to connect with hotel_data database

conn = sqlite3.connect('MFDatabase.db')
 
cursor = conn.cursor()

# Create setups table
def create_setups_table():
    conn = sqlite3.connect('MFDatabase.db')
    cursor = conn.cursor()
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

def create_experiments_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Experiments (
            experiment_id INTEGER PRIMARY KEY,
            experiment_name TEXT NOT NULL,
            Ch1_Flow INT,
            Ch2_Flow INT,
            Ch3_Flow INT,
            Ch4_Flow INT,
            setup_id INTEGER,
            activity BOOLEAN,
            FOREIGN KEY (setup_id) REFERENCES Setups (setup_id)
        )
    ''')
    conn.commit()

def create_records_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Records (
            experiment_id INTEGER PRIMARY KEY,
            experiment_name TEXT NOT NULL,
            setup_name TEXT NOT NULL,
            Ch1_Reag TEXT,
            Ch2_Reag TEXT,
            Ch3_Reag TEXT,
            Ch4_Reag TEXT,
            Ch1_Flow INT,
            Ch2_Flow INT,
            Ch3_Flow INT,
            Ch4_Flow INT,
            setup_id INTEGER,
            activity BOOLEAN,
            timestamp TEXT,
            FOREIGN KEY (setup_id) REFERENCES Setups (setup_id)
        )
    ''')
    conn.commit()


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

def create_experiment(setup_id, experiment_name, Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow):
    cursor.execute('''
        INSERT INTO Experiments (setup_id, experiment_name, Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow) VALUES (?, ?, ?, ?, ?, ?)
    ''', (setup_id, experiment_name, Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow))
    conn.commit()

def get_all_setup_names():
    """
    Retrieve all setup names from the Setups table as a list of strings.
    """
    cursor.execute('SELECT setup_name FROM Setups')
    setup_names = [row[0] for row in cursor.fetchall()]
    return setup_names

def add_description_to_setup(setup_id, new_description):
    """
    Add a description to an existing setup row in the Setups table.
    """
    cursor.execute('''
        UPDATE Setups SET description = ? WHERE setup_id = ?
    ''', (new_description, setup_id))
    conn.commit()
    
def get_setup_info(setup_name):

    cursor.execute('SELECT * FROM Setups WHERE setup_name = ?', (setup_name,))
    setup_info = cursor.fetchone()
    return setup_info

def get_setup_id_by_name(setup_name):
    cursor.execute('SELECT setup_id FROM Setups WHERE setup_name = ?', (setup_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_experiment_info(experiment_name):
    cursor.execute('SELECT * FROM Experiments WHERE experiment_name = ?', (experiment_name,))
    experiment_info = cursor.fetchone()
    return experiment_info

def get_experiment_info_with_id(experiment_id):
    cursor.execute('SELECT * FROM Experiments WHERE experiment_id = ?', (experiment_id,))
    experiment_info = cursor.fetchone()
    return experiment_info

def get_experiment_names_in_order():
    """
    Retrieve all experiment names in order from the Experiments table.
    """
    cursor.execute('SELECT experiment_name FROM Experiments ORDER BY experiment_id')
    experiment_names = [row[0] for row in cursor.fetchall()]
    return experiment_names

def get_experiment_ids_in_order():
    """
    Retrieve all experiment names in order from the Experiments table.
    """
    cursor.execute('SELECT experiment_id FROM Experiments ORDER BY experiment_id')
    experiment_ids = [row[0] for row in cursor.fetchall()]
    return experiment_ids

def delete_all_experiments():
    try:
        cursor.execute('DELETE FROM Experiments')
        conn.commit()
        print("All experiments deleted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

def copy_setup_and_experiment_to_record(setup_id, experiment_id):
    """
    Copy data from a specific row in Setups and Experiments tables to Records table.
    """
    cursor.execute('''
        INSERT INTO Records (
            experiment_id, experiment_name, setup_name, Ch1_Reag, Ch2_Reag, Ch3_Reag, Ch4_Reag,
            Ch1_Flow, Ch2_Flow, Ch3_Flow, Ch4_Flow, setup_id, activity
        )
        SELECT
            E.experiment_id, E.experiment_name,
            S.setup_name, S.Ch1_Reag, S.Ch2_Reag, S.Ch3_Reag, S.Ch4_Reag,
            E.Ch1_Flow, E.Ch2_Flow, E.Ch3_Flow, E.Ch4_Flow,
            E.setup_id, E.activity
        FROM Experiments E
        INNER JOIN Setups S ON E.setup_id = S.setup_id
        WHERE E.experiment_id = ? AND S.setup_id = ?
    ''', (experiment_id, setup_id))
    conn.commit()

def get_records_info(experiment_id):
    cursor.execute('SELECT * FROM Records WHERE experiment_id = ?', (experiment_id,))
    records_info = cursor.fetchone()
    return records_info

def delete_all_records():
    """
    Delete the Records table.
    """
    cursor.execute('DROP TABLE IF EXISTS Records')
    conn.commit()

def is_experiments_table_empty():
    """
    Check if the Experiments table is empty.
    Returns True if the table is empty, False otherwise.
    """
    cursor.execute('SELECT COUNT(*) FROM Experiments')
    row_count = cursor.fetchone()[0]
    return row_count == 0

def print_all_records_columns():
    """
    Print all columns from the Records table.
    """
    cursor.execute('PRAGMA table_info(Records)')
    columns_info = cursor.fetchall()

    column_names = [info[1] for info in columns_info]

    print("Columns in the Records table:")
    for column_name in column_names:
        print(column_name)
        
def delete_experiment_by_id(experiment_id):
    """
    Delete a row from the Experiments table based on experiment_id.
    """
    cursor.execute('DELETE FROM Experiments WHERE experiment_id = ?', (experiment_id,))
    conn.commit()

def get_first_experiment_name():
    """
    Retrieve the first experiment_name from the Experiments table.
    Returns None if the table is empty.
    """
    cursor.execute('SELECT experiment_name FROM Experiments ORDER BY experiment_id LIMIT 1')
    result = cursor.fetchone()
    return result[0] if result else None


if __name__ == '__main__':
    create_connection()
