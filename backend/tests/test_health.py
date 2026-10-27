import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings


def test_health_endpoint():
    import backend.app.services.llm as llm_service
    llm_service._quota_exhausted = False
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "llm" in data
    assert "model" in data
    if not settings.is_offline:
        assert data["llm"] is True
        assert data["model"] == settings.gemini_model
    else:
        assert data["llm"] is False



def test_settings_load():
    assert settings.port == 8000
    assert settings.max_file_size_mb == 20
    assert settings.vif_threshold == 5.0
    assert settings.leakage_corr_threshold == 0.85
