# Employee Directory Application

A full-stack application for managing employee information, built with React, FastAPI, and SQLite.

## Features

- 📋 List all employees in a data table
- ➕ Add new employees with detailed information
- ✏️ Edit existing employee records
- 🗑️ Delete employees with confirmation dialog
- 📱 Responsive Material UI design
- 📆 Automatic age calculation based on date of birth

## Tech Stack

### Frontend
- React with Hooks
- Material UI for components
- ESBuild for build tooling
- Date-fns for date manipulation

### Backend
- FastAPI (Python)
- SQLite database
- Pydantic for data validation

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

## Installation

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Build and Start the development server:
```bash
npm run build
```

The application will be available at `http://localhost:8080`

## API Endpoints

### GET /employees/
- Retrieves all employees
- Response: List of employee objects

### GET /employees/{employee_id}
- Retrieves information of employee; given employee id
- Response: employee object

### POST /employees/
- Creates a new employee
- Request Body: Employee data
- Response: Created employee object

### PUT /employees/{employee_id}
- Updates an existing employee
- Request Body: Updated employee data
- Response: Updated employee object

### DELETE /employees/{employee_id}
- Deletes an employee
- Response: Success message

## Data Structure

### Employee Object
```json
{
  "id": number,
  "name": string,
  "age": number,
  "dob": string (YYYY-MM-DD),
  "gender": string ("male" | "female" | "other"),
  "department": string
}
```

## Project Structure

```
assess/
├── backend/
│   └── app.py
│   └── requirements.txt
├── frontend/
│   └──src/
│       ├── App.jsx
│       └── index.jsx
│   └── build.js
│   └── index.html
│   └── package.json
└── README.md
```

