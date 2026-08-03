"""Risk scoring routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.api.schemas.response import RiskResponse
from src.analysis.risk_analysis import RiskFeatureBuilder
from src.scoring.smoke_index import SmokeIndexScorer

router = APIRouter(prefix="/companies", tags=["risk"])


@router.get("/{company_id}/risk", response_model=RiskResponse)
def get_company_risk(company_id: int) -> RiskResponse:
    features = RiskFeatureBuilder(source="auto").build()
    company_features = features[features["company_id"] == company_id]
    if company_features.empty:
        raise HTTPException(status_code=404, detail=f"Company not found: {company_id}")

    scored = SmokeIndexScorer().score(company_features)
    row = scored.iloc[0]
    return RiskResponse(
        company_id=int(row["company_id"]),
        company_name=str(row["company_name"]),
        smoke_index=float(row["total_score"]),
        risk_level=str(row["risk_level"]),
        summary=str(row["risk_summary"]),
        factor_scores={
            "financial": float(row["financial_score"]),
            "lawsuit": float(row["lawsuit_score"]),
            "penalty": float(row["penalty_score"]),
            "opinion": float(row["opinion_score"]),
        },
    )