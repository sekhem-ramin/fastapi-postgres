# 📚 Personal Book Library API

A RESTful backend API built with **FastAPI** and **PostgreSQL** that allows users to manage their personal book collection. Users can create accounts, save books, update book details, and delete entries — with OAuth-protected endpoints for secure access.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Authentication | OAuth2 (Bearer Token) |
| Language | Python 3.x |

---

## ✨ Features

- **User Registration & Authentication** — Create an account and log in securely using OAuth2
- **Save Books** — Add books to your personal library
- **Update Books** — Modify details of any saved book
- **Delete Books** — Remove books from your library (requires authentication)
- **SQLAlchemy ORM** — Database tables are modeled as Python classes for clean, maintainable data access

---

## 🔌 API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/login` | Authenticate and receive access token | ❌ |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/users` | Create a new user account | ❌ |
| `GET` | `/users/{id}` | Get a user by ID | ❌ |

### Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `POST` | `/books` | Save a new book | ❌ |
| `GET` | `/books` | Get all books | ❌ |
| `GET` | `/books/{id}` | Get a specific book | ❌ |
| `PUT` | `/books/{id}` | Update a saved book | ❌ |
| `DELETE` | `/books/{id}` | Delete a book | ✅ |

> 🔒 The `DELETE /books/{id}` endpoint is an example endpoint which requires a valid OAuth2 Bearer token, enforcing that only authenticated users can delete books.
> Each OAuth secured endpoint is denoted with a 🔒

## 🔐 Authentication Flow

1. Register a new user account via `POST /users`
2. Log in via the Authentication button on top right side of window which returns a JWT access token
3. The token will be passed as a Bearer token in the `Authorization` header to access protected routes:
   ```
   Authorization: Bearer <your_token>
   ```
---

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL running locally or remotely
- `pip` for package management

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/book-library-api.git
   cd book-library-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/book_library
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Visit the interactive Swagger API docs**
   ```
   http://127.0.0.1:8000/docs
   ```

---

## 🗄️ Database Models

### User
```python
id          # Primary Key
email       # Unique user email
password    # Hashed password
created_at  # Timestamp
```

### Book
```python
id          # Primary Key
title       # Book title
author      # Book author
description # Optional description
owner_id    # Foreign Key → User
created_at  # Timestamp
```
---
## 📄 License

This project is open source and available under the [MIT License](LICENSE).
