"""
generate_company_data.py

Generate demo enterprise risk data that matches the current MySQL table design.
The script writes CSV samples for the core source tables so the next steps
(cleaning, loading, scoring, and API integration) can share the same baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from random import Random
from typing import Iterable

import pandas as pd

try:
    from src.utils.config import config
except ModuleNotFoundError:
    config = None


INDUSTRIES = [
    "???",
    "????",
    "????",
    "????",
    "????",
    "???",
    "????",
    "????",
    "????",
    "?????",
]

PROVINCE_CITY = {
    "???": ["???"],
    "???": ["???"],
    "???": ["???", "???", "???", "???"],
    "???": ["???", "???", "???"],
    "???": ["???", "???", "???"],
    "???": ["???", "???"],
    "???": ["???", "???"],
    "???": ["???", "???"],
}

BUSINESS_STATUSES = ["??", "??", "??", "??"]
CASE_TYPES = ["??????", "????", "????????", "??????"]
PLAINTIFF_TYPES = ["???", "??", "??", "??"]
JUDGMENT_RESULTS = [
    "??????",
    "????????",
    "????",
    "?????????",
]
PENALTY_AUTHORITIES = ["???????", "???", "?????", "?????"]
PENALTY_REASONS = ["???????", "??????", "???????", "?????????"]
NEWS_SOURCES = ["????", "?????", "???", "??????", "????"]
NEGATIVE_TITLES = [
    "????????",
    "?????????",
    "??????????",
    "?????????",
]
POSITIVE_TITLES = [
    "???????",
    "????????",
    "????????",
    "????????",
]

SURNAMES = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?"]
GIVEN_NAMES = ["?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?", "?"]
COMPANY_BRANDS = ["??", "??", "??", "??", "??", "??", "??", "??", "??", "??"]


@dataclass
class GeneratedData:
    company_basic: pd.DataFrame
    company_financial: pd.DataFrame
    company_lawsuit: pd.DataFrame
    company_penalty: pd.DataFrame
    company_opinion: pd.DataFrame


class DemoDataGenerator:
    """Generate sample enterprise risk data for local development and demos."""

    def __init__(self) -> None:
        generator_config = self._load_generator_config()
        output_config = self._load_output_config()

        self.company_count = int(generator_config.get("company_count", 100))
        self.random_seed = int(generator_config.get("random_seed", 2026))
        self.random = Random(self.random_seed)

        project_root = Path(__file__).resolve().parents[2]
        self.output_dir = project_root / output_config.get("csv_path", "data/sample")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _load_generator_config() -> dict[str, object]:
        if config is None:
            return {"company_count": 100, "random_seed": 2026}
        return config.get_generator_config()

    @staticmethod
    def _load_output_config() -> dict[str, object]:
        if config is None:
            return {"csv_path": "data/sample"}
        return config.get_output_config()

    def generate(self) -> GeneratedData:
        companies = self._generate_company_basic()
        financials = self._generate_company_financial(companies)
        lawsuits = self._generate_company_lawsuit(companies)
        penalties = self._generate_company_penalty(companies)
        opinions = self._generate_company_opinion(companies)

        return GeneratedData(
            company_basic=companies,
            company_financial=financials,
            company_lawsuit=lawsuits,
            company_penalty=penalties,
            company_opinion=opinions,
        )

    def save(self, data: GeneratedData) -> list[Path]:
        outputs = {
            "company_basic.csv": data.company_basic,
            "company_financial.csv": data.company_financial,
            "company_lawsuit.csv": data.company_lawsuit,
            "company_penalty.csv": data.company_penalty,
            "company_opinion.csv": data.company_opinion,
        }

        saved_files: list[Path] = []
        for filename, dataframe in outputs.items():
            target = self.output_dir / filename
            dataframe.to_csv(target, index=False, encoding="utf-8-sig")
            saved_files.append(target)
        return saved_files

    def _generate_company_basic(self) -> pd.DataFrame:
        records: list[dict[str, object]] = []
        for company_id in range(1, self.company_count + 1):
            province = self.random.choice(list(PROVINCE_CITY.keys()))
            city = self.random.choice(PROVINCE_CITY[province])
            establish_date = self._random_date(365, 365 * 20)
            registered_capital = self._money(self.random.uniform(500, 50000))
            company_name = self._company_name()

            records.append(
                {
                    "company_id": company_id,
                    "company_name": company_name,
                    "unified_code": self._credit_code(company_id),
                    "legal_person": self._person_name(),
                    "registered_capital": registered_capital,
                    "establish_date": establish_date.isoformat(),
                    "industry": self.random.choice(INDUSTRIES),
                    "province": province,
                    "city": city,
                    "business_status": self.random.choices(
                        BUSINESS_STATUSES,
                        weights=[0.70, 0.20, 0.05, 0.05],
                        k=1,
                    )[0],
                }
            )
        return pd.DataFrame(records)

    def _generate_company_financial(self, companies: pd.DataFrame) -> pd.DataFrame:
        current_year = date.today().year
        records: list[dict[str, object]] = []
        for row in companies.itertuples(index=False):
            base_assets = float(row.registered_capital) * self.random.uniform(1.2, 4.0)
            for fiscal_year in range(current_year - 2, current_year + 1):
                assets = self._money(base_assets * self.random.uniform(0.9, 1.2))
                ratio = self.random.uniform(25, 92)
                liabilities = self._money(float(assets) * ratio / 100)
                operating_income = self._money(float(assets) * self.random.uniform(0.4, 1.8))
                net_profit = self._money(float(operating_income) * self.random.uniform(-0.08, 0.20))
                records.append(
                    {
                        "company_id": row.company_id,
                        "fiscal_year": fiscal_year,
                        "total_assets": assets,
                        "total_liabilities": liabilities,
                        "operating_income": operating_income,
                        "net_profit": net_profit,
                        "asset_liability_ratio": self._decimal(ratio),
                    }
                )
        return pd.DataFrame(records)

    def _generate_company_lawsuit(self, companies: pd.DataFrame) -> pd.DataFrame:
        records: list[dict[str, object]] = []
        for row in companies.itertuples(index=False):
            lawsuit_count = self.random.choices([0, 1, 2, 3], weights=[0.45, 0.30, 0.18, 0.07], k=1)[0]
            for index in range(lawsuit_count):
                filing_date = self._random_date(1, 365 * 3)
                plaintiff_type = self.random.choice(PLAINTIFF_TYPES)
                records.append(
                    {
                        "company_id": row.company_id,
                        "case_number": f"({filing_date.year}){row.province[:1]}01??{row.company_id:04d}{index + 1:02d}?",
                        "case_type": self.random.choice(CASE_TYPES),
                        "plaintiff": f"{plaintiff_type}{self._company_name()}",
                        "defendant": row.company_name,
                        "filing_date": filing_date.isoformat(),
                        "judgment_result": self.random.choice(JUDGMENT_RESULTS),
                        "risk_level": self.random.choices(["LOW", "MEDIUM", "HIGH"], weights=[0.50, 0.35, 0.15], k=1)[0],
                    }
                )
        return pd.DataFrame(records)

    def _generate_company_penalty(self, companies: pd.DataFrame) -> pd.DataFrame:
        records: list[dict[str, object]] = []
        for row in companies.itertuples(index=False):
            penalty_count = self.random.choices([0, 1, 2], weights=[0.60, 0.28, 0.12], k=1)[0]
            for _ in range(penalty_count):
                penalty_amount = self._money(self.random.uniform(1, 120))
                penalty_date = self._random_date(1, 365 * 3)
                records.append(
                    {
                        "company_id": row.company_id,
                        "penalty_authority": self.random.choice(PENALTY_AUTHORITIES),
                        "penalty_reason": self.random.choice(PENALTY_REASONS),
                        "penalty_amount": penalty_amount,
                        "penalty_date": penalty_date.isoformat(),
                    }
                )
        return pd.DataFrame(records)

    def _generate_company_opinion(self, companies: pd.DataFrame) -> pd.DataFrame:
        records: list[dict[str, object]] = []
        for row in companies.itertuples(index=False):
            opinion_count = self.random.randint(1, 4)
            for index in range(opinion_count):
                sentiment = self.random.choices(
                    ["positive", "neutral", "negative"],
                    weights=[0.30, 0.40, 0.30],
                    k=1,
                )[0]
                title_prefix = self.random.choice(NEGATIVE_TITLES if sentiment == "negative" else POSITIVE_TITLES)
                publish_date = self._random_date(1, 365 * 2)
                records.append(
                    {
                        "company_id": row.company_id,
                        "news_title": f"{row.company_name}{title_prefix}",
                        "news_source": self.random.choice(NEWS_SOURCES),
                        "sentiment": sentiment,
                        "publish_date": publish_date.isoformat(),
                        "url": f"https://demo.enterprise-risk.local/news/{row.company_id}/{index + 1}",
                    }
                )
        return pd.DataFrame(records)

    def _company_name(self) -> str:
        prefix = self.random.choice(COMPANY_BRANDS)
        suffix = self.random.choice(["??????", "???????", "??????", "????????"])
        return f"{prefix}{suffix}"


    def _person_name(self) -> str:
        return f"{self.random.choice(SURNAMES)}{self.random.choice(GIVEN_NAMES)}{self.random.choice(GIVEN_NAMES)}"

    def _random_date(self, min_days_ago: int, max_days_ago: int) -> date:
        days_ago = self.random.randint(min_days_ago, max_days_ago)
        return date.today() - timedelta(days=days_ago)

    def _credit_code(self, company_id: int) -> str:
        return f"91{self.random_seed % 100:02d}{company_id:014d}"[:18]

    @staticmethod
    def _decimal(value: float) -> str:
        decimal_value = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return format(decimal_value, "f")

    def _money(self, value: float) -> str:
        return self._decimal(value)


def summarize(data: GeneratedData) -> Iterable[str]:
    yield f"company_basic: {len(data.company_basic)} rows"
    yield f"company_financial: {len(data.company_financial)} rows"
    yield f"company_lawsuit: {len(data.company_lawsuit)} rows"
    yield f"company_penalty: {len(data.company_penalty)} rows"
    yield f"company_opinion: {len(data.company_opinion)} rows"


def main() -> None:
    generator = DemoDataGenerator()
    data = generator.generate()
    saved_files = generator.save(data)

    print("Demo data generated successfully.")
    for line in summarize(data):
        print(f"- {line}")
    print("Saved files:")
    for path in saved_files:
        print(f"- {path}")


if __name__ == "__main__":
    main()
