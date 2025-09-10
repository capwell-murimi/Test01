from mysql.connector import Error
from db import get_connection
from utils import hash_password, verify_password
from schemas import UserCreate

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS people (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL,age INT NOT NULL)")
    conn.commit()
    conn.close()
    cursor.close()

def create_user(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    hash_pwd = hash_password(user.password)

    cursor.execute("INSERT INTO people (name,email,password,age) VALUES(%s,%s,%s,%s)", (user.name, user.email, hash_pwd, user.age))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    cursor.close()
    return {**user.dict(), "id": user_id}

def get_user_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM people WHERE email = %s",(email,))
    user = cursor.fetchone()
    conn.close()
    cursor.close()
    return user

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if user and verify_password(password, user["password"]):
        return user

def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM people")
    users = cursor.fetchall()
    conn.close()
    cursor.close()

    return users

def update_users(id: int, name: str, email: str, age: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE people SET name=%s, email=%s, age=%s WHERE id=%s", (name,email,age,id))
    conn.commit()
    cursor.execute("SELECT * FROM people WHERE id=%s",(id,))
    user = cursor.fetchone()
    conn.close()
    cursor.close()
    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "age": user[4]
    }

def delete_users(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM people WHERE id=%s", (id,))

    conn.commit()
    conn.close()
    cursor.close()