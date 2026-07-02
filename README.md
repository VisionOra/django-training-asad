# Django Blog Application

A full-featured **Django REST API** with a web UI, covering blog management, AI-powered chatbot, and automated source generation — all secured with JWT authentication and backed by PostgreSQL.

---

## Features

| App | Description |
|-----|-------------|
| **Blog** | CRUD for posts and categories with a web UI |
| **Accounts** | Register, login, token refresh, user profile |
| **Chatbot** | AI chat sessions powered by Groq (LLaMA 3.3 70B) via LangChain |
| **Source Generator** | Fetch authentic Google search results via the Serper API |

- JWT authentication (access: 60 min, refresh: 7 days)
- PostgreSQL database
- Swagger UI + ReDoc for all endpoints
- Modular `services/` architecture in Chatbot and Source Generator

---

## Tech Stack

- **Python 3.14** / **Django 6**
- **Django REST Framework**
- **drf-spectacular** + **drf-spectacular-sidecar** (Swagger/ReDoc)
- **djangorestframework-simplejwt**
- **LangChain** + **langchain-groq** (Groq LLaMA 3.3 70B)
- **Serper API** (Google Search)
- **PostgreSQL** + **psycopg2-binary**
- **python-decouple**

---

## Project Structure

```
Blog Application/
├── apps/
│   ├── blog/                     # Blog posts & categories (web UI + API)
│   │   ├── templates/blog/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── accounts/                 # Custom User model + JWT auth
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── chatbot/                  # AI chat sessions (Groq / LangChain)
│   │   ├── migrations/
│   │   ├── services/
│   │   │   └── ai_service.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── source_generator/         # Google search source fetcher (Serper)
│       ├── migrations/
│       ├── services/
│       │   └── serper_service.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── blog_project/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
├── .env                          # secrets (gitignored)
└── .env.example
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/VisionOra/django-training-asad.git
cd django-training-asad
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

`.env` contents:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=blog_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

### 5. Set up PostgreSQL

```sql
CREATE DATABASE blog_db;
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## Available URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Blog web UI (post list) |
| `http://127.0.0.1:8000/swagger/` | Swagger UI — all endpoints |
| `http://127.0.0.1:8000/redoc/` | ReDoc documentation |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

> The **API Docs** button in the top-right of the web UI opens Swagger directly.

---

## API Endpoints

### Accounts — `/api/accounts/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/accounts/register/` | No | Register a new user |
| POST | `/api/accounts/login/` | No | Login — returns JWT tokens |
| POST | `/api/accounts/refresh/` | No | Refresh access token |
| GET | `/api/accounts/profile/` | JWT | Get current user profile |

### Blog Posts — `/api/posts/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/posts/` | No | List all posts |
| POST | `/api/posts/` | JWT | Create a post |
| GET | `/api/posts/<id>/` | No | Retrieve a post |
| PATCH | `/api/posts/<id>/` | JWT | Update a post |
| DELETE | `/api/posts/<id>/` | JWT | Delete a post |

### Categories — `/api/categories/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/categories/` | No | List all categories |
| POST | `/api/categories/` | JWT | Create a category |
| GET | `/api/categories/<id>/` | No | Retrieve a category |
| PATCH | `/api/categories/<id>/` | JWT | Update a category |
| DELETE | `/api/categories/<id>/` | JWT | Delete a category |

### Chatbot — `/api/chat/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/chat/sessions/` | JWT | List all chat sessions |
| POST | `/api/chat/sessions/` | JWT | Create a new chat session |
| GET | `/api/chat/sessions/<id>/` | JWT | Get session with full chat history |
| PATCH | `/api/chat/sessions/<id>/` | JWT | Rename a session |
| DELETE | `/api/chat/sessions/<id>/` | JWT | Delete a session |
| GET | `/api/chat/sessions/<id>/messages/` | JWT | List all messages in a session |
| POST | `/api/chat/sessions/<id>/send/` | JWT | Send a message — receive AI reply |
| DELETE | `/api/chat/sessions/<id>/clear/` | JWT | Clear all messages in a session |

### Source Generator — `/api/sources/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/sources/searches/` | JWT | List all searches |
| POST | `/api/sources/searches/` | JWT | Generate sources for a topic |
| GET | `/api/sources/searches/<id>/` | JWT | Get search with all its sources |
| PATCH | `/api/sources/searches/<id>/` | JWT | Update search topic or limit |
| DELETE | `/api/sources/searches/<id>/` | JWT | Delete a search |
| POST | `/api/sources/searches/<id>/refetch/` | JWT | Re-fetch sources from Serper API |
| GET | `/api/sources/searches/<id>/sources/` | JWT | List sources for a search |
| GET | `/api/sources/sources/<id>/` | JWT | Retrieve a single source |
| PATCH | `/api/sources/sources/<id>/` | JWT | Update a single source |
| DELETE | `/api/sources/sources/<id>/` | JWT | Delete a single source |

---

## JWT Authentication

### 1. Register

```bash
POST /api/accounts/register/
```
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "StrongPass123",
  "password2": "StrongPass123"
}
```

### 2. Login — get tokens

```bash
POST /api/accounts/login/
```
```json
{
  "username": "john_doe",
  "password": "StrongPass123"
}
```

Response:
```json
{
  "refresh": "eyJ...",
  "access": "eyJ..."
}
```

### 3. Authorize in Swagger

Open `http://127.0.0.1:8000/swagger/` → click **Authorize** → paste the raw access token (no `Bearer` prefix — Swagger adds it automatically).

### 4. Refresh token

```bash
POST /api/accounts/refresh/
```
```json
{
  "refresh": "eyJ..."
}
```

---

## Chatbot Usage

```bash
# 1. Create a session
POST /api/chat/sessions/
{ "title": "My first chat" }

# 2. Send a message
POST /api/chat/sessions/1/send/
{ "message": "Give me 3 blog post ideas about Django." }
```

The AI uses the full conversation history for context on every request.

---

## Source Generator Usage

```bash
# Fetch sources for a topic
POST /api/sources/searches/
{ "topic": "Django REST Framework", "limit": 5 }

# Re-fetch with latest results
POST /api/sources/searches/1/refetch/
```

---

## Author

**Muhammad Asad**
