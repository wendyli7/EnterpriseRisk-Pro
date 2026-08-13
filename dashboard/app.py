"""Streamlit dashboard for EnterpriseRisk-Pro."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Render starts Streamlit from the dashboard directory; expose the repository
# root so the shared analysis and scoring packages can be imported reliably.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.risk_analysis import RiskFeatureBuilder
from src.scoring.smoke_index import SmokeIndexScorer


SCORE_PATH = ROOT / "data" / "processed" / "enterprise_smoke_index.csv"
FEATURE_PATH = ROOT / "data" / "processed" / "enterprise_risk_features.csv"

st.set_page_config(page_title="企业风险画像", page_icon="📊", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if FEATURE_PATH.exists():
        features = pd.read_csv(FEATURE_PATH, encoding="utf-8-sig")
    else:
        features = RiskFeatureBuilder(source="csv").build()

    if SCORE_PATH.exists():
        scores = pd.read_csv(SCORE_PATH, encoding="utf-8-sig")
    else:
        scores = SmokeIndexScorer().score(features)
    return scores, features


def main() -> None:
    st.title("企业风险画像平台")
    st.caption("基于工商、财务、司法、处罚和舆情数据的可解释风险分析")

    try:
        scores, features = load_data()
    except Exception as error:
        st.error(f"风险数据加载失败：{type(error).__name__}: {error}")
        st.code(
            ".\\.venv\\Scripts\\python.exe -m src.analysis.risk_analysis\n"
            ".\\.venv\\Scripts\\python.exe -m src.scoring.smoke_index"
        )
        return

    high_risk_count = int(scores["risk_level"].str.startswith(("D-", "E-"), na=False).sum())
    average_score = scores["total_score"].mean()
    top_score = scores["total_score"].max()

    metric_columns = st.columns(4)
    metric_columns[0].metric("企业数量", f"{len(scores):,}")
    metric_columns[1].metric("高风险企业", f"{high_risk_count:,}")
    metric_columns[2].metric("平均风险分", f"{average_score:.2f}")
    metric_columns[3].metric("最高风险分", f"{top_score:.2f}")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("风险等级分布")
        distribution = scores["risk_level"].value_counts().rename_axis("risk_level").reset_index(name="count")
        fig = px.bar(distribution, x="risk_level", y="count", color="risk_level", text="count")
        fig.update_layout(showlegend=False, xaxis_title="风险等级", yaxis_title="企业数量")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("行业风险概览")
        industry = scores.groupby("industry", as_index=False).agg(
            average_score=("total_score", "mean"), company_count=("company_id", "count")
        ).sort_values("average_score", ascending=False).head(10)
        fig = px.bar(industry, x="average_score", y="industry", orientation="h", text="company_count")
        fig.update_layout(xaxis_title="平均风险分", yaxis_title="行业")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("企业查询")
    keyword = st.text_input("搜索企业名称", placeholder="例如：科技、制造、供应链")
    filtered = scores[scores["company_name"].str.contains(keyword, case=False, na=False)] if keyword else scores
    filtered = filtered.sort_values("total_score", ascending=False)
    if filtered.empty:
        st.warning("没有找到匹配的企业。")
        return

    selected_id = st.selectbox(
        "选择企业",
        filtered["company_id"].tolist(),
        format_func=lambda company_id: f"{company_id} - {scores.loc[scores['company_id'].eq(company_id), 'company_name'].iloc[0]}",
    )
    selected = scores[scores["company_id"].eq(selected_id)].iloc[0]
    selected_features = features[features["company_id"].eq(selected_id)]
    st.dataframe(filtered.head(20), use_container_width=True, hide_index=True)

    st.subheader(f"{selected['company_name']} 风险画像")
    detail_columns = st.columns(5)
    detail_columns[0].metric("Smoke Index", f"{selected['total_score']:.2f}")
    detail_columns[1].metric("风险等级", selected["risk_level"])
    detail_columns[2].metric("财务风险", f"{selected['financial_score']:.2f}")
    detail_columns[3].metric("司法风险", f"{selected['lawsuit_score']:.2f}")
    detail_columns[4].metric("处罚风险", f"{selected['penalty_score']:.2f}")
    st.info(f"风险摘要：{selected['risk_summary']}")
    st.markdown(f"[打开 {selected['company_name']} 的风险报告](http://127.0.0.1:8000/reports/{int(selected_id)})")

    factors = pd.DataFrame(
        {"风险因素": ["财务", "司法", "处罚", "舆情"], "分数": [selected["financial_score"], selected["lawsuit_score"], selected["penalty_score"], selected["opinion_score"]]}
    )
    st.plotly_chart(px.bar(factors, x="风险因素", y="分数", range_y=[0, 100], text_auto=".2f"), use_container_width=True)
    if not selected_features.empty:
        st.caption("特征数据")
        st.dataframe(selected_features, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
