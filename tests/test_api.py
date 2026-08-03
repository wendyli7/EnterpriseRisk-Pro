"""API regression tests for Sprint 6 Day 1."""

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "EnterpriseRisk-Pro running"}


def test_company_list_and_risk() -> None:
    companies = client.get("/companies?limit=3")
    assert companies.status_code == 200
    assert len(companies.json()) == 3

    company_id = companies.json()[0]["company_id"]
    risk = client.get(f"/companies/{company_id}/risk")
    assert risk.status_code == 200
    assert 0 <= risk.json()["smoke_index"] <= 100
    assert set(risk.json()["factor_scores"]) == {"financial", "lawsuit", "penalty", "opinion"}


def test_company_detail_and_not_found() -> None:
    detail = client.get("/companies/1")
    assert detail.status_code == 200
    assert set(detail.json()) == {"basic_info", "financial", "lawsuits", "penalties", "opinions"}

    missing = client.get("/companies/999999")
    assert missing.status_code == 404