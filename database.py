import sqlite3
from typing import List
from model import Email

def create_database():
    conn = sqlite3.connect('email_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Email (
        Id TEXT PRIMARY KEY,
        FromUser TEXT,
        ToUser TEXT,
        Content TEXT,
        Subject TEXT,
        Date TEXT,
        Filtered INTEGER DEFAULT 0
    )''')
    
    # Create Label table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Label (
            Id INTEGER PRIMARY KEY,
            Label TEXT
        )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Email_Labels (
        Id INTEGER PRIMARY KEY,
        EmailId INTEGER,
        LabelId INTEGER,
        FOREIGN KEY (EmailId) REFERENCES Email (ID),
        FOREIGN KEY (LabelId) REFERENCES Label (Id)
    )''')


    conn.commit()
    conn.close()

def insert_labels():
    labels = [
        "CHAT", "SENT", "INBOX", "IMPORTANT", "TRASH", "DRAFT", "SPAM",
        "CATEGORY_FORUMS", "CATEGORY_UPDATES", "CATEGORY_PERSONAL", 
        "CATEGORY_PROMOTIONS", "CATEGORY_SOCIAL", "STARRED", "UNREAD", 
        "Unwanted"
    ]

    conn = sqlite3.connect('email_database.db')
    cursor = conn.cursor()

    for label in labels:
        cursor.execute('''
            INSERT INTO Label (Label) VALUES (?)
        ''', (label,))
    
    conn.commit()
    conn.close()

def remove_all_entries_from_table(table_name):
    conn = sqlite3.connect('email_database.db')
    cursor = conn.cursor()

    # Execute the DELETE statement without specifying a condition
    cursor.execute(f'DELETE FROM {table_name}')

    conn.commit()
    conn.close()

def prepare_db():
    create_database()
    print("Database tables created successfully.")
    remove_all_entries_from_table('Label')
    print('Removed all entries from Label table')
    insert_labels()


def add_to_db(db_file: str, data: dict, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Generate SQL query to insert data into the table
    columns = 'Id, Content, Date, Subject, FromUser, ToUser'
    placeholders = ', '.join('?' * len(data))
    query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    print('Query is:')
    print(query)
    print(data.values())
    # Execute the query with the dictionary values as parameters
    cursor.execute(query, tuple(data.values()))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def load_emails_from_db() -> List[Email]:
    conn = sqlite3.connect('email_database.db')
    cursor = conn.cursor()
    # Query data from the SQLite table
    cursor.execute('SELECT Id, FromUser, ToUser, Content, Subject, Date FROM Email')
    rows = cursor.fetchall()

    # Map retrieved data to Pydantic model instances
    email_instances = []
    for row in rows:
        email_instance = Email(

            idField=row[0],
            fromField = row[1],
            toField=row[2],
            dateReceivedField=row[3],
            contentField=row[4],
            subjectField=row[5]
        )
        email_instances.append(email_instance)

    # Close the database connection
    conn.close()
    return email_instances


if __name__ == "__main__":
    #prepare_db()
    prepare_db()