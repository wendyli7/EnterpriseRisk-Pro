"""Pydantic response models for the public API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    message: str


class CompanySummary(BaseModel):
    company_id: int
    company_name: str
    industry: str
    province: str
    city: str


class CompanyDetail(BaseModel):
    model_config = ConfigDict(extra="allow")

    basic_info: dict[str, Any]
    financial: list[dict[str, Any]]
    lawsuits: list[dict[str, Any]]
    penalties: list[dict[str, Any]]
    opinions: list[dict[str, Any]]


class RiskResponse(BaseModel):
    company_id: int
    company_name: str
    smoke_index: float = Field(ge=0, le=100)
    risk_level: str
    summary: str
    factor_scores: dict[str, float]