"""Generate a readable single-company risk report as HTML."""

from __future__ import annotations

from html import escape
from pathlib import Path

from src.api.routes.company import _read_table
from src.analysis.risk_analysis import RiskFeatureBuilder
from src.scoring.smoke_index import SmokeIndexScorer


def generate_report(company_id: int, output_dir: Path | None = None) -> Path:
    """Generate an HTML report and return its path."""
    basic = _read_table("company_basic")
    company = basic[basic["company_id"].eq(company_id)]
    if company.empty:
        raise ValueError(f"Company not found: {company_id}")

    features = RiskFeatureBuilder(source="auto").build()
    scored = SmokeIndexScorer().score(features[features["company_id"].eq(company_id)])
    result = scored.iloc[0]
    detail = company.iloc[0]
    output_dir = output_dir or Path(__file__).resolve().parents[2] / "reports" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"company_{company_id}_risk_report.html"

    factor_rows = "".join(
        f"<tr><td>{label}</td><td>{float(result[column]):.2f}</td></tr>"
        for label, column in [("财务风险", "financial_score"), ("司法风险", "lawsuit_score"), ("行政处罚风险", "penalty_score"), ("舆情风险", "opinion_score")]
    )
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>企业风险报告 - {escape(str(detail.company_name))}</title>
<style>body{{font-family:Arial,sans-serif;color:#182230;max-width:850px;margin:40px auto;line-height:1.6}}h1{{color:#123b63}}h2{{color:#24577f;border-bottom:1px solid #dce3ec;padding-bottom:8px}}table{{border-collapse:collapse;width:100%;margin:12px 0 28px}}td,th{{border:1px solid #dce3ec;padding:10px;text-align:left}}.score{{font-size:40px;font-weight:bold;color:#1260a0}}.summary{{padding:14px;background:#fff7e6;border-left:4px solid #e6a23c}}</style>
</head><body><h1>企业风险分析报告</h1>
<p>报告企业：<strong>{escape(str(detail.company_name))}</strong></p>
<h2>一、企业概况</h2><table><tr><th>项目</th><th>内容</th></tr>
<tr><td>企业编号</td><td>{company_id}</td></tr><tr><td>行业</td><td>{escape(str(detail.industry))}</td></tr>
<tr><td>地区</td><td>{escape(str(detail.province))} {escape(str(detail.city))}</td></tr><tr><td>注册资本</td><td>{escape(str(detail.registered_capital))}</td></tr>
<tr><td>经营状态</td><td>{escape(str(detail.business_status))}</td></tr></table>
<h2>二、风险结果</h2><p class="score">Smoke Index：{float(result.total_score):.2f}</p><p>风险等级：<strong>{escape(str(result.risk_level))}</strong></p><p class="summary">{escape(str(result.risk_summary))}</p>
<h2>三、风险因素</h2><table><tr><th>风险维度</th><th>分数</th></tr>{factor_rows}</table>
<h2>四、风险建议</h2><p>建议持续关注高分风险维度，结合近期司法案件、行政处罚和负面舆情变化进行复核；本报告结果用于演示和辅助分析，不替代人工尽调。</p>
</body></html>"""
    output_path.write_text(html, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(generate_report(1))
