"""Persist the latest rule-based risk results into MySQL."""

from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import text

from src.database.db_connect import database
from src.scoring.smoke_index import SmokeIndexScorer


LEVEL_MAPPING = {
    "A-低风险": "LOW",
    "B-一般风险": "MEDIUM",
    "C-关注风险": "MEDIUM",
    "D-高风险": "HIGH",
    "E-严重风险": "HIGH",
}


def persist_results(scored: pd.DataFrame | None = None) -> int:
    """Replace the current persisted score snapshot and return its row count."""
    dataframe = scored if scored is not None else SmokeIndexScorer().score()
    evaluation_date = date.today()

    score_rows = dataframe[
        [
            "company_id",
            "financial_score",
            "lawsuit_score",
            "penalty_score",
            "opinion_score",
            "total_score",
            "risk_level",
        ]
    ].copy()
    score_rows["risk_level"] = score_rows["risk_level"].map(LEVEL_MAPPING)
    score_rows["evaluation_date"] = evaluation_date

    smoke_rows = score_rows[["company_id", "total_score", "risk_level"]].rename(
        columns={"total_score": "smoke_index", "risk_level": "smoke_level"}
    )
    smoke_rows["calculation_version"] = "smoke-index-v1"

    with database.engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE risk_score"))
        connection.execute(text("TRUNCATE TABLE smoke_index_result"))

        score_sql = text(
            """INSERT INTO risk_score
            (company_id, financial_score, lawsuit_score, penalty_score,
             opinion_score, total_score, risk_level, evaluation_date)
            VALUES (:company_id, :financial_score, :lawsuit_score, :penalty_score,
                    :opinion_score, :total_score, :risk_level, :evaluation_date)"""
        )
        smoke_sql = text(
            """INSERT INTO smoke_index_result
            (company_id, smoke_index, smoke_level, calculation_version)
            VALUES (:company_id, :smoke_index, :smoke_level, :calculation_version)"""
        )
        connection.execute(score_sql, score_rows.to_dict(orient="records"))
        connection.execute(smoke_sql, smoke_rows.to_dict(orient="records"))

    return len(score_rows)


def main() -> None:
    count = persist_results()
    print(f"Persisted {count} risk scores and smoke index results.")


if __name__ == "__main__":
    main()
