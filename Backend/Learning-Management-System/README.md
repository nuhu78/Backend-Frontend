# 🎓 Learning Management System (LMS) API

A RESTful API built with **Django** and **Django REST Framework** for managing an online learning platform.

---

## 🚀 Features

- 🔐 JWT-based authentication (login via phone number + password)
- 👤 User registration & profile management
- 📚 Full CRUD operations for:
  - Teachers
  - Students
  - Courses
  - Enrollments
  - Lessons
  - Assignments
  - Submissions
  - Results

---

## 🛠 Tech Stack

- **Backend:** Python, Django  
- **API:** Django REST Framework  
- **Authentication:** JWT (`djangorestframework-simplejwt`)  
- **Database:** MySQL  

---

## ⚙️ Requirements

- Python 3.x  
- MySQL  

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/nuhu78/Learning-Management-System.git
cd Learning-Management-System/lms
````

### 2. Install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt mysqlclient
```

### 3. Configure database

Create a MySQL database named:

```
lms_db
```

Then update your `lms/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lms_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### 🔐 Authentication

| Method | Endpoint         | Description               | Auth |
| ------ | ---------------- | ------------------------- | ---- |
| POST   | `/api/register/` | Register a new user       | ❌    |
| POST   | `/api/login/`    | Login (returns JWT token) | ❌    |
| GET    | `/api/profile/`  | Get current user profile  | ✅    |

---

### 👨‍🏫 Teachers

| Method         | Endpoint              | Description                | Auth |
| -------------- | --------------------- | -------------------------- | ---- |
| GET/POST       | `/api/teachers/`      | List / Create teachers     | ✅    |
| GET/PUT/DELETE | `/api/teachers/<id>/` | Retrieve / Update / Delete | ✅    |

---

### 👨‍🎓 Students

| Method         | Endpoint              | Description                | Auth |
| -------------- | --------------------- | -------------------------- | ---- |
| GET/POST       | `/api/students/`      | List / Create students     | ✅    |
| GET/PUT/DELETE | `/api/students/<id>/` | Retrieve / Update / Delete | ✅    |

---

### 📚 Courses

| Method         | Endpoint             | Description                | Auth |
| -------------- | -------------------- | -------------------------- | ---- |
| GET/POST       | `/api/courses/`      | List / Create courses      | ✅    |
| GET/PUT/DELETE | `/api/courses/<id>/` | Retrieve / Update / Delete | ✅    |

---

### 📝 Other Resources

| Resource    | Endpoint            |
| ----------- | ------------------- |
| Enrollments | `/api/enrollments/` |
| Lessons     | `/api/lessons/`     |
| Assignments | `/api/assignments/` |
| Submissions | `/api/submissions/` |
| Results     | `/api/results/`     |

> All follow standard CRUD: `GET / POST / PUT / DELETE` (Auth required)

---

## 🔑 Authentication

Use JWT token in headers:

```http
Authorization: Bearer <your_access_token>
```

---

## ⚠️ Notes

* 🔒 Change `SECRET_KEY` before production
* 🚫 Set `DEBUG = False` in production
* 🛡️ Use environment variables for sensitive data

---

## 👨‍💻 Author

**Nuhu**
GitHub: [https://github.com/nuhu78](https://github.com/nuhu78)

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!


