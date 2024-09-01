import sqlite3
import os
from pathlib import Path

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    # Create a table to store resumes with additional columns for name, email, and phone number
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            content BLOB,
            name TEXT,
            email TEXT,
            phone_no TEXT
        )
    ''')

    conn.commit()
    conn.close()

def store_resumes():
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    # Get the path to the Resumes folder
    resumes_dir = Path(__file__).parent / 'Resumes'

    # Insert PDFs into the database
    for filename in os.listdir(resumes_dir):
        if filename.endswith('.pdf'):
            with open(resumes_dir / filename, 'rb') as file:
                content = file.read()

            # Manually input the name, email, and phone number for each resume
            print(f"Processing: {filename}")
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone_no = input("Enter phone number: ")

            cursor.execute('''
                INSERT INTO resumes (filename, content, name, email, phone_no)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, content, name, email, phone_no))

    conn.commit()
    conn.close()
    print("Resumes stored successfully in the database.")

def view_resumes():
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    # Retrieve and display all entries in the resumes table except the BLOB content
    cursor.execute('SELECT id, filename, name, email, phone_no FROM resumes')
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]}, Filename: {row[1]}, Name: {row[2]}, Email: {row[3]}, Phone No.: {row[4]}")

    conn.close()

if __name__ == "__main__":
    # create_database()  # Create the database and table if they don't exist
    # store_resumes()    # Store the resumes in the database
    view_resumes()     # View the stored resumes
