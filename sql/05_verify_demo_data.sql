/* Verify the current demo data volume after CSV import. */
USE enterprise_risk_db;

SELECT 'company_basic' AS table_name, COUNT(*) AS row_count FROM company_basic
UNION ALL SELECT 'company_financial', COUNT(*) FROM company_financial
UNION ALL SELECT 'company_lawsuit', COUNT(*) FROM company_lawsuit
UNION ALL SELECT 'company_penalty', COUNT(*) FROM company_penalty
UNION ALL SELECT 'company_opinion', COUNT(*) FROM company_opinion;

SELECT COUNT(DISTINCT company_name) AS unique_company_names FROM company_basic;