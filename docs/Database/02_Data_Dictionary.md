# EnterpriseRisk-Pro

# Data Dictionary

**Version:** V1.0  
**Author:** Wendy Li  
**Last Updated:** 2026-07-10

---

# 1. Document Overview

## 1.1 Purpose

This document defines the data dictionary for the EnterpriseRisk-Pro database. It specifies the structure, field definitions, data types, and naming conventions of each table to ensure consistency during database development and future maintenance.

---

# 2. Database Information

| Item | Value |
|------|-------|
| Database Name | enterprise_risk_db |
| Database Type | MySQL 8.0 |
| Storage Engine | InnoDB |
| Character Set | utf8mb4 |

---

# 3. Table Dictionary

## 3.1 Table：company_basic

### Business Description

Stores the basic information of enterprises. This is the core table of the entire database, and all business tables are associated with it through **company_id**.

### Table Structure

| Field Name | Data Type | Length | Primary Key | Nullable | Description |
|------------|-----------|--------|-------------|----------|-------------|
| company_id | BIGINT | - | Yes | No | Enterprise ID |
| company_name | VARCHAR | 200 | No | No | Enterprise Name |
| unified_code | VARCHAR | 18 | No | No | Unified Social Credit Code |
| legal_person | VARCHAR | 100 | No | Yes | Legal Representative |
| registered_capital | DECIMAL | 18,2 | No | Yes | Registered Capital |
| establish_date | DATE | - | No | Yes | Establishment Date |
| industry | VARCHAR | 100 | No | Yes | Industry |
| province | VARCHAR | 50 | No | Yes | Province |
| city | VARCHAR | 50 | No | Yes | City |
| business_status | VARCHAR | 50 | No | Yes | Business Status |
| create_time | DATETIME | - | No | No | Record Creation Time |
| update_time | DATETIME | - | No | No | Record Update Time |

---

# 4. Naming Conventions

## Table Naming

- Use lowercase letters.
- Use underscores (_) to separate words.
- Use business-oriented names.

Example:

company_basic

company_financial

company_lawsuit

risk_score

---

## Field Naming

- Use lowercase letters.
- Separate words with underscores.
- Avoid abbreviations.

Example:

company_name

registered_capital

business_status

create_time

---

## Primary Key Naming

All primary keys follow the format:

company_id

---

## Foreign Key Naming

Foreign keys use the same field name as the referenced primary key.

Example:

company_id

---

# 5. Data Type Standards

| Data Type | Usage |
|------------|------|
| BIGINT | Primary Key |
| VARCHAR | Text |
| DATE | Date |
| DATETIME | Timestamp |
| DECIMAL | Financial Amount |
| INT | Integer |

---

# 6. Database Constraints

## Primary Key

Each table must contain one primary key.

Example:

company_id

---

## Unique Constraint

The unified social credit code must be unique.

Field:

unified_code

---

## Character Set

utf8mb4

---

## Storage Engine

InnoDB

---

# 7. Index Design (Planned)

The following indexes will be created during SQL implementation.

| Index | Field |
|--------|-------|
| PK_company | company_id |
| IDX_company_name | company_name |
| IDX_unified_code | unified_code |
| IDX_industry | industry |

---

# 8. Future Tables

The following tables will be added in future versions.

- company_financial
- company_lawsuit
- company_penalty
- company_opinion
- risk_tag
- risk_score
- risk_warning
- smoke_index_result
- risk_report

---

# End of Document