import csv
import sqlite3
import os

con = sqlite3.connect("alexa.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
con.commit()

# # print(f"Database path: {os.path.abspath('jarvis.db')}")
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sys_command';")
# result = cursor.fetchone()
# print(f"Table check result: {result}")
# cursor.execute("SELECT * FROM sys_command;")
# rows = cursor.fetchall()
# print(f"Table data: {rows}")

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())  # Should show [('sys_command',), ('web_command',)]

query = "INSERT INTO sys_command VALUES (null,'canva','C:\\Users\\nikhi\\AppData\\Local\\Programs\\Canva\\Canva.exe')"
cursor.execute(query)
con.commit()

# query = "INSERT INTO sys_command VALUES (null,'ONENOTE','C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')"
# cursor.execute(query)
# con.commit()

# query="DELETE FROM sys_command WHERE id =2"
# cursor.execute(query)
# con.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)
con.commit()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())  # Should show [('sys_command',), ('web_command',)]


# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()

# query = "INSERT INTO web_command VALUES (null,'canva', 'https://www.canva.com/')"
# cursor.execute(query)
# con.commit()

# query="DELETE FROM web_command WHERE id =4"
# cursor.execute(query)
# con.commit()

# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'Nayana', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'nikhil'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])