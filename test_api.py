from fastapi.testclient import TestClient
from main import app
import models

client = TestClient(app)

def test_rbac_dashboard():
    print("\n--- Testing Dashboard RBAC ---")
    # Admin (User 1)
    response = client.get("/dashboard/analytics", headers={"X-User-ID": "1"})
    print(f"Admin Access Dashboard: {response.status_code}")
    assert response.status_code == 200
    
    # Analyst (User 2)
    response = client.get("/dashboard/analytics", headers={"X-User-ID": "2"})
    print(f"Analyst Access Dashboard: {response.status_code}")
    assert response.status_code == 200
    
    # Viewer (User 3)
    response = client.get("/dashboard/analytics", headers={"X-User-ID": "3"})
    print(f"Viewer Access Dashboard: {response.status_code}")
    assert response.status_code == 200

def test_rbac_records():
    print("\n--- Testing Records RBAC ---")
    # Admin (User 1) - Can Read
    response = client.get("/records/", headers={"X-User-ID": "1"})
    print(f"Admin Read Records: {response.status_code}")
    assert response.status_code == 200
    
    # Analyst (User 2) - Can Read
    response = client.get("/records/", headers={"X-User-ID": "2"})
    print(f"Analyst Read Records: {response.status_code}")
    assert response.status_code == 200
    
    # Viewer (User 3) - Cannot Read (Wait, let me double check my code)
    # My code: router records.py: dependencies=[Depends(auth.require_analyst_or_admin)]
    response = client.get("/records/", headers={"X-User-ID": "3"})
    print(f"Viewer Read Records: {response.status_code} (Expected 403)")
    assert response.status_code == 403

def test_record_creation():
    print("\n--- Testing Record Creation RBAC ---")
    record_data = {
        "amount": 100.0,
        "type": "EXPENSE",
        "category": "Office",
        "date": "2026-04-03",
        "description": "Office Supplies"
    }
    
    # Admin (User 1) - Can Create
    response = client.post("/records/", json=record_data, headers={"X-User-ID": "1"})
    print(f"Admin Create Record: {response.status_code}")
    assert response.status_code == 200
    
    # Analyst (User 2) - Cannot Create
    response = client.post("/records/", json=record_data, headers={"X-User-ID": "2"})
    print(f"Analyst Create Record: {response.status_code} (Expected 403)")
    assert response.status_code == 403

def test_user_management():
    print("\n--- Testing User Management RBAC (Admin Only) ---")
    
    # Admin (User 1) - Can list users
    response = client.get("/users/", headers={"X-User-ID": "1"})
    print(f"Admin List Users: {response.status_code}")
    assert response.status_code == 200
    
    # Analyst (User 2) - Cannot list users
    response = client.get("/users/", headers={"X-User-ID": "2"})
    print(f"Analyst List Users: {response.status_code} (Expected 403)")
    assert response.status_code == 403

def test_analytics_correctness():
    print("\n--- Testing Analytics Logic ---")
    response = client.get("/dashboard/analytics", headers={"X-User-ID": "1"})
    data = response.json()
    summary = data["summary"]
    print(f"Total Income: {summary['total_income']}")
    print(f"Total Expenses: {summary['total_expenses']}")
    print(f"Net Balance: {summary['net_balance']}")
    
    # New Indian seed data calculations:
    # Income: 75500.00 + 12450.50 = 87950.50
    # Initial Expenses: 4500 + 1250.75 + 350 + 45000 + 2500 = 53600.75
    # test_record_creation adds one expense of 100.0
    # Total Expenses = 53700.75
    # Net Balance = 87950.50 - 53700.75 = 34249.75
    
    assert summary["total_income"] == 87950.50
    assert summary["total_expenses"] == 53700.75
    assert summary["net_balance"] == 34249.75

if __name__ == "__main__":
    # Note: Each run might modify the DB, so we should ideally clean up.
    # For this simple assignment, we just run once.
    try:
        test_rbac_dashboard()
        test_rbac_records()
        test_record_creation()
        test_user_management()
        test_analytics_correctness()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
