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
            dataframe.to_sql(
                name=table_name,
                con=self.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=500,
            )
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


def main() -> None:
    importer = DemoDataImporter()
    importer.import_all()
    print("Demo data import completed.")


if __name__ == "__main__":
    main()
