<<<<<<< HEAD
# Samas-Academy
=======
# Student Management System

A fully responsive web application for managing students, courses, enrollments, and grades. Built with Django (backend) and Bootstrap 5 (frontend).

## Features

### User Roles
- **Admin** - Full access: manage students, courses, teachers, enrollments, grades
- **Teacher** - Access assigned courses, view enrolled students, assign grades, export student lists

### Core Modules
- **Students** - Add, update, delete, search by name/roll number, filter by department
- **Courses** - Add, update, delete, assign teachers
- **Enrollments** - Enroll students in courses
- **Grades** - Assign and update grades, view grade reports per student

### UI/UX
- Clean academic-themed design
- Fully responsive (mobile, tablet, desktop)
- Bootstrap 5 navbar with Dashboard, Students, Courses, Grades, Logout
- Search bar and dropdown filters
- Pagination for student lists
- Export student list to CSV (optional)

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin Account
```bash
python manage.py create_admin
```
Default credentials: **username:** `admin`, **password:** `admin123`

### 4. (Optional) Seed Sample Departments
```bash
python manage.py seed_departments
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Project Structure

```
PROJECT/
├── accounts/          # Authentication, roles (Admin/Teacher)
├── students/          # Student & Department management
├── courses/           # Course management
├── grades/            # Enrollments & grades
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── student_management/ # Project settings
└── manage.py
```

## Usage

1. **Login** as admin with `admin` / `admin123`
2. **Add Teachers** via Dashboard → Teachers → Add Teacher
3. **Add Students** via Students → Add Student
4. **Add Courses** via Courses → Add Course (assign a teacher)
5. **Enroll Students** via Grades → Enroll Student
6. **Assign Grades** via Grades list → Assign/Update for each enrollment

## Technical Notes

- Django 5.x+ with SQLite (change to PostgreSQL in production)
- Bootstrap 5 and Bootstrap Icons
- Custom CSS in `static/css/custom.css` for academic branding
- Role-based access via decorators in `accounts/decorators.py`
>>>>>>> 1ebb9ab (Initial commit: Add Django Student Management project)
