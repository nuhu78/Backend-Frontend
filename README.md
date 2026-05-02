# Learning Management System (LMS)

A full-stack Learning Management System built with **Django REST Framework** (backend) and **React 19 + Vite** (frontend), featuring JWT authentication, role-based access control, course management, and admin reporting.

---

## 🚀 Project Overview

This LMS platform enables users to:
- **Register and authenticate** using username/email or phone number with JWT tokens
- **Enroll in courses** and track learning progress
- **Manage courses** as instructors or admins
- **View role-based dashboards** with summaries and analytics
- **Access admin reporting** for user management and statistics
- **Control profile information** with email, phone, address, and bio

The system supports three user roles:
- **Admin**: Full system access, user management, reporting
- **Instructor**: Course creation and management, student tracking
- **Student**: Course enrollment, lesson viewing, assignment completion

---

## ✨ Features

### Authentication & Authorization
- ✅ JWT-based authentication with refresh tokens
- ✅ User registration with role selection
- ✅ Login with username or phone number
- ✅ Password reset flow with email verification
- ✅ Role-based access control (RBAC)
- ✅ Protected routes and endpoints

### Course Management
- ✅ Create, read, update, delete courses
- ✅ Course categorization
- ✅ Difficulty levels (Beginner, Intermediate, Advanced)
- ✅ Price management
- ✅ Publish/draft status
- ✅ Instructor assignment

### User Management
- ✅ Student enrollment in courses
- ✅ Instructor course assignments
- ✅ Admin user reporting and analytics
- ✅ User activation/deactivation
- ✅ Role distribution tracking

### Dashboard & Reports
- ✅ Role-specific dashboards
- ✅ User statistics (total, active, inactive)
- ✅ Course metrics (published, enrollments)
- ✅ Role-wise user distribution
- ✅ Quick navigation shortcuts

### API Features
- ✅ RESTful endpoints for all resources
- ✅ CORS support for frontend integration
- ✅ Pagination for list endpoints
- ✅ Permission-based filtering
- ✅ Comprehensive error handling

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 6.0 + Django REST Framework
- **Authentication**: SimpleJWT (JSON Web Tokens)
- **Database**: MySQL
- **ORM**: Django ORM
- **API**: RESTful API with DRF ViewSets

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 8.0
- **Routing**: React Router v7
- **State Management**: React Context API
- **Styling**: CSS3 with modern design patterns
- **HTTP Client**: Native Fetch API with auto-retry

### Development
- **Version Control**: Git
- **Package Management**: npm (Node.js)
- **Python Environment**: venv or equivalent

---

## 📋 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL Server running on localhost:3306
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd Backend/Learning-Management-System/lms
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create MySQL database**
   ```sql
   CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django development server**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at: `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd Frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start Vite development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at: `http://localhost:5173` (or next available port)

4. **Build for production**
   ```bash
   npm run build
   ```

### API Integration

The frontend is configured to proxy API requests to the backend:
- Frontend runs on: `http://localhost:5173` (or `5174`)
- Backend API: `http://127.0.0.1:8000/api`
- Vite proxy automatically routes `/api/*` to the backend

---

## 📁 Project Structure

```
LMS/
├── Backend/
│   └── Learning-Management-System/
│       └── lms/
│           ├── api/
│           │   ├── models.py          # Database models
│           │   ├── serializers.py     # DRF serializers
│           │   ├── views.py           # API endpoints
│           │   ├── permissions.py     # Permission classes
│           │   ├── urls.py            # URL routing
│           │   ├── middleware.py      # CORS middleware
│           │   └── migrations/        # Database migrations
│           └── lms/
│               ├── settings.py        # Django settings
│               ├── urls.py            # Main URL config
│               └── wsgi.py            # WSGI app
├── Frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main app component
│   │   ├── App.css                   # Global styles
│   │   ├── index.css                 # Base styles
│   │   ├── main.jsx                  # Entry point
│   │   ├── lib/
│   │   │   └── api.js                # API wrapper
│   │   ├── context/
│   │   │   └── AuthContext.jsx       # Auth state management
│   │   ├── components/
│   │   │   └── AppShell.jsx          # Layout & routing
│   │   └── pages.jsx                 # Page components
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

---

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login with credentials
- `POST /api/auth/logout/` - Logout and blacklist token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/forgot-password/` - Request password reset
- `POST /api/auth/reset-password/` - Reset password with token
- `POST /api/auth/token/refresh/` - Refresh access token

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create course (instructor/admin)
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course (owner/admin)
- `DELETE /api/courses/{id}/` - Delete course (owner/admin)

### Enrollments
- `GET /api/enrollments/` - List user enrollments
- `POST /api/enrollments/` - Enroll in course
- `GET /api/enrollments/{id}/` - Get enrollment details
- `PUT /api/enrollments/{id}/` - Update enrollment
- `DELETE /api/enrollments/{id}/` - Cancel enrollment

### Lessons
- `GET /api/lessons/` - List lessons
- `POST /api/lessons/` - Create lesson (instructor/admin)
- `GET /api/lessons/{id}/` - Get lesson details
- `PUT /api/lessons/{id}/` - Update lesson
- `DELETE /api/lessons/{id}/` - Delete lesson

### Admin
- `GET /api/admin/users/` - List all users (admin only)
- `PUT /api/admin/users/{id}/` - Update user (admin only)
- `GET /api/admin/users/summary/` - User statistics (admin only)
- `GET /api/dashboard/summary/` - Dashboard summary (admin only)

### Categories
- `GET /api/categories/` - List course categories
- `POST /api/categories/` - Create category (admin)

---

## 🔑 Test Credentials

After running migrations and creating a superuser, you can:

1. **Create test users** via the registration page at `/register`
2. **Default admin** - Use the superuser credentials you created with `createsuperuser`

**Test User Roles:**
- Role: `STUDENT` - Can browse and enroll in courses
- Role: `INSTRUCTOR` - Can create and manage courses
- Role: `ADMIN` - Full system access and reporting

---

## 📸 Screenshots

The following screenshots demonstrate key features:

1. **Login Page** - Username/phone and password authentication

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ef098613-0a28-4c8d-952c-715da40bd488" />

   
2. **Dashboard** - Role-specific overview with statistics

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/23e5775b-45ab-4fe0-9a96-b77b739d18a9" />


4. **Courses Page** - Browse, search, and manage courses

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a1a006bf-13c9-4a03-ab7f-8a897db1c498" />


---

## 🚀 Deployment

### Backend (Django)
Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn lms.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (React)
Build and serve static files:
```bash
npm run build
# Serve dist/ directory with a static file server
```

---

## 🐛 Troubleshooting

### Backend Issues
- **Database connection error**: Ensure MySQL is running and credentials in `settings.py` are correct
- **Migrations failed**: Run `python manage.py migrate --run-syncdb`
- **CORS error**: Update `FRONTEND_ORIGINS` in `settings.py`

### Frontend Issues
- **API requests failing**: Ensure backend is running on `http://127.0.0.1:8000`
- **Port already in use**: Vite will automatically use the next available port
- **Hot reload not working**: Check that `vite.config.js` proxy is configured correctly

---

## 📝 Development Notes

### Adding New Endpoints
1. Create a model in `api/models.py`
2. Create a serializer in `api/serializers.py`
3. Create a viewset in `api/views.py`
4. Register the route in `api/urls.py`

### Adding New Pages
1. Add page component to `src/pages.jsx`
2. Add route in `src/App.jsx`
3. Wrap with `<ProtectedRoute>` if authentication required
4. Import and use `useAuth()` context hook

### Permission System
Three-tier permission system:
- **Role-based**: Check user role (ADMIN, INSTRUCTOR, STUDENT)
- **Object-level**: Check resource ownership
- **View-level**: Apply permissions to viewsets

---

## 📚 Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Vite Documentation](https://vite.dev/)
- [React Router](https://reactrouter.com/)

---

## 👥 Author

**MD Tangimul Anjam Nuhu**

---

## 📄 License

This project is part of the Ostad Full Stack Development Course.

---

## 🤝 Contributing

This is an educational project. For improvements or suggestions, please create an issue or pull request.

---

**Last Updated**: May 2, 2026
