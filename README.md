# django-training-asad

# Django Blog Application

A simple **Blog Application** built with **Django** and **Django REST Framework (DRF)**.
This project supports blog posts, categories, REST API endpoints, Swagger documentation, and **JWT authentication** for protected API operations.

---

## Features

### Blog Functionality

* View all published blog posts
* View a single post in detail
* Organize posts by category
* Track post author and status (`draft` / `published`)

### API Functionality

* Full CRUD API for **Posts**
* Full CRUD API for **Categories**
* Public read access for API endpoints
* Protected write operations using **JWT authentication**

### Authentication & Documentation

* JWT authentication using **SimpleJWT**
* Custom accounts API for **register, login, refresh, and profile**
* Swagger/OpenAPI documentation using **drf-spectacular**
* API testing directly from Swagger UI

---

## Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **drf-spectacular**
* **drf-spectacular-sidecar**
* **djangorestframework-simplejwt**
* **PostgreSQL**
* **python-decouple**
* **psycopg2-binary**

---

## Project Structure

```bash
Blog Application/
│── apps/
│   ├── blog/                     # Blog app
│   │   ├── migrations/
│   │   ├── templates/blog/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── accounts/                 # Accounts / JWT auth app
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
│
│── blog_project/                 # Project settings and root urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
│── manage.py
│── .env.example
│── requirements.txt
│── README.md
```

---

## Models

### Category

* `name`

### Post

* `title`
* `body`
* `author`
* `category`
* `created_at`
* `updated_at`
* `status`

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/VisionOra/django-training-asad.git
cd django-training-asad
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Server will start at:

```bash
http://127.0.0.1:8000/
```

---

## Available URLs

### HTML Pages

* **Home / Post List**
  `http://127.0.0.1:8000/`

* **Post Detail**
  `http://127.0.0.1:8000/post/<id>/`

---

## API Endpoints

## Accounts

* `POST /accounts/register/` → Register a new user
* `POST /accounts/login/` → Login and get JWT access/refresh tokens
* `POST /accounts/refresh/` → Get a new access token using refresh token
* `GET /accounts/profile/` → Get logged-in user profile (**JWT required**)

## Categories

* `GET /api/categories/` → List all categories
* `POST /api/categories/` → Create a category (**JWT required**)
* `GET /api/categories/<id>/` → Retrieve a category
* `PUT /api/categories/<id>/` → Update a category (**JWT required**)
* `PATCH /api/categories/<id>/` → Partially update a category (**JWT required**)
* `DELETE /api/categories/<id>/` → Delete a category (**JWT required**)

## Posts

* `GET /api/posts/` → List all posts
* `POST /api/posts/` → Create a post (**JWT required**)
* `GET /api/posts/<id>/` → Retrieve a single post
* `PUT /api/posts/<id>/` → Update a post (**JWT required**)
* `PATCH /api/posts/<id>/` → Partially update a post (**JWT required**)
* `DELETE /api/posts/<id>/` → Delete a post (**JWT required**)

---

## Swagger / API Documentation

Swagger UI is available at:

```bash
http://127.0.0.1:8000/swagger/
```

OpenAPI schema is available at:

```bash
http://127.0.0.1:8000/api/schema/
```

---

## JWT Authentication Flow

### 1. Register a user

Endpoint:

```bash
POST /accounts/register/
```

Request body:

```json
{
  "username": "asadtest1",
  "email": "asadtest1@example.com",
  "password": "Testpass123",
  "password2": "Testpass123"
}
```

---

### 2. Login and get tokens

Endpoint:

```bash
POST /accounts/login/
```

Request body:

```json
{
  "username": "asadtest1",
  "password": "Testpass123"
}
```

Example response:

```json
{
  "refresh": "your_refresh_token_here",
  "access": "your_access_token_here"
}
```

---

### 3. Refresh access token

Endpoint:

```bash
POST /accounts/refresh/
```

Request body:

```json
{
  "refresh": "your_refresh_token_here"
}
```

---

### 4. Use the access token in Swagger

Open Swagger UI and click **Authorize**.

Paste **only the raw access token** — **not** JSON and **not** quoted.

Correct:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Not this:

```text
Bearer "eyJ..."
```

Swagger will automatically send it as:

```bash
Authorization: Bearer <your_access_token>
```

---

## Example: Create a Category via API

### Endpoint

```bash
POST /api/categories/
```

### Request body

```json
{
  "name": "Technology"
}
```

---

## Example: Create a Post via API

### Endpoint

```bash
POST /api/posts/
```

### Request body

```json
{
  "title": "My JWT Post",
  "body": "This post was created using JWT authentication.",
  "category_id": 1,
  "status": "published"
}
```

---

## Current Permission Behavior

* **Anyone** can read posts and categories using `GET` requests.
* **Authenticated users with JWT** can create, update, and delete through the API.

---

## Tested API Flow

The following flow has been manually tested through Swagger:

* User registration
* User login
* Token refresh
* User profile access
* Categories CRUD
* Posts CRUD

---

## Future Improvements

Possible improvements for this project:

* Restrict update/delete so only the **post author** can modify their own posts
* Add pagination for API responses
* Add search and filtering
* Add frontend forms connected directly to JWT-protected APIs
* Add automated tests

---

## Requirements

The project dependencies are stored in:

```bash
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## Author

**Muhammad Asad**
