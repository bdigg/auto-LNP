cursor.execute('''
    CREATE TABLE IF NOT EXISTS Setups (
        setup_id FIND INTEGER PRIMARY KEY,
        Ch1_Reag VARCHAR(15),
        Ch1_Conc INT,
        Ch2_Reag VARCHAR(15),
        Ch2_Conc INT,
        Ch3_Reag VARCHAR(15),
        Ch3_Conc INT,
        Ch4_Reag VARCHAR(15),
        Ch4_Conc INT,
    )
''')

# Create experiments table
conn.execute(""" CREATE TABLE Experiments (
            FIND INT PRIMARY KEY NOT NULL, 
            setup_id INT
            FOREIGN KEY (setup_id) REFERENCES Setups (setup_id)
            Ch1_Flow INT,
            Ch2_Flow INT,
            Ch3_Flow INT,
            Ch4_Flow INT,           
        ); """)