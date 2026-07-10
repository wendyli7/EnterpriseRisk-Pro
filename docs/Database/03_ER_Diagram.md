# EnterpriseRisk-Pro

# Entity Relationship Diagram (ER Diagram)

**Version:** V1.0  
**Author:** Wendy Li  
**Last Updated:** 2026-07-10

---

# 1. Database Relationship Overview

The EnterpriseRisk-Pro database adopts a **Company-Centered** architecture.

The `company_basic` table is the core entity.

All business tables are associated through the `company_id` field.

---

# 2. Entity Relationship Diagram

```mermaid
erDiagram

company_basic {

BIGINT company_id PK

VARCHAR company_name

VARCHAR unified_code

VARCHAR legal_person

DECIMAL registered_capital

DATE establish_date

VARCHAR industry

VARCHAR province

VARCHAR city

VARCHAR business_status

}

company_financial {

BIGINT financial_id PK

BIGINT company_id FK

DECIMAL total_assets

DECIMAL total_liabilities

DECIMAL revenue

DECIMAL net_profit

}

company_lawsuit {

BIGINT lawsuit_id PK

BIGINT company_id FK

VARCHAR case_number

VARCHAR case_type

DATE filing_date

VARCHAR court

}

company_penalty {

BIGINT penalty_id PK

BIGINT company_id FK

VARCHAR penalty_type

DECIMAL penalty_amount

DATE penalty_date

VARCHAR authority

}

company_opinion {

BIGINT opinion_id PK

BIGINT company_id FK

VARCHAR news_title

VARCHAR sentiment

DATE publish_date

}

risk_tag {

BIGINT tag_id PK

BIGINT company_id FK

VARCHAR tag_name

VARCHAR tag_level

}

risk_score {

BIGINT score_id PK

BIGINT company_id FK

DECIMAL score

VARCHAR risk_level

DATE evaluation_date

}

risk_warning {

BIGINT warning_id PK

BIGINT company_id FK

VARCHAR warning_type

VARCHAR warning_level

DATE warning_date

}

company_basic ||--o{ company_financial : contains

company_basic ||--o{ company_lawsuit : contains

company_basic ||--o{ company_penalty : contains

company_basic ||--o{ company_opinion : contains

company_basic ||--o{ risk_tag : owns

company_basic ||--o{ risk_score : generates

company_basic ||--o{ risk_warning : triggers
```

---

# 3. Relationship Description

## company_basic

Core table of the database.

Stores enterprise master data.

---

## company_financial

Stores enterprise financial indicators.

Relationship:

One Company → Multiple Financial Records

---

## company_lawsuit

Stores judicial litigation records.

Relationship:

One Company → Multiple Lawsuits

---

## company_penalty

Stores administrative penalty records.

Relationship:

One Company → Multiple Penalties

---

## company_opinion

Stores public opinion and news information.

Relationship:

One Company → Multiple News Records

---

## risk_tag

Stores enterprise risk labels.

Relationship:

One Company → Multiple Risk Tags

---

## risk_score

Stores machine learning prediction results.

Relationship:

One Company → Multiple Risk Scores

---

## risk_warning

Stores early warning records.

Relationship:

One Company → Multiple Warning Records

---

# 4. Database Design Principles

- One enterprise corresponds to one master record.
- Business tables are linked through `company_id`.
- All tables satisfy Third Normal Form (3NF).
- Foreign keys ensure data integrity.
- Indexes will be added on high-frequency query fields.

---

# End of Document