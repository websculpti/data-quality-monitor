from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_analyze_dataset():

    csv_content = """name,age,salary
Alice,25,50000
Bob,,60000
Bob,,60000
Charlie,35,1000000
"""

    file = {
        "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
    }

    # Step 1 — upload
    upload_response = client.post("/upload", files=file)

    assert upload_response.status_code == 200

    file_id = upload_response.json()["file_id"]

    # Step 2 — analyze
    response = client.post(f"/analyze/{file_id}")

    assert response.status_code == 200

    data = response.json()

    # Step 3 — validate structure

    assert "metadata" in data
    assert "missing_values" in data
    assert "duplicates" in data
    assert "outliers" in data
    assert "data_types" in data