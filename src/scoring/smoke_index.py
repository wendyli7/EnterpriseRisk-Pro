"""
smoke_index.py

Rule-based enterprise risk scoring for the MVP demo pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.analysis.risk_analysis import RiskFeatureBuilder


@dataclass(frozen=True)
class ScoreWeights:
    financial: float = 0.35
    lawsuit: float = 0.25
    penalty: float = 0.20
    opinion: float = 0.20


class SmokeIndexScorer:
    """Calculate interpretable risk scores from engineered risk features."""

    def __init__(self, weights: ScoreWeights | None = None) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.feature_path = self.project_root / "data" / "processed" / "enterprise_risk_features.csv"
        self.output_path = self.project_root / "data" / "processed" / "enterprise_smoke_index.csv"
        self.weights = weights or ScoreWeights()

    def score(self, features: pd.DataFrame | None = None) -> pd.DataFrame:
        dataframe = features.copy() if features is not None else self._load_or_build_features()

        dataframe["financial_score"] = dataframe.apply(self._financial_score, axis=1)
        dataframe["lawsuit_score"] = dataframe.apply(self._lawsuit_score, axis=1)
        dataframe["penalty_score"] = dataframe.apply(self._penalty_score, axis=1)
        dataframe["opinion_score"] = dataframe.apply(self._opinion_score, axis=1)
        dataframe["total_score"] = dataframe.apply(self._total_score, axis=1).round(2)
        dataframe["risk_level"] = dataframe["total_score"].apply(self._risk_level)
        dataframe["risk_summary"] = dataframe.apply(self._risk_summary, axis=1)

        columns = [
            "company_id",
            "company_name",
            "industry",
            "province",
            "city",
            "financial_score",
            "lawsuit_score",
            "penalty_score",
            "opinion_score",
            "total_score",
            "risk_level",
            "risk_summary",
        ]
        return dataframe[columns].sort_values("total_score", ascending=False).reset_index(drop=True)

    def save(self, dataframe: pd.DataFrame) -> Path:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        return self.output_path

    def _load_or_build_features(self) -> pd.DataFrame:
        if self.feature_path.exists():
            return pd.read_csv(self.feature_path, encoding="utf-8-sig")
        builder = RiskFeatureBuilder(source="auto")
        features = builder.build()
        builder.save(features)
        return features

    def _financial_score(self, row: pd.Series) -> float:
        score = 0.0
        asset_liability_ratio = float(row.get("asset_liability_ratio", 0))
        profit_margin = float(row.get("profit_margin", 0))
        revenue_to_assets_ratio = float(row.get("revenue_to_assets_ratio", 0))

        if asset_liability_ratio >= 85:
            score += 35
        elif asset_liability_ratio >= 70:
            score += 24
        elif asset_liability_ratio >= 55:
            score += 12

        if int(row.get("is_loss_making", 0)) == 1:
            score += 25
        elif profit_margin < 0.03:
            score += 12

        if revenue_to_assets_ratio < 0.35:
            score += 15
        if int(row.get("is_abnormal_status", 0)) == 1:
            score += 25
        return min(score, 100.0)

    def _lawsuit_score(self, row: pd.Series) -> float:
        score = float(row.get("lawsuit_count", 0)) * 10
        score += float(row.get("medium_risk_lawsuit_count", 0)) * 8
        score += float(row.get("high_risk_lawsuit_count", 0)) * 18
        score += float(row.get("lawsuit_last_12m_count", 0)) * 10
        return min(score, 100.0)

    def _penalty_score(self, row: pd.Series) -> float:
        score = float(row.get("penalty_count", 0)) * 18
        score += min(float(row.get("penalty_total_amount", 0)) / 10, 35)
        score += float(row.get("penalty_last_12m_count", 0)) * 12
        return min(score, 100.0)

    def _opinion_score(self, row: pd.Series) -> float:
        score = float(row.get("negative_opinion_ratio", 0)) * 65
        score += float(row.get("negative_opinion_count", 0)) * 8
        score += float(row.get("opinion_last_90d_count", 0)) * 5
        return min(score, 100.0)

    def _total_score(self, row: pd.Series) -> float:
        return (
            row["financial_score"] * self.weights.financial
            + row["lawsuit_score"] * self.weights.lawsuit
            + row["penalty_score"] * self.weights.penalty
            + row["opinion_score"] * self.weights.opinion
        )

    @staticmethod
    def _risk_level(score: float) -> str:
        if score >= 80:
            return "E-严重风险"
        if score >= 60:
            return "D-高风险"
        if score >= 40:
            return "C-关注风险"
        if score >= 20:
            return "B-一般风险"
        return "A-低风险"

    @staticmethod
    def _risk_summary(row: pd.Series) -> str:
        reasons: list[str] = []
        if row["financial_score"] >= 50:
            reasons.append("财务压力较高")
        if row["lawsuit_score"] >= 40:
            reasons.append("司法案件风险突出")
        if row["penalty_score"] >= 35:
            reasons.append("行政处罚记录较多")
        if row["opinion_score"] >= 35:
            reasons.append("负面舆情占比较高")
        return "；".join(reasons) if reasons else "暂无显著风险信号"


def main() -> None:
    scorer = SmokeIndexScorer()
    scored = scorer.score()
    output_path = scorer.save(scored)
    print(f"Smoke index calculated successfully: {len(scored)} rows")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
