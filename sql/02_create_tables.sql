/*
====================================================
Project : EnterpriseRisk-Pro
Module  : Create Core Tables
Author  : Wendy Li
Version : V1.0
====================================================
*/

USE enterprise_risk_db;

-- ==========================
-- Table: company_basic
-- ==========================

CREATE TABLE company_basic (

    company_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '企业ID',

    company_name VARCHAR(200) NOT NULL COMMENT '企业名称',

    unified_code VARCHAR(18) NOT NULL UNIQUE COMMENT '统一社会信用代码',

    legal_person VARCHAR(100) COMMENT '法定代表人',

    registered_capital DECIMAL(18,2) COMMENT '注册资本（万元）',

    establish_date DATE COMMENT '成立日期',

    industry VARCHAR(100) COMMENT '所属行业',

    province VARCHAR(50) COMMENT '省份',

    city VARCHAR(50) COMMENT '城市',

    business_status VARCHAR(50) DEFAULT '存续' COMMENT '企业状态',

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业基础信息表';
-- ============================================
-- Table: company_financial
-- 企业财务信息
-- ============================================

CREATE TABLE company_financial (

    financial_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '财务记录ID',

    company_id BIGINT NOT NULL COMMENT '企业ID',

    fiscal_year YEAR NOT NULL COMMENT '财务年度',

    total_assets DECIMAL(18,2) COMMENT '总资产（万元)',

    total_liabilities DECIMAL(18,2) COMMENT '总负债（万元)',

    operating_income DECIMAL(18,2) COMMENT '营业收入（万元)',

    net_profit DECIMAL(18,2) COMMENT '净利润（万元)',

    asset_liability_ratio DECIMAL(6,2) COMMENT '资产负债率',

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_financial_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业财务信息表';
-- ============================================
-- Table: company_lawsuit
-- 企业司法信息
-- ============================================

CREATE TABLE company_lawsuit (

    lawsuit_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    case_number VARCHAR(200),

    case_type VARCHAR(100),

    plaintiff VARCHAR(200),

    defendant VARCHAR(200),

    filing_date DATE,

    judgment_result TEXT,

    risk_level VARCHAR(20),

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_lawsuit_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业司法诉讼表';
-- ============================================
-- Table: company_penalty
-- 行政处罚信息
-- ============================================

CREATE TABLE company_penalty (

    penalty_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    penalty_authority VARCHAR(200),

    penalty_reason TEXT,

    penalty_amount DECIMAL(18,2),

    penalty_date DATE,

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_penalty_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业行政处罚表';
-- ============================================
-- Table: company_opinion
-- 企业舆情信息
-- ============================================

CREATE TABLE company_opinion (

    opinion_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    news_title VARCHAR(300) NOT NULL,

    news_source VARCHAR(100),

    sentiment ENUM('positive','neutral','negative') DEFAULT 'neutral',

    publish_date DATE,

    url VARCHAR(500),

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_opinion_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业舆情信息表';
-- ============================================
-- Table: risk_tag
-- 风险标签
-- ============================================

CREATE TABLE risk_tag (

    tag_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    tag_name VARCHAR(100),

    tag_level ENUM('LOW','MEDIUM','HIGH'),

    tag_source VARCHAR(100),

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tag_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业风险标签表';
-- ============================================
-- Table: risk_score
-- 企业风险评分
-- ============================================

CREATE TABLE risk_score (

    score_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    financial_score DECIMAL(5,2),

    lawsuit_score DECIMAL(5,2),

    penalty_score DECIMAL(5,2),

    opinion_score DECIMAL(5,2),

    total_score DECIMAL(5,2),

    risk_level ENUM('LOW','MEDIUM','HIGH'),

    evaluation_date DATE,

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_score_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业风险评分表';
-- ============================================
-- Table: risk_warning
-- 风险预警
-- ============================================

CREATE TABLE risk_warning (

    warning_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    warning_type VARCHAR(100),

    warning_level ENUM('LOW','MEDIUM','HIGH'),

    warning_reason TEXT,

    status ENUM('OPEN','PROCESSING','CLOSED') DEFAULT 'OPEN',

    warning_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_warning_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业风险预警表';
-- ============================================
-- Table: smoke_index_result
-- 冒烟指数计算结果
-- ============================================

CREATE TABLE smoke_index_result (

    smoke_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    smoke_index DECIMAL(5,2),

    smoke_level ENUM('LOW','MEDIUM','HIGH'),

    calculation_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    calculation_version VARCHAR(20),

    CONSTRAINT fk_smoke_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业冒烟指数结果表';
-- ============================================
-- Table: risk_report
-- 企业风险分析报告
-- ============================================

CREATE TABLE risk_report (

    report_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    company_id BIGINT NOT NULL,

    report_no VARCHAR(50) UNIQUE,

    report_summary TEXT,

    report_file VARCHAR(500),

    report_date DATE,

    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_report_company
        FOREIGN KEY(company_id)
        REFERENCES company_basic(company_id)

) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COMMENT='企业风险分析报告';