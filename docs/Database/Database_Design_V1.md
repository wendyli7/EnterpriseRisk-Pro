# EnterpriseRisk-Pro

# Database Design Document

Version：V1.0

Author：Wendy Li

Date：2026-07-10

---

# 1. Document Overview

## 1.1 Purpose

This document describes the database design of the EnterpriseRisk-Pro system.

The database supports enterprise risk profiling, enterprise risk scoring, and enterprise risk early warning based on multi-source public data.

---

## 1.2 Database Information

| Item | Content |
|------|---------|
| Database Name | enterprise_risk_db |
| Database Type | MySQL 8.0 |
| Character Set | utf8mb4 |
| Storage Engine | InnoDB |

---

# 2. Business Overview

The system aims to build enterprise risk profiles by integrating multiple public data sources.

Main business modules include:

- Enterprise Basic Information
- Financial Information
- Judicial Litigation
- Administrative Penalty
- Public Opinion Monitoring
- Risk Tag Management
- Enterprise Risk Scoring
- Risk Early Warning

---

# 3. Database Architecture

enterprise_risk_db

├── company_basic

├── company_financial

├── company_lawsuit

├── company_penalty

├── company_opinion

├── risk_tag

├── risk_score

└── risk_warning

---

# 4. Entity Relationship

The company_basic table is the core table.

All business tables are associated through company_id.

Relationship:

company_basic

├── company_financial

├── company_lawsuit

├── company_penalty

├── company_opinion

├── risk_tag

├── risk_score

└── risk_warning

Relationship Type:

One Company → Multiple Risk Records

---

# 5. Table Design

## 5.1 company_basic

Business Description

Store enterprise basic information.

Primary Key

company_id

Fields

| Field | Type | Description |
|------|------|------------|
| company_id | BIGINT | Enterprise ID |
| company_name | VARCHAR(200) | Enterprise Name |
| unified_code | VARCHAR(18) | Unified Social Credit Code |
| legal_person | VARCHAR(100) | Legal Representative |
| registered_capital | DECIMAL(18,2) | Registered Capital |
| establish_date | DATE | Establishment Date |
| industry | VARCHAR(100) | Industry |
| province | VARCHAR(50) | Province |
| city | VARCHAR(50) | City |
| business_status | VARCHAR(50) | Business Status |
| create_time | DATETIME | Record Creation Time |
| update_time | DATETIME | Record Update Time |

---

# 6. Design Principles

The following principles are adopted during database design.

## Principle 1

Each enterprise has only one unique company_id.

## Principle 2

The Unified Social Credit Code is used as the unique business identifier.

## Principle 3

Business tables should not store duplicate enterprise information.

## Principle 4

All risk tables are associated with company_basic through company_id.

## Principle 5

The database follows Third Normal Form (3NF).

---

# 7. Future Database Expansion

The database supports future expansion.

Possible tables include:

- smoke_index_result
- enterprise_report
- user_operation_log
- crawler_log
- system_user
- role_permission

---

# 8. Next Development Plan

Sprint 2

Database Design

Sprint 3

SQL Development

Sprint 4

Data Collection

Sprint 5

Data Cleaning

Sprint 6

Feature Engineering

Sprint 7

Risk Modeling

Sprint 8

Dashboard Development

---

End of Document