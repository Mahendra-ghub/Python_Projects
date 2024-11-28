import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="",  # No password
            database="tracker_data"
        )
        print("Database connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd=""
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS tracker_data")
        print("Database 'tracker_data' created or already exists.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table():
    try:
        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task_name VARCHAR(255) NOT NULL,
                duration INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Table 'tasks' created or already exists.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    create_database()
    create_table()
