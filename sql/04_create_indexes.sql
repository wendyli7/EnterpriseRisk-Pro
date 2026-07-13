USE enterprise_risk_db;

CREATE INDEX idx_company_name
ON company_basic(company_name);

CREATE INDEX idx_unified_code
ON company_basic(unified_code);

CREATE INDEX idx_company_financial
ON company_financial(company_id);

CREATE INDEX idx_company_lawsuit
ON company_lawsuit(company_id);

CREATE INDEX idx_company_penalty
ON company_penalty(company_id);