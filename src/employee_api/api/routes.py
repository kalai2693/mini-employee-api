from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from ..services.employee_service import EmployeeService, EmployeeNotFoundError, DuplicateEmailError
from ..services.file_service import FileProcessor
from ..services.external_api_service import ExternalAPIClient
from ..storage import StorageService, StorageError

router=APIRouter()
storage=StorageService()
service=EmployeeService(storage)
processor=FileProcessor()
client=ExternalAPIClient()

def handle_storage_error(exc: StorageError) -> None:
    raise HTTPException(status_code=503, detail=str(exc))

@router.get("/employees", response_model=list[EmployeeResponse])
def list_employees(skip:int=0, limit:int=10):
    try: return service.list(skip, min(limit,100))
    except StorageError as exc: handle_storage_error(exc)

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id:int):
    try: return service.get(employee_id)
    except EmployeeNotFoundError: raise HTTPException(404, "Employee not found")
    except StorageError as exc: handle_storage_error(exc)

@router.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(payload:EmployeeCreate):
    try: return service.create(payload)
    except DuplicateEmailError: raise HTTPException(400, "Email already exists")
    except StorageError as exc: handle_storage_error(exc)

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def replace_employee(employee_id:int,payload:EmployeeCreate):
    try: return service.replace(employee_id,payload)
    except EmployeeNotFoundError: raise HTTPException(404,"Employee not found")
    except DuplicateEmailError: raise HTTPException(400,"Email already exists")
    except StorageError as exc: handle_storage_error(exc)

@router.patch("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id:int,payload:EmployeeUpdate):
    try: return service.update(employee_id,payload)
    except EmployeeNotFoundError: raise HTTPException(404,"Employee not found")
    except DuplicateEmailError: raise HTTPException(400,"Email already exists")
    except StorageError as exc: handle_storage_error(exc)

@router.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id:int):
    try: service.delete(employee_id)
    except EmployeeNotFoundError: raise HTTPException(404,"Employee not found")
    except StorageError as exc: handle_storage_error(exc)

@router.post("/employees/import/csv")
async def import_csv(file:UploadFile=File(...)):
    if not file.filename.lower().endswith(".csv"): raise HTTPException(400,"CSV file required")
    records, failed=processor.csv_import(await file.read())
    created=0
    for r in records:
        try: service.create(r); created+=1
        except (DuplicateEmailError, StorageError) as exc: failed+=1
    return {"created":created,"failed":failed}

@router.post("/employees/import/excel")
async def import_excel(file:UploadFile=File(...)):
    if not file.filename.lower().endswith(".xlsx"): raise HTTPException(400,"XLSX file required")
    records, failed=processor.excel_import(await file.read())
    created=0
    for r in records:
        try: service.create(r); created+=1
        except (DuplicateEmailError, StorageError): failed+=1
    return {"created":created,"failed":failed}

@router.post("/employees/import/pdf")
async def import_pdf(file:UploadFile=File(...)):
    if not file.filename.lower().endswith(".pdf"): raise HTTPException(400,"PDF file required")
    return processor.pdf_import(await file.read())

@router.post("/employees/sync")
def sync_employees():
    try: payload=client.fetch_employees()
    except Exception as exc:
        raise HTTPException(503, f"External API unavailable: {exc}") from exc
    return {"received":len(payload), "nested_example": [client.extract_nested(x) for x in payload if isinstance(x,dict)]}
