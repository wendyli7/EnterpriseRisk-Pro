"""FastAPI application entry point for EnterpriseRisk-Pro."""

from fastapi import FastAPI

from src.api.routes.company import router as company_router
from src.api.routes.risk import router as risk_router

app = FastAPI(
    title="EnterpriseRisk-Pro API",
    version="2.0.0",
    description="Enterprise risk profile and explainable scoring service.",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "success", "message": "EnterpriseRisk-Pro running"}


app.include_router(company_router)
app.include_router(risk_router)