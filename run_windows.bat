@echo off
.venv\Scripts\activate
uvicorn employee_api.main:app --reload
