import io
import json
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config import settings


@pytest.fixture
def client():
    return TestClient(app)


def test_api_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert "llm" in data


def test_api_demo_debate(client):
    res = client.get("/api/demo")
    assert res.status_code == 200
    data = res.json()
    assert data["meta"]["session_id"] == "demo_titanic"
    assert len(data["rounds"]) >= 14


def test_api_sessions_list(client):
    res = client.get("/api/sessions")
    assert res.status_code == 200
    sessions = res.json()
    assert isinstance(sessions, list)
    # Harus ada minimal demo session
    assert any(s["session_id"] == "demo_titanic" for s in sessions)


def test_api_upload_invalid_extension(client):
    file_content = b"col1,col2\n1,2\n3,4\n"
    res = client.post(
        "/api/sessions",
        files={"file": ("test.txt", file_content, "text/plain")}
    )
    assert res.status_code == 400
    assert "Hanya file berformat .csv" in res.json()["detail"]


def test_api_upload_empty_file(client):
    res = client.post(
        "/api/sessions",
        files={"file": ("empty.csv", b"", "text/csv")}
    )
    assert res.status_code == 400
    assert "kosong" in res.json()["detail"]


def test_api_upload_file_too_large(client, monkeypatch):
    monkeypatch.setattr(settings, "max_file_size_mb", 1)
    large_bytes = b"a" * (2 * 1024 * 1024)
    res = client.post(
        "/api/sessions",
        files={"file": ("large.csv", large_bytes, "text/csv")}
    )
    assert res.status_code == 413
    assert "melebihi batas" in res.json()["detail"]


def test_api_session_lifecycle(client):
    # Buat dataset sintetis valid (100 baris agar CV 5-lipatan dan learning curve stabil)
    rows = ["feature_a,feature_b,target"]
    for i in range(100):
        t = 1 if i % 2 == 0 else 0
        val_b = i * 2.5 + (1.2 if t == 1 else -1.2)
        rows.append(f"{i * 1.5},{val_b:.2f},{t}")
    csv_bytes = "\n".join(rows).encode("utf-8")

    # 1. POST upload
    res = client.post(
        "/api/sessions",
        files={"file": ("synthetic_test.csv", csv_bytes, "text/csv")},
        data={"target": "target"}
    )
    assert res.status_code == 200
    job_id = res.json()["job_id"]
    session_id = res.json()["session_id"]
    assert job_id is not None
    assert session_id is not None

    # 2. GET SSE events
    # Baca event stream
    with client.stream("GET", f"/api/jobs/{job_id}/events") as sse_stream:
        events_received = []
        for line in sse_stream.iter_lines():
            if line.startswith("data: "):
                data_json = json.loads(line[6:])
                events_received.append(data_json)
                if data_json.get("done") or data_json.get("error"):
                    break
        assert len(events_received) >= 1

    # 3. GET debate
    res_debate = client.get(f"/api/sessions/{session_id}/debate")
    assert res_debate.status_code == 200
    debate_doc = res_debate.json()
    assert debate_doc["meta"]["session_id"] == session_id
    assert len(debate_doc["rounds"]) >= 14

    # 4. GET notebook
    res_nb = client.get(f"/api/sessions/{session_id}/notebook")
    assert res_nb.status_code == 200
    assert "attachment" in res_nb.headers.get("content-disposition", "")

    # 5. DELETE session
    res_del = client.delete(f"/api/sessions/{session_id}")
    assert res_del.status_code == 200
    assert res_del.json()["ok"] is True

    # 6. Verify deleted
    res_check = client.get(f"/api/sessions/{session_id}/debate")
    assert res_check.status_code == 404
