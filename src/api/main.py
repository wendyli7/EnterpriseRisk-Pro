"""FastAPI application entry point for EnterpriseRisk-Pro."""

from __future__ import annotations

import os
from html import escape

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.api.routes.company import _read_table
from src.api.routes.company import router as company_router
from src.api.routes.risk import router as risk_router
from src.api.routes.view import router as view_router

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
def home(keyword: str | None = Query(default=None, description="企业名称关键词")) -> str:
    companies = _read_table("company_basic")
    if keyword:
        mask = companies["company_name"].astype(str).str.contains(keyword, case=False, na=False)
        companies = companies[mask]
    companies = companies.sort_values("company_id").head(100)
    options = "".join(
        f'<option value="{int(row.company_id)}">{int(row.company_id)} - {escape(str(row.company_name))}</option>'
        for row in companies.itertuples()
    )
    empty = "<p class=\"empty\">没有找到匹配的企业，请换一个关键词。</p>" if companies.empty else ""
    return f"""
    <!doctype html>
    <html lang="zh-CN">
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
      <title>企业风险画像平台</title>
      <style>
        body {{ margin: 0; background: #f4f7fb; color: #182230; font-family: Arial, sans-serif; }}
        main {{ max-width: 860px; margin: 48px auto; padding: 0 24px; }}
        section {{ background: white; border: 1px solid #dce3ec; border-radius: 10px; padding: 28px; box-shadow: 0 8px 24px rgba(20, 35, 55, .06); }}
        h1 {{ margin: 0 0 12px; color: #123b63; }} h2 {{ color: #24577f; margin-top: 28px; }}
        p {{ line-height: 1.7; }} label {{ display: block; margin: 12px 0 6px; font-weight: 600; }}
        input, select {{ box-sizing: border-box; width: 100%; padding: 12px; border: 1px solid #b9c7d6; border-radius: 7px; font-size: 15px; }}
        button, .button {{ border: 0; border-radius: 7px; padding: 12px 16px; background: #1260a0; color: white; cursor: pointer; text-decoration: none; display: inline-block; margin: 12px 8px 0 0; }}
        .secondary {{ background: #eaf3fb; color: #1260a0; }} .empty {{ color: #a15c00; }} small {{ color: #64748b; }}
      </style>
    </head>
    <body><main><section>
      <h1>企业风险画像平台</h1>
      <p>搜索企业名称，选择企业后查看企业详情或风险评分。</p>
      <form method="get" action="/">
        <label for="keyword">搜索企业</label>
        <input id="keyword" name="keyword" value="{escape(keyword or '')}" placeholder="例如：科技、制造、供应链">
        <button type="submit">搜索</button>
      </form>
      {empty}
      <label for="company">选择企业</label>
      <select id="company" aria-label="选择企业">{options}</select>
      <div>
        <a id="detail-link" class="button" href="/company/{int(companies.iloc[0].company_id) if not companies.empty else 1}">查看企业详情</a>
        <a id="risk-link" class="button secondary" href="/risk/{int(companies.iloc[0].company_id) if not companies.empty else 1}">查看风险评分</a>
      </div>
      <p><small>开发人员可使用 <a href="/docs">接口文档</a> 调用 API。</small></p>
    </section></main>
    <script>
      const selector = document.getElementById('company');
      const detailLink = document.getElementById('detail-link');
      const riskLink = document.getElementById('risk-link');
      function updateLinks() {{
        const id = selector.value;
        detailLink.href = '/company/' + id;
        riskLink.href = '/risk/' + id;
      }}
      selector.addEventListener('change', updateLinks);
    </script>
    </body></html>
    """


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "success", "message": "EnterpriseRisk-Pro running"}


app.include_router(company_router)
app.include_router(risk_router)
app.include_router(view_router)