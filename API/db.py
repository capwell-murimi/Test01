import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        connector = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT"))
        )

        if connector.is_connected():
            print("Successfully connected to mysql platform")
            return connector
    except Error as e:
        print(f"Error connecting to mysql platform: {e}")
        return None


get_connection()
    