"""FastAPI application entry point for EnterpriseRisk-Pro."""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.api.routes.company import router as company_router
from src.api.routes.risk import router as risk_router

app = FastAPI(
    title="EnterpriseRisk-Pro API",
    version="2.0.0",
    description="Enterprise risk profile and explainable scoring service.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return """
    <!doctype html>
    <html lang="zh-CN">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>企业风险画像平台</title>
      <style>
        body { margin: 0; background: #f4f7fb; color: #182230; font-family: Arial, sans-serif; }
        main { max-width: 860px; margin: 48px auto; padding: 0 24px; }
        section { background: white; border: 1px solid #dce3ec; border-radius: 10px; padding: 28px; box-shadow: 0 8px 24px rgba(20, 35, 55, .06); }
        h1 { margin: 0 0 12px; color: #123b63; }
        p { line-height: 1.7; }
        .links { display: grid; gap: 12px; margin-top: 24px; }
        a { display: block; padding: 14px 16px; border-radius: 7px; background: #eaf3fb; color: #1260a0; text-decoration: none; }
        a:hover { background: #dceefa; }
        small { color: #64748b; }
      </style>
    </head>
    <body>
      <main>
        <section>
          <h1>企业风险画像平台</h1>
          <p>这是一个根据企业工商、财务、司法、行政处罚和舆情信息，生成风险评分和风险等级的系统。</p>
          <p><strong>普通用户：</strong>可以等待后续 Dashboard 页面；<strong>开发人员：</strong>可以通过下面的接口入口查看和调用数据。</p>
          <div class="links">
            <a href="/companies?limit=20">查看企业列表</a>
            <a href="/companies/1">查看 1 号企业详情</a>
            <a href="/companies/1/risk">查看 1 号企业风险评分</a>
            <a href="/docs">打开开发接口文档</a>
          </div>
          <p><small>当前版本：FastAPI 服务化 MVP</small></p>
        </section>
      </main>
    </body>
    </html>
    """


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "success", "message": "EnterpriseRisk-Pro running"}


app.include_router(company_router)
app.include_router(risk_router)