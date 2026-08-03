"""Company query routes backed by the local sample CSV data."""

from __future__ import annotations

from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from src.api.schemas.response import CompanyDetail, CompanySummary

router = APIRouter(prefix="/companies", tags=["companies"])

PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parents[3]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"


def _read_table(name: str) -> pd.DataFrame:
    path = SAMPLE_DIR / f"{name}.csv"
    if not path.exists():
        raise HTTPException(status_code=503, detail=f"Data source is unavailable: {name}")
    return pd.read_csv(path, encoding="utf-8-sig")


def _records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    return dataframe.where(pd.notna(dataframe), None).to_dict(orient="records")


@router.get("", response_model=list[CompanySummary])
def list_companies(
    keyword: str | None = Query(default=None, description="Company name keyword"),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[CompanySummary]:
    dataframe = _read_table("company_basic")
    if keyword:
        mask = dataframe["company_name"].astype(str).str.contains(keyword, case=False, na=False)
        dataframe = dataframe[mask]
    columns = ["company_id", "company_name", "industry", "province", "city"]
    return [CompanySummary(**item) for item in _records(dataframe[columns].head(limit))]


@router.get("/{company_id}", response_model=CompanyDetail)
def get_company(company_id: int) -> CompanyDetail:
    basic = _read_table("company_basic")
    match = basic[basic["company_id"] == company_id]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Company not found: {company_id}")

    def company_rows(name: str) -> list[dict[str, Any]]:
        table = _read_table(name)
        return _records(table[table["company_id"] == company_id])

    return CompanyDetail(
        basic_info=_records(match.iloc[[0]])[0],
        financial=company_rows("company_financial"),
        lawsuits=company_rows("company_lawsuit"),
        penalties=company_rows("company_penalty"),
        opinions=company_rows("company_opinion"),
    )