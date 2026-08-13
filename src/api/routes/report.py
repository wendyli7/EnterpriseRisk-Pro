"""Human-readable report route."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.reports.risk_report import generate_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{company_id}", response_class=HTMLResponse, include_in_schema=False)
def company_report(company_id: int) -> HTMLResponse:
    try:
        report_path = generate_report(company_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return HTMLResponse(content=report_path.read_text(encoding="utf-8"))
