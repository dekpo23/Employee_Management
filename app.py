from sqlalchemy import text
import uvicorn
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastapi import FastAPI, status, HTTPException
from database import db
import re
from typing import Optional, Union
from datetime import date
import bcrypt

load_dotenv()

class employee_info(BaseModel):
    name: str = Field(..., max_length=100, example = "David Ekpo")
    email: str = Field(..., max_length=100, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', example  = "davidekpo@example.com")
    password: str = Field(..., max_length=255)
    position: Optional[str] = Field(None, example="Junior Data Analyst")
    department: Optional[str] = Field(None, example="Sales")
    date_hired: date = Field(..., example="2024-08-23")
    salary: float = Field(..., example=1500000)

    @field_validator("password")
    def check_password(cls, v):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$")
        if pattern.match(v) and len(v) >= 8:
            return v
        else:
            raise ValueError("Password must contain at least 8 characters, Uppercase and numbers")
        
class log_in(BaseModel):
    email: str = Field(..., max_length=100, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', example = "davidekpo@example.com")
    password: str = Field(..., max_length = 255)

    @field_validator("password")
    def check_password(cls, v):
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$")
        if pattern.match(v) and len(v) >= 8:
            return v
        else:
            raise ValueError("Password must contain at least 8 characters, Uppercase and numbers")



app = FastAPI(version="1.0.0")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: employee_info):
    try:
        check_duplicate = text("select * from employees where email = :email")
        if db.execute(check_duplicate, params = {"email": payload.email}).fetchone():
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="Email already exists, try logging in")
        else:
            encoded_password = bcrypt.hashpw(payload.password.encode("utf-8"), salt=bcrypt.gensalt())
            insert_query = text("insert into employees(name, email, password, position, department, date_hired, salary) values (:name, :email, :password, :position, :department, :date_hired, :salary)")
            db.execute(insert_query, params={"name": payload.name, "email": payload.email, "password": encoded_password, "position": payload.position, "department": payload.department, "date_hired": payload.date_hired, "salary": payload.salary})
            db.commit()
            print("Registration was successful")
            
        
    except HTTPException as e:
        return e
    
@app.post("/login", status_code=status.HTTP_201_CREATED)
def login(payload: log_in):
    

if __name__ == "__main__":
    uvicorn.run(app, host = os.getenv("host"), port = int(os.getenv("port")))

        
