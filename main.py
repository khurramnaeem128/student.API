import sqlite3
import os

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import jwt

load_dotenv()
app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

connection = sqlite3.connect("students.db", check_same_thread=False)

print("Database location:", os.path.abspath("students.db"))

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

connection.commit()

class Student(BaseModel):
    name: str
    age: int = Field(ge=1, le=120)


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, ge=1, le=120)


class User(BaseModel):
    username: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

@app.post("/register")
def register(user: User):

    hashed_password = hash_password(user.password)

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, hashed_password)
    )

    connection.commit()

    return {
        "message": "User registered successfully"
    }

@app.get("/")
def home():
    return {"message": "Hello API"}

@app.get("/students")
def get_students(token: str):

    verify_token(token)

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    return [
        {
            "id": student[0],
            "name": student[1],
            "age": student[2]
        }
        for student in students
    ]

@app.get("/students/{student_id}")
def get_student(student_id: int, token: str):

    verify_token(token)

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student[0],
        "name": student[1],
        "age": student[2]
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student, token: str):

    verify_token(token)

    cursor.execute(
        "UPDATE students SET name = ?, age = ? WHERE id = ?",
        (student.name, student.age, student_id)
    )

    connection.commit()

    return {
        "message": "Student updated successfully"
    }

@app.post("/students", status_code=201)
def add_student(student: Student, token: str):

    verify_token(token)

    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (student.name, student.age)
    )

    connection.commit()

    return {
        "message": "Student added successfully"
    }


@app.patch("/students/{student_id}")
def patch_student(student_id: int, student: StudentUpdate, token: str):
    verify_token(token)

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    existing_student = cursor.fetchone()

    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    name = student.name if student.name is not None else existing_student[1]
    age = student.age if student.age is not None else existing_student[2]

    cursor.execute(
        "UPDATE students SET name = ?, age = ? WHERE id = ?",
        (name, age, student_id)
    )

    connection.commit()

    return {
        "message": "Student updated successfully"
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int, token: str):
    verify_token(token)

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()

    return {
        "message": "Student deleted successfully"
    }

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/login")
def login(user: User):

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (user.username,)
    )

    existing_user = cursor.fetchone()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    password_correct = verify_password(
        user.password,
        existing_user[2]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = jwt.encode(
        {"username": user.username},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": token
    }

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )