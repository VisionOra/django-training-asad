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
* **SQLite**

---

## Project Structure

```bash
Blog Application/
│── blog/                     # Main blog app
│   ├── migrations/
│   ├── templates/blog/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
│── blog_project/             # Project settings and root urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
│── manage.py
│── db.sqlite3
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

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

---

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

### Posts

* `GET /api/posts/` → List all posts
* `POST /api/posts/` → Create a post (**JWT required**)
* `GET /api/posts/<id>/` → Retrieve a single post
* `PUT /api/posts/<id>/` → Update a post (**JWT required**)
* `PATCH /api/posts/<id>/` → Partially update a post (**JWT required**)
* `DELETE /api/posts/<id>/` → Delete a post (**JWT required**)

### Categories

* `GET /api/categories/` → List all categories
* `POST /api/categories/` → Create a category (**JWT required**)
* `GET /api/categories/<id>/` → Retrieve a category
* `PUT /api/categories/<id>/` → Update a category (**JWT required**)
* `PATCH /api/categories/<id>/` → Partially update a category (**JWT required**)
* `DELETE /api/categories/<id>/` → Delete a category (**JWT required**)

---

## JWT Authentication Endpoints

* **Obtain token**

  ```bash
  POST /api/token/
  ```

* **Refresh token**

  ```bash
  POST /api/token/refresh/
  ```

---

## Swagger / API Documentation

Swagger UI is available at:

```bash
http://127.0.0.1:8000/api/docs/
```

OpenAPI schema is available at:

```bash
http://127.0.0.1:8000/api/schema/
```

---

# How to Use JWT Authentication

## 1. Get access and refresh token

Send a POST request to:

```bash
/api/token/
```

with request body:

```json
{
  "username": "your_username",
  "password": "your_password"
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

## 2. Authorize in Swagger

Open Swagger UI and click **Authorize**.

Paste the access token in this format:

```text
Bearer your_access_token_here
```

Example:

```text
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

After authorization, protected endpoints such as `POST /api/posts/` can be used.

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
  "status": "published"
}
```

### With category

```json
{
  "title": "My JWT Post",
  "body": "This post was created using JWT authentication.",
  "category_id": 1,
  "status": "published"
}
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

## Current Permission Behavior

* **Anyone** can read posts and categories using `GET` requests.
* **Authenticated users with JWT** can create, update, and delete through the API.

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

