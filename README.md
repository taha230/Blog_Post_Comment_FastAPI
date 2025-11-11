# 🧠 FastAPI Blog Comment API

A simple and clean **CRUD (Create, Read, Update, Delete)** REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**.  
This project demonstrates how to structure and connect a real FastAPI backend with a database and expose endpoints for managing blog comments.

---

## 🚀 Features

- ⚙️ **FastAPI** for modern Python web APIs  
- 🧩 **SQLAlchemy ORM** for database modeling  
- 🧠 **Pydantic** for data validation  
- 💾 **SQLite** as a lightweight local database (easily switchable to PostgreSQL/MySQL)  
- 🔁 **CRUD operations** (Create, Read, Update, Delete)  
- 📘 **Swagger UI** for interactive API docs  
- 🧱 Simple, extendable architecture  

---

## 📂 Project Structure

```
fastapi-blog-comments/
│
├── main.py              # Main FastAPI application
├── database.db          # SQLite database (auto-created)
├── requirements.txt      # Dependencies (optional)
└── README.md            # Project documentation
```

---

## 🧰 Requirements

- Python 3.9+
- FastAPI
- SQLAlchemy
- Uvicorn

You can install all dependencies using pip:

```bash
pip install fastapi sqlalchemy uvicorn
```

*(Optionally add `pydantic` explicitly if not included automatically.)*

---

## ⚙️ Running the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/fastapi-blog-comments.git
   cd fastapi-blog-comments
   ```

2. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the app**

   - Interactive Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - Alternative Docs (Redoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧠 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/comments/` | Create a new comment |
| **GET** | `/comments/` | Retrieve all comments (optional filter: `?blog_id=`) |
| **GET** | `/comments/{comment_id}` | Retrieve a comment by ID |
| **PUT** | `/comments/{comment_id}` | Update a comment |
| **DELETE** | `/comments/{comment_id}` | Delete a comment |

---

## 🧾 Example Request

### ➕ Create Comment (POST `/comments/`)
```json
{
  "username": "taha",
  "blog_id": 101,
  "text": "FastAPI makes backend development so clean!"
}
```

### 🔍 Get Comments (GET `/comments/`)
```
/comments/?blog_id=101
```

### ✏️ Update Comment (PUT `/comments/1`)
```json
{
  "text": "Updated comment text!"
}
```

### ❌ Delete Comment (DELETE `/comments/1`)
Response:
```json
{
  "message": "Comment with id 1 has been deleted"
}
```

---

## 🧱 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **FastAPI** | API framework |
| **SQLAlchemy** | ORM for database |
| **SQLite** | Lightweight database |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |

---

## 🐳 Optional: Run with Docker

You can easily containerize the app:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi sqlalchemy uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Then build and run:
```bash
docker build -t fastapi-comments .
docker run -p 8000:8000 fastapi-comments
```

---

## 🧭 Future Improvements

- Add authentication (JWT)
- Connect to PostgreSQL or MySQL
- Add pagination and search
- Write unit tests with Pytest
- Deploy on Render / Railway / AWS

---

## 👤 Author

**Taha Hamedani**  
📧 [taha.hamedani8@gmail.com](mailto:taha.hamedani8@gmail.com)  

---

## 📜 License

This project is open-source under the **MIT License** — feel free to use and modify it.

---

### ⭐ If you like this project, consider giving it a star on GitHub!
