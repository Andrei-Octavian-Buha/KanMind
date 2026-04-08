# kanMind Backend

Backend API for a Kanban-style project management application. Built with Django REST Framework, it provides authentication, board management, task tracking, and comments functionality. It acts as the core service layer connecting the frontend with the database.

---

## Tech Stack

* Python 3.x
* Django 5.x
* Django REST Framework
* django-cors-headers
* SQLite (development) / PostgreSQL (production-ready option)

---

## Features

* User authentication (registration, login)
* Board management (create, read, update, delete)
* Task management (assignment, status, filtering)
* Comment system for tasks
* RESTful API architecture
* CORS support for frontend integration
* Django admin panel

---

## Project Structure

```bash
kanMind/
│── auth_app/          # Authentication (users, login, registration)
│── boards_app/        # Boards CRUD and logic
│── tasks_app/         # Tasks management (create, assign, update, delete)
│── comments_app/      # Task comments system
│── core/              # Settings, URLs, WSGI/ASGI configuration
│── manage.py
│── requirements.txt
│── README.md
```

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/Andrei-Octavian-Buha/kanMind.git
cd kanMind
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### Activate environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Apply migrations

```bash
python manage.py migrate
```

---

### 5. Run server

```bash
python manage.py runserver
```

---

## Requirements

```txt
asgiref==3.11.0
Django==5.2.9
django-cors-headers==4.9.0
djangorestframework==3.16.1
sqlparse==0.5.5
typing_extensions==4.15.0
```

---

## API Endpoints

### Authentication

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| POST   | /api/registration/ | Register user      |
| POST   | /api/login/        | Login user         |
| GET    | /api/email-check/  | Check email exists |

---

### Boards

| Method | Endpoint          | Description     |
| ------ | ----------------- | --------------- |
| GET    | /api/boards/      | List all boards |
| POST   | /api/boards/      | Create board    |
| GET    | /api/boards/{id}/ | Retrieve board  |
| PATCH  | /api/boards/{id}/ | Update board    |
| DELETE | /api/boards/{id}/ | Delete board    |

---

### Tasks

| Method | Endpoint                   | Description            |
| ------ | -------------------------- | ---------------------- |
| GET    | /api/tasks/assigned-to-me/ | Tasks assigned to user |
| GET    | /api/tasks/reviewing/      | Tasks under review     |
| POST   | /api/tasks/                | Create task            |
| PATCH  | /api/tasks/{id}/           | Update task            |
| DELETE | /api/tasks/{id}/           | Delete task            |

---

### Comments

| Method | Endpoint                            | Description    |
| ------ | ----------------------------------- | -------------- |
| GET    | /api/tasks/{id}/comments/           | Get comments   |
| POST   | /api/tasks/{id}/comments/           | Add comment    |
| DELETE | /api/tasks/{task_id}/comments/{id}/ | Delete comment |

---

## Environment Variables

Create a `.env` file in project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## Notes

* Always run inside a virtual environment
* Configure CORS for frontend communication
* Set `DEBUG=False` in production
* Use PostgreSQL for production deployments

---

## License

MIT
