"""Regression tests for the local enterprise risk pipeline."""

from __future__ import annotations

import unittest

import pandas as pd

from src.analysis.risk_analysis import RiskFeatureBuilder
from src.generator.generate_company_data import DemoDataGenerator
from src.scoring.smoke_index import SmokeIndexScorer


class PipelineTests(unittest.TestCase):
    def test_demo_generator_is_deterministic_and_complete(self) -> None:
        first = DemoDataGenerator().generate()
        second = DemoDataGenerator().generate()

        self.assertEqual(len(first.company_basic), 500)
        self.assertEqual(len(first.company_financial), 1500)
        self.assertEqual(len(first.company_opinion), 1250)
        self.assertEqual(first.company_basic["company_name"].nunique(), 500)
        pd.testing.assert_frame_equal(first.company_basic, second.company_basic)

    def test_feature_builder_returns_one_row_per_company(self) -> None:
        features = RiskFeatureBuilder(source="csv").build()

        self.assertEqual(len(features), 500)
        self.assertEqual(features["company_id"].nunique(), 500)
        required = {
            "asset_liability_ratio",
            "lawsuit_count",
            "penalty_count",
            "negative_opinion_ratio",
        }
        self.assertTrue(required.issubset(features.columns))
        self.assertFalse(features[list(required)].isna().any().any())

    def test_scorer_outputs_bounded_scores_and_levels(self) -> None:
        features = pd.DataFrame(
            [
                {
                    "company_id": 1,
                    "company_name": "High Risk Co",
                    "industry": "manufacturing",
                    "province": "test",
                    "city": "test",
                    "asset_liability_ratio": 95,
                    "profit_margin": -0.1,
                    "revenue_to_assets_ratio": 0.1,
                    "is_loss_making": 1,
                    "is_abnormal_status": 1,
                    "lawsuit_count": 4,
                    "high_risk_lawsuit_count": 2,
                    "medium_risk_lawsuit_count": 1,
                    "lawsuit_last_12m_count": 2,
                    "penalty_count": 3,
                    "penalty_total_amount": 500,
                    "penalty_last_12m_count": 2,
                    "negative_opinion_ratio": 1,
                    "negative_opinion_count": 4,
                    "opinion_last_90d_count": 2,
                },
                {
                    "company_id": 2,
                    "company_name": "Low Risk Co",
                    "industry": "technology",
                    "province": "test",
                    "city": "test",
                },
            ]
        )

        scored = SmokeIndexScorer().score(features)

        self.assertEqual(list(scored["risk_level"]), ["E-严重风险", "A-低风险"])
        self.assertTrue(scored["total_score"].between(0, 100).all())
        self.assertIn("财务压力较高", scored.iloc[0]["risk_summary"])
        self.assertEqual(scored.iloc[1]["risk_summary"], "暂无显著风险信号")


if __name__ == "__main__":
    unittest.main()