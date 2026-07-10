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