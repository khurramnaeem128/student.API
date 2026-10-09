# Student Management API

## Project Overview

The Student Management API is a backend application built with FastAPI and SQLite that allows users to manage student records through RESTful API endpoints. It supports CRUD (Create, Read, Update, Delete) operations, request validation, error handling, and JWT-based authentication to protect API operations.

The project demonstrates how to build a structured backend service with database integration, secure authentication, and interactive API documentation.

## Features

* **Create Students:** Add new student records.
* **Retrieve Students:** Get all students or retrieve an individual student by ID.
* **Update Student Records:** Modify existing student information.
* **Partial Updates:** Update selected student fields without replacing the entire record.
* **Delete Students:** Remove student records from the database.
* **SQLite Integration:** Store student information in a local database.
* **JWT Authentication:** Use JSON Web Tokens to authenticate protected API requests.
* **Password Hashing:** Hash user passwords instead of storing them in plain text.
* **Input Validation:** Validate incoming data using Pydantic.
* **Error Handling:** Return appropriate HTTP errors for invalid requests and missing records.
* **Interactive Documentation:** Test API endpoints through the automatically generated Swagger UI.

## Technologies Used

* Python
* FastAPI
* SQLite
* SQL
* Pydantic
* Uvicorn
* JWT Authentication
* Password hashing with bcrypt
* Swagger UI / OpenAPI

## Project Structure

```text
API-project/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database is created or initialized by the application when required. The local database file and environment-specific secrets should not be committed to the repository.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd API-project
```

Replace `<repository-url>` with the actual repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Configure the required environment variables, including the JWT secret key, according to the application's configuration. Do not commit real secrets to GitHub.

### 5. Start the API Server

```bash
python -m uvicorn main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

Use Swagger UI to inspect endpoints, submit requests, and test the API.

## API Operations

| HTTP Method | Operation                | Purpose                                                            |
| ----------- | ------------------------ | ------------------------------------------------------------------ |
| POST        | Create student           | Add a student record                                               |
| GET         | List students            | Retrieve student records                                           |
| GET         | Get student by ID        | Retrieve a specific student                                        |
| PUT         | Update student           | Replace or update a student record according to the implementation |
| PATCH       | Partially update student | Modify selected student fields                                     |
| DELETE      | Delete student           | Remove a student record                                            |

The exact endpoint paths and authentication requirements are defined in `main.py`.

## Authentication and Security

The application includes JWT-based authentication for protected operations.

* Authenticate using the application's configured login flow.
* Use the issued token when calling protected endpoints.
* Store passwords as hashes.
* Keep the JWT secret key outside the source code in environment configuration.
* Validate input data and handle unauthorized requests appropriately.

**Security note:** JWT authentication should be combined with appropriate token expiration, secure secret management, and authorization checks. A valid token alone does not automatically establish permission to access every student record.

## Data Storage

Student records are stored in an SQLite database. SQLite provides lightweight, file-based storage without requiring a separate database server.

The application uses its database logic to create, retrieve, update, and delete records. The database file should be excluded from GitHub if it contains private or local data.

## Error Handling and Validation

The API uses request validation to reject invalid input and HTTP exceptions to handle errors such as records that do not exist.

For example, student age validation can enforce an allowed range, while a request for a nonexistent student can return an HTTP `404 Not Found` response.

## Learning Outcomes

This project demonstrates practical experience with:

* REST API development
* FastAPI application structure
* HTTP methods and status codes
* SQLite database operations
* Pydantic data validation
* Authentication using JWT
* Password hashing
* CRUD functionality
* API testing with Swagger UI
* Dependency management and GitHub project organization

## Future Improvements

* Add automated tests with Pytest.
* Implement role-based authorization.
* Improve database session and connection management.
* Add pagination and filtering to student listings.
* Use a migration tool for database schema changes.
* Add structured logging and production error handling.
* Deploy the API to a suitable hosting platform.

## Conclusion

The Student Management API demonstrates how to develop a backend service using FastAPI, SQLite, and JWT authentication. It combines database operations, data validation, authentication, and interactive documentation into a practical project that can serve as a foundation for more advanced backend and AI application development.
