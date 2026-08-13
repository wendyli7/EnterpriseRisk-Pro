"""Human-readable report route."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.reports.risk_report import generate_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{company_id}", response_class=FileResponse, include_in_schema=False)
def company_report(company_id: int) -> FileResponse:
    try:
        report_path = generate_report(company_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return FileResponse(report_path, media_type="text/html", filename=report_path.name)
