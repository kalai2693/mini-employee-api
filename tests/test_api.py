import json, hmac, hashlib
from fastapi.testclient import TestClient
from employee_api.main import app
from employee_api.api import routes
from employee_api.config import WEBHOOK_SECRET

client=TestClient(app)
payload={"first_name":"Test","last_name":"User","email":"test@example.com","phone":"9999999999",
"department":"IT","designation":"Engineer","salary":50000,"status":"Active","joining_date":"2025-01-01"}

def test_crud():
    old=routes.storage.data_file
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        from pathlib import Path
        routes.storage.data_file=Path(d)/"employees.json"
        r=client.post("/employees",json=payload); assert r.status_code==201
        eid=r.json()["id"]
        assert client.get(f"/employees/{eid}").status_code==200
        assert client.patch(f"/employees/{eid}",json={"salary":60000}).status_code==200
        assert client.delete(f"/employees/{eid}").status_code==204
    routes.storage.data_file=old

def test_webhook_hmac():
    body=json.dumps({"event":"employee.created"}).encode()
    sig=hmac.new(WEBHOOK_SECRET.encode(),body,hashlib.sha256).hexdigest()
    r=client.post("/webhooks/employee",content=body,headers={"X-Signature":sig})
    assert r.status_code==200
    assert client.post("/webhooks/employee",content=body,headers={"X-Signature":"bad"}).status_code==403
