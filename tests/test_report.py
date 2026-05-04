from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_report_generation(monkeypatch):

    # Step 1 — upload dataset

    csv_content = "name,age\nAlice,25\nBob,30"

    file = {
        "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
    }

    upload_response = client.post("/upload", files=file)

    assert upload_response.status_code == 200

    file_id = upload_response.json()["file_id"]

    # Step 2 — mock LLM report generator

    def mock_generate_report(file_id: str):
        return {
            "file_id": file_id,
            "report": {
                "Summary": "Mock summary",
                "Risk level": "Low",
                "recommendations": "No action needed"
            },
            "report_path": f"reports/{file_id}_report.json"
        }

    monkeypatch.setattr(
        "app.routes.report.generate_report_with_llm",
        mock_generate_report
    )

    # Step 3 — call report endpoint

    response = client.get(f"/report/{file_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["file_id"] == file_id
    assert "report" in data
    assert "Summary" in data["report"]

    # Step 4 — call again (cached behavior)

    response_cached = client.get(f"/report/{file_id}")

    assert response_cached.status_code == 200

    data_cached = response_cached.json()

    assert data_cached["file_id"] == file_id 