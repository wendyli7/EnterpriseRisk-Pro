/*
====================================================
Project : EnterpriseRisk-Pro
Module  : Database Initialization
Author  : Wendy Li
Version : V1.0
Date    : 2026-07-10
====================================================
*/

-- ==========================
-- Create Database
-- ==========================

DROP DATABASE IF EXISTS enterprise_risk_db;

CREATE DATABASE enterprise_risk_db
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE enterprise_risk_db;

-- ==========================
-- Database Information
-- ==========================

SELECT DATABASE() AS CurrentDatabase;