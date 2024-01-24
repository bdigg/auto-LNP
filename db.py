#Setup Database
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    #create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if conn == None:
            print("No Conn")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r".\Experiments.db"
    print("oi")
    
    # create a database connection
    conn = create_connection(database)
    print(conn)
    
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()    
