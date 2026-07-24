"""
import_demo_data.py

Import generated demo CSV files into MySQL in foreign-key-safe order.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.database.db_connect import database
from src.utils.config import config


TABLE_FILE_MAPPING = [
    ("company_basic", "company_basic.csv"),
    ("company_financial", "company_financial.csv"),
    ("company_lawsuit", "company_lawsuit.csv"),
    ("company_penalty", "company_penalty.csv"),
    ("company_opinion", "company_opinion.csv"),
]

TABLE_COLUMNS = {
    "company_basic": [
        "company_id",
        "company_name",
        "unified_code",
        "legal_person",
        "registered_capital",
        "establish_date",
        "industry",
        "province",
        "city",
        "business_status",
    ],
    "company_financial": [
        "company_id",
        "fiscal_year",
        "total_assets",
        "total_liabilities",
        "operating_income",
        "net_profit",
        "asset_liability_ratio",
    ],
    "company_lawsuit": [
        "company_id",
        "case_number",
        "case_type",
        "plaintiff",
        "defendant",
        "filing_date",
        "judgment_result",
        "risk_level",
    ],
    "company_penalty": [
        "company_id",
        "penalty_authority",
        "penalty_reason",
        "penalty_amount",
        "penalty_date",
    ],
    "company_opinion": [
        "company_id",
        "news_title",
        "news_source",
        "sentiment",
        "publish_date",
        "url",
    ],
}


class DemoDataImporter:
    """Load generated sample CSV files into the project database."""

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        output_config = config.get_output_config()
        self.sample_dir = project_root / output_config.get("csv_path", "data/sample")
        self.engine = database.engine

    def import_all(self) -> None:
        self._validate_files()
        self._truncate_tables()

        for table_name, filename in TABLE_FILE_MAPPING:
            dataframe = self._read_csv(filename)
            self._insert_dataframe(table_name, dataframe)
            print(f"Imported {len(dataframe)} rows into {table_name}.")

    def _validate_files(self) -> None:
        missing_files = [
            filename
            for _, filename in TABLE_FILE_MAPPING
            if not (self.sample_dir / filename).exists()
        ]
        if missing_files:
            missing_text = ", ".join(missing_files)
            raise FileNotFoundError(
                f"Missing sample files in {self.sample_dir}: {missing_text}"
            )

    def _truncate_tables(self) -> None:
        # Child tables must be cleared before the parent table.
        truncate_order = [table_name for table_name, _ in reversed(TABLE_FILE_MAPPING)]

        with self.engine.begin() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            try:
                for table_name in truncate_order:
                    connection.execute(text(f"TRUNCATE TABLE {table_name}"))
            finally:
                connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    def _read_csv(self, filename: str) -> pd.DataFrame:
        path = self.sample_dir / filename
        return pd.read_csv(path, encoding="utf-8-sig")

    def _insert_dataframe(self, table_name: str, dataframe: pd.DataFrame) -> None:
        columns = TABLE_COLUMNS[table_name]
        placeholders = ", ".join(f":{column}" for column in columns)
        column_list = ", ".join(columns)
        statement = text(
            f"INSERT INTO {table_name} ({column_list}) VALUES ({placeholders})"
        )

        records = dataframe[columns].where(pd.notnull(dataframe[columns]), None)
        payload = records.to_dict(orient="records")

        with self.engine.begin() as connection:
            connection.execute(statement, payload)


def main() -> None:
    importer = DemoDataImporter()
    importer.import_all()
    print("Demo data import completed.")


if __name__ == "__main__":
    main()
