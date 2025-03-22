# Task Management API

## Overview
The Task Management API is a backend application built using Django and Django REST Framework (DRF). It allows users to manage tasks efficiently, providing functionalities to create, read, update, delete, and filter tasks. The API is designed to be secure, user-friendly, and scalable.

## Features
### Core Features:
- **Task Management (CRUD):** Users can create, read, update, and delete tasks with attributes such as:
  - Title
  - Description
  - Due Date
  - Priority Level (Low, Medium, High)
  - Status (Pending, Completed)
  - Completed Timestamp
- **User Management (CRUD):** Users can register, view, update, and delete their profiles securely.
- **Authentication:** Secure access via Django's authentication system and optional JWT-based token authentication.
- **Task Filters and Sorting:** Users can filter tasks based on Status, Priority, and Due Date, and sort them by Due Date or Priority Level.