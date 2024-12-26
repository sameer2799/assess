# main.py
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from datetime import datetime
import sqlite3
from typing import List
import enum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create SQLite database and table
def init_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob DATE NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Enums for validation
class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

# Pydantic models for request/response validation
class EmployeeBase(BaseModel):
    name: str
    age: int
    dob: datetime
    gender: Gender
    department: str

class Employee(EmployeeBase):
    id: int

class EmployeeCreate(EmployeeBase):
    pass

# Database utilities
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# API endpoints
@app.get("/employees/", response_model=List[Employee])
async def get_employees():
    try:

        conn = sqlite3.connect('employees.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        
        employees = c.execute('SELECT * FROM employees').fetchall()
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()
    if not employees:
        return {"message": "No employees found"}
    
    return employees

@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    try:
        conn = sqlite3.connect('employees.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        
        employee = c.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        
        
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()
    
    return employee

@app.post("/employees/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    
    
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
        
    try:
        
        c.execute('''
            INSERT INTO employees (name, age, dob, gender, department)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            employee.name,
            employee.age,
            employee.dob,
            employee.gender,
            employee.department
        ))
        
        employee_id = c.lastrowid
        conn.commit()
        
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()

    
    return {**employee.dict(), "id": employee_id}

@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: EmployeeCreate):
    
    try:
        
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        
        # Check if employee exists
        if not c.execute('SELECT 1 FROM employees WHERE id = ?', (employee_id,)).fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employee not found")
        
        c.execute('''
            UPDATE employees
            SET name = ?, age = ?, dob = ?, gender = ?, department = ?
            WHERE id = ?
        ''', (
            employee.name,
            employee.age,
            employee.dob,
            employee.gender,
            employee.department,
            employee_id
        ))
        
        conn.commit()
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()
    
    return {**employee.dict(), "id": employee_id}

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    
    try:

        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        
        # Check if employee exists
        if not c.execute('SELECT 1 FROM employees WHERE id = ?', (employee_id,)).fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employee not found")
        
        c.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        conn.close()
    
    return {"message": "Employee deleted successfully"}
