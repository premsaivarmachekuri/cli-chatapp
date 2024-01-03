import threading
import sqlite3

def insert_data(data):
    # Connect to the database (SQLite in this case)
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()

    # Perform data insertion (for simplicity, using a mock table)
    cursor.execute("INSERT INTO my_table (data) VALUES (?)", (data,))
    connection.commit()

    # Close the connection
    connection.close()
    print(f"Data '{data}' inserted successfully")

# List of data to insert
data_to_insert = ["Data1", "Data2", "Data3", "Data4", "Data5"]

# Create threads for data insertion
threads = []
for data in data_to_insert:
    thread = threading.Thread(target=insert_data, args=(data,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All data insertion completed")
