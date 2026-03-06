# 🔐 Digital Signature system

A **Zero-Knowledge Secure File Sharing System** built with **FastAPI** that enables encrypted file storage and secure digital file sharing between users.

The system ensures that **files remain private and protected**, even from the server itself.

---

## 🚀 Features

* 🔐 Secure user authentication
* 📂 Encrypted file upload and storage
* 📥 Secure file download
* 🧾 Digital signature verification
* 🗄 Database-backed file management
* 🌐 REST API built with FastAPI
* ⚡ Deployable on cloud platforms (Render)

---

## 🏗 System Architecture

```
Client (Frontend)
        │
        ▼
FastAPI Backend (app/main.py)
        │
        ├── Authentication API
        ├── File Upload API
        ├── File Download API
        │
        ▼
Database (SQLite / PostgreSQL)

        │
        ▼
Encrypted File Storage
```

---

## 📂 Project Structure

```
secure-file-sharing-system
│
├── app
│   ├── api
│   │   ├── auth.py
│   │   └── files.py
│   │
│   ├── db
│   │   └── database.py
│   │
│   └── main.py
│
├── storage
├── start.sh
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/Tejamaloth8/secure-file-sharing-system.git
cd secure-file-sharing-system
```

Create virtual environment:

```
python -m venv venv
```

Activate environment:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn app.main:app --reload
```

Open API docs:

```
http://127.0.0.1:8000/docs
```

---

## 🌐 Deployment

This project can be deployed using:

* **Render**
* **Docker**
* **AWS EC2**
* **Railway**

Start command for Render:

```
bash start.sh
```

---

## 📘 API Documentation

FastAPI automatically generates documentation.

Swagger UI:

```
/docs
```

ReDoc:

```
/redoc
```

---

## 🔒 Security Model

The system follows a **Zero-Knowledge architecture**:

* Files are encrypted before storage
* Server cannot read file contents
* Authentication ensures only authorized users access files

---

## 👨‍💻 Author

Teja
Computer Science Engineering Student

GitHub
https://github.com/Tejamaloth8

---

## 📜 License

MIT License
