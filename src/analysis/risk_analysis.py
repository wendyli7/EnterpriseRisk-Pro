"""
risk_analysis.py

Build enterprise-level risk features from the five core business tables.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.database.db_connect import database


class RiskFeatureBuilder:
    """Aggregate multi-table business data into enterprise risk features."""

    def __init__(self) -> None:
        self.engine = database.engine
        self.project_root = Path(__file__).resolve().parents[2]
        self.output_path = (
            self.project_root / "data" / "processed" / "enterprise_risk_features.csv"
        )
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def build(self) -> pd.DataFrame:
        company_basic = self._read_table("company_basic")
        company_financial = self._read_table("company_financial")
        company_lawsuit = self._read_table("company_lawsuit")
        company_penalty = self._read_table("company_penalty")
        company_opinion = self._read_table("company_opinion")

        base_features = self._build_base_features(company_basic)
        financial_features = self._build_financial_features(company_financial)
        lawsuit_features = self._build_lawsuit_features(company_lawsuit)
        penalty_features = self._build_penalty_features(company_penalty)
        opinion_features = self._build_opinion_features(company_opinion)

        feature_table = (
            base_features.merge(financial_features, on="company_id", how="left")
            .merge(lawsuit_features, on="company_id", how="left")
            .merge(penalty_features, on="company_id", how="left")
            .merge(opinion_features, on="company_id", how="left")
        )

        feature_table = feature_table.fillna(
            {
                "total_assets": 0,
                "total_liabilities": 0,
                "operating_income": 0,
                "net_profit": 0,
                "asset_liability_ratio": 0,
                "revenue_to_assets_ratio": 0,
                "profit_margin": 0,
                "is_loss_making": 0,
                "lawsuit_count": 0,
                "high_risk_lawsuit_count": 0,
                "medium_risk_lawsuit_count": 0,
                "lawsuit_last_12m_count": 0,
                "penalty_count": 0,
                "penalty_total_amount": 0,
                "penalty_avg_amount": 0,
                "penalty_last_12m_count": 0,
                "opinion_count": 0,
                "negative_opinion_count": 0,
                "neutral_opinion_count": 0,
                "positive_opinion_count": 0,
                "negative_opinion_ratio": 0,
                "opinion_last_90d_count": 0,
            }
        )

        return feature_table.sort_values("company_id").reset_index(drop=True)

    def save(self, dataframe: pd.DataFrame) -> Path:
        dataframe.to_csv(self.output_path, index=False, encoding="utf-8-sig")
        return self.output_path

    def _read_table(self, table_name: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table_name}", con=self.engine)

    def _build_base_features(self, company_basic: pd.DataFrame) -> pd.DataFrame:
        dataframe = company_basic.copy()
        dataframe["establish_date"] = pd.to_datetime(dataframe["establish_date"])
        today = pd.Timestamp.today().normalize()

        dataframe["company_age_years"] = (
            (today - dataframe["establish_date"]).dt.days / 365.25
        ).round(2)
        dataframe["registered_capital"] = pd.to_numeric(
            dataframe["registered_capital"], errors="coerce"
        ).fillna(0)
        dataframe["is_abnormal_status"] = (
            dataframe["business_status"].fillna("").ne("存续")
        ).astype(int)

        return dataframe[
            [
                "company_id",
                "company_name",
                "industry",
                "province",
                "city",
                "business_status",
                "registered_capital",
                "company_age_years",
                "is_abnormal_status",
            ]
        ]

    def _build_financial_features(self, company_financial: pd.DataFrame) -> pd.DataFrame:
        dataframe = company_financial.copy()
        numeric_columns = [
            "total_assets",
            "total_liabilities",
            "operating_income",
            "net_profit",
            "asset_liability_ratio",
        ]
        for column in numeric_columns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

        latest_financial = (
            dataframe.sort_values(["company_id", "fiscal_year"])
            .groupby("company_id", as_index=False)
            .tail(1)
            .copy()
        )

        latest_financial["revenue_to_assets_ratio"] = (
            latest_financial["operating_income"] / latest_financial["total_assets"]
        ).replace([pd.NA, float("inf"), float("-inf")], 0)
        latest_financial["profit_margin"] = (
            latest_financial["net_profit"] / latest_financial["operating_income"]
        ).replace([pd.NA, float("inf"), float("-inf")], 0)
        latest_financial["is_loss_making"] = (
            latest_financial["net_profit"] < 0
        ).astype(int)

        return latest_financial[
            [
                "company_id",
                "fiscal_year",
                "total_assets",
                "total_liabilities",
                "operating_income",
                "net_profit",
                "asset_liability_ratio",
                "revenue_to_assets_ratio",
                "profit_margin",
                "is_loss_making",
            ]
        ]

    def _build_lawsuit_features(self, company_lawsuit: pd.DataFrame) -> pd.DataFrame:
        if company_lawsuit.empty:
            return pd.DataFrame(columns=[
                "company_id",
                "lawsuit_count",
                "high_risk_lawsuit_count",
                "medium_risk_lawsuit_count",
                "lawsuit_last_12m_count",
            ])

        dataframe = company_lawsuit.copy()
        dataframe["filing_date"] = pd.to_datetime(dataframe["filing_date"])
        last_12_months = pd.Timestamp.today().normalize() - pd.Timedelta(days=365)

        summary = dataframe.groupby("company_id").agg(
            lawsuit_count=("case_number", "count"),
            high_risk_lawsuit_count=("risk_level", lambda x: (x == "HIGH").sum()),
            medium_risk_lawsuit_count=("risk_level", lambda x: (x == "MEDIUM").sum()),
            lawsuit_last_12m_count=(
                "filing_date",
                lambda x: (x >= last_12_months).sum(),
            ),
        )
        return summary.reset_index()

    def _build_penalty_features(self, company_penalty: pd.DataFrame) -> pd.DataFrame:
        if company_penalty.empty:
            return pd.DataFrame(columns=[
                "company_id",
                "penalty_count",
                "penalty_total_amount",
                "penalty_avg_amount",
                "penalty_last_12m_count",
            ])

        dataframe = company_penalty.copy()
        dataframe["penalty_amount"] = pd.to_numeric(
            dataframe["penalty_amount"], errors="coerce"
        ).fillna(0)
        dataframe["penalty_date"] = pd.to_datetime(dataframe["penalty_date"])
        last_12_months = pd.Timestamp.today().normalize() - pd.Timedelta(days=365)

        summary = dataframe.groupby("company_id").agg(
            penalty_count=("penalty_amount", "count"),
            penalty_total_amount=("penalty_amount", "sum"),
            penalty_avg_amount=("penalty_amount", "mean"),
            penalty_last_12m_count=(
                "penalty_date",
                lambda x: (x >= last_12_months).sum(),
            ),
        )
        return summary.reset_index()

    def _build_opinion_features(self, company_opinion: pd.DataFrame) -> pd.DataFrame:
        if company_opinion.empty:
            return pd.DataFrame(columns=[
                "company_id",
                "opinion_count",
                "negative_opinion_count",
                "neutral_opinion_count",
                "positive_opinion_count",
                "negative_opinion_ratio",
                "opinion_last_90d_count",
            ])

        dataframe = company_opinion.copy()
        dataframe["publish_date"] = pd.to_datetime(dataframe["publish_date"])
        last_90_days = pd.Timestamp.today().normalize() - pd.Timedelta(days=90)

        summary = dataframe.groupby("company_id").agg(
            opinion_count=("news_title", "count"),
            negative_opinion_count=("sentiment", lambda x: (x == "negative").sum()),
            neutral_opinion_count=("sentiment", lambda x: (x == "neutral").sum()),
            positive_opinion_count=("sentiment", lambda x: (x == "positive").sum()),
            opinion_last_90d_count=(
                "publish_date",
                lambda x: (x >= last_90_days).sum(),
            ),
        )
        summary["negative_opinion_ratio"] = (
            summary["negative_opinion_count"] / summary["opinion_count"]
        ).fillna(0)
        return summary.reset_index()


def main() -> None:
    builder = RiskFeatureBuilder()
    feature_table = builder.build()
    output_path = builder.save(feature_table)

    print(f"Feature table built successfully: {len(feature_table)} rows")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
