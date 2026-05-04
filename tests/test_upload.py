from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_upload_valid_csv():

    csv_content = "name,age\nAlice,25\nBob,30"

    file = {
        "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
    }

    response = client.post("/upload", files=file)

    assert response.status_code == 200

    data = response.json()

    assert "file_id" in data
   # assert data["status"] == "uploaded"
    assert data["file_name"] == "test.csv"