import sqlite3

def update_db_schema():
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    # Add a new column 'shortlisted' to the 'resumes' table
    cursor.execute('''
        UPDATE resumes
        SET phone_no = ?, email = ?
    ''', ('7978701483', 'sahoomadhumita1977@gmail.com'))

    conn.commit()
    conn.close()
    print("Database schema updated successfully.")


if __name__ == "__main__":
    update_db_schema()