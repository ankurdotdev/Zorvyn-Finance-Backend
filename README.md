# Finance Data Processing and Access Control Backend

## Overview
This is a robust FastAPI-based backend for a finance dashboard system. It supports financial record management, user role management, and summary-level analytics, all protected by a role-based access control (RBAC) system.

## Features
- **User Management**: Admin can create, update, and manage users and their roles.
- **Financial Records**: CRUD operations for income and expense entries with filtering by date, type, and category.
- **Dashboard Analytics**: Real-time calculation of total income, expenses, net balance, and category-wise breakdowns.
- **Role-Based Access Control (RBAC)**:
  - **ADMIN**: Full access to all resources (Users, Records, Dashboard).
  - **ANALYST**: Can view records and dashboard analytics.
  - **VIEWER**: Can only view dashboard analytics.
- **Data Persistence**: Uses SQLite with SQLAlchemy ORM.
- **Validation**: Strict data validation using Pydantic (V2).

## Project Structure
- `main.py`: Entry point, app initialization, and database seeding.
- `database.py`: Database connection and session management.
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic schemas for request/response validation.
- `crud.py`: Encapsulated database operations.
- `auth.py`: Mock authentication and RBAC dependency guards.
- `routers/`:
  - `users.py`: Endpoints for user management.
  - `records.py`: Endpoints for financial records.
  - `dashboard.py`: Endpoints for analytics and summaries.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic[email] httpx
   ```

### Running the Application
Start the server using `uvicorn`:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### API Documentation
Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Authentication (Mock)
The system uses a mock authentication header `X-User-ID`. 
Initial seed data creates the following users:
- **User ID 1**: Admin (`admin`)
- **User ID 2**: Analyst (`analyst`)
- **User ID 3**: Viewer (`viewer`)

Example Request:
```bash
curl -H "X-User-ID: 1" http://127.0.0.1:8000/records/
```

## Running Tests
A verification script is included to test RBAC and business logic:
```bash
python test_api.py
```

## Assumptions & Design Decisions
- **Mock Auth**: For simplicity and as per the assignment's flexibility, we use a simple Header-based authentication (`X-User-ID`). This can be easily swapped for JWT in a production environment.
- **Filtering**: Records can be filtered by `type` (INCOME/EXPENSE), `category`, `start_date`, and `end_date` via query parameters.
- **Analytics**: Aggregations are performed at the database level using SQLAlchemy's `func` module for efficiency.
