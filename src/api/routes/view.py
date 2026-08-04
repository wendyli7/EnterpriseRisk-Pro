"""Human-readable HTML views for non-technical users."""

from __future__ import annotations

from html import escape

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.api.routes.company import get_company
from src.api.routes.risk import get_company_risk

router = APIRouter(tags=["web pages"])


def _page(title: str, body: str) -> str:
    return f"""
    <!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <style>
      body {{ margin: 0; background: #f4f7fb; color: #182230; font-family: Arial, sans-serif; }}
      main {{ max-width: 900px; margin: 36px auto; padding: 0 20px; }}
      section {{ background: #fff; border: 1px solid #dce3ec; border-radius: 10px; padding: 26px; margin-bottom: 18px; }}
      h1 {{ color: #123b63; margin-top: 0; }} h2 {{ color: #24577f; }}
      .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
      .item {{ padding: 14px; background: #f5f8fb; border-radius: 7px; }}
      .label {{ color: #64748b; font-size: 13px; }} .value {{ margin-top: 5px; font-weight: 600; }}
      a {{ color: #1260a0; text-decoration: none; }} .score {{ font-size: 42px; color: #123b63; font-weight: 700; }}
      .notice {{ padding: 14px; background: #fff7e6; border-left: 4px solid #e6a23c; }}
    </style></head><body><main>{body}</main></body></html>
    """


@router.get("/company/{company_id}", response_class=HTMLResponse, include_in_schema=False)
def company_page(company_id: int) -> str:
    detail = get_company(company_id).model_dump()
    basic = detail["basic_info"]
    fields = [
        ("企业名称", basic.get("company_name")),
        ("所属行业", basic.get("industry")),
        ("所在省市", f"{basic.get('province', '')} {basic.get('city', '')}"),
        ("注册资本", basic.get("registered_capital")),
        ("成立日期", basic.get("establish_date")),
        ("经营状态", basic.get("business_status")),
    ]
    cards = "".join(f'<div class="item"><div class="label">{escape(str(label))}</div><div class="value">{escape(str(value))}</div></div>' for label, value in fields)
    body = f"<section><h1>企业详情</h1><div class=\"grid\">{cards}</div></section>"
    body += f"<section><h2>风险分析</h2><p>查看该企业的综合风险评分和风险因素：</p><p><a href=\"/risk/{company_id}\">打开风险评分页面</a></p></section>"
    body += f"<p><a href=\"/\">返回平台首页</a> · <a href=\"/companies/{company_id}\">查看原始 API 数据</a></p>"
    return _page(f"{basic.get('company_name', '企业详情')} - 企业风险画像", body)


@router.get("/risk/{company_id}", response_class=HTMLResponse, include_in_schema=False)
def risk_page(company_id: int) -> str:
    result = get_company_risk(company_id).model_dump()
    factor_cards = "".join(f'<div class="item"><div class="label">{escape(str(name))}风险</div><div class="value">{value:.2f}</div></div>' for name, value in result["factor_scores"].items())
    body = f"<section><h1>{escape(result['company_name'])} 风险评分</h1><div class=\"score\">{result['smoke_index']:.2f}</div><p>风险等级：<strong>{escape(result['risk_level'])}</strong></p><div class=\"notice\">{escape(result['summary'])}</div></section>"
    body += f"<section><h2>风险因素</h2><div class=\"grid\">{factor_cards}</div></section>"
    body += f"<p><a href=\"/company/{company_id}\">返回企业详情</a> · <a href=\"/\">返回平台首页</a></p>"
    return _page(f"{result['company_name']} - 风险评分", body)