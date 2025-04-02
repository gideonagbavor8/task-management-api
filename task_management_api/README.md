# Task Management API

## Overview
The Task Management API is a backend application built using Django and Django REST Framework (DRF). It allows users to manage tasks efficiently, providing functionalities to create, read, update, delete, and filter tasks. The API is designed to be secure, user-friendly, and scalable.

---

## Features

### **Core Features**
- **Task Management (CRUD):**
  - Users can create, read, update, and delete tasks.
  - Each task includes the following attributes:
    - Title
    - Description
    - Due Date
    - Priority Level (Low, Medium, High)
    - Status (Pending, Completed)
    - Completed Timestamp
  - Tasks are linked to the user who created them, ensuring task ownership.

- **Task Categories:**
  - Users can create categories (e.g., Work, Personal) and assign tasks to these categories.
  - Categories are user-specific and cannot be accessed by other users.

- **User Management:**
  - Users can register, view, update, and delete their profiles securely.
  - Admins can manage all users via the Django admin panel.

- **Authentication:**
  - Secure access via Django's authentication system.
  - JWT-based token authentication for API access.

- **Task Filters and Sorting:**
  - Users can filter tasks based on:
    - Status (Pending, Completed)
    - Priority Level (Low, Medium, High)
    - Due Date
  - Tasks can be sorted by:
    - Due Date
    - Priority Level

---

## API Endpoints

### **Authentication**
- `POST /api/token/`: Obtain JWT access and refresh tokens.
- `POST /api/token/refresh/`: Refresh the access token.

### **User Management**
- `POST /register/`: Register a new user.
- `GET /api/users/`: Retrieve all users (admin only).
- `GET /api/users/<id>/`: Retrieve a specific user (admin only).
- `PUT /api/users/<id>/`: Update a user (admin only).
- `DELETE /api/users/<id>/`: Delete a user (admin only).

### **Task Management**
- `GET /api/tasks/`: Retrieve all tasks for the authenticated user.
- `POST /api/tasks/`: Create a new task.
- `GET /api/tasks/<id>/`: Retrieve a specific task.
- `PUT /api/tasks/<id>/`: Update a task.
- `PATCH /api/tasks/<id>/`: Partially update a task.
- `DELETE /api/tasks/<id>/`: Delete a task.

### **Task Categories**
- `GET /api/categories/`: Retrieve all categories for the authenticated user.
- `POST /api/categories/`: Create a new category.
- `GET /api/categories/<id>/`: Retrieve a specific category.
- `PUT /api/categories/<id>/`: Update a category.
- `DELETE /api/categories/<id>/`: Delete a category.

---

## Validations
- **Task Ownership:** Tasks are only accessible to the users who created them.
- **Due Date Validation:** Tasks cannot have a due date in the past.
- **Unique Username Validation:** Usernames must be unique during registration.
- **Category Ownership:** Categories are user-specific and cannot be accessed by other users.
