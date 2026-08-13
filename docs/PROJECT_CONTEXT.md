# EnterpriseRisk-Pro 项目上下文记录

最后更新日期：2026-08-03

## 项目定位

EnterpriseRisk-Pro 面向金融风控场景构建企业风险画像与预警能力。项目通过工商、财务、司法、行政处罚和舆情等多源数据，形成企业级风险特征，输出可解释的风险评分、风险等级和风险摘要。

## 仓库路径

`D:\github\EnterpriseRisk-Pro`

## 已完成内容

- 项目目录结构与 Git 仓库初始化
- MySQL 建库、建表和索引脚本
- `src/database/db_connect.py` 数据库连接模块
- `src/generator/generate_company_data.py` 演示数据生成模块
- `src/analysis/risk_analysis.py` 企业风险特征聚合模块
- `src/scoring/smoke_index.py` 规则版风险评分模块
- `src/utils/logger.py` 统一日志配置
- `tests/test_pipeline.py` 数据链路自动化测试
- `src/api/` FastAPI 查询、详情和风险评分接口
- `src/database/persist_risk_results.py` 风险结果持久化
- `render.yaml` Render 部署配置

## 当前数据闭环

```text
src/generator/generate_company_data.py
-> data/sample/*.csv
-> src/analysis/risk_analysis.py
-> data/processed/enterprise_risk_features.csv
-> src/scoring/smoke_index.py
-> data/processed/enterprise_smoke_index.csv
```

最近一次完整运行包含 500 家企业、1500 条财务记录、399 条司法记录、281 条处罚记录和 1250 条舆情记录，最终生成 100 条企业特征和 100 条评分结果。

## 评分指标

- 财务风险：资产负债率、亏损状态、营收资产比和经营状态
- 司法风险：案件数量、中高风险案件和近 12 个月案件
- 行政处罚风险：处罚数量、处罚金额和近 12 个月处罚
- 舆情风险：负面舆情占比、负面数量和近 90 天舆情

综合权重为财务 35%、司法 25%、行政处罚 20%、舆情 20%。风险等级为 A 低风险、B 一般风险、C 关注风险、D 高风险、E 严重风险。

## 下一步建议

当前优先开发 Streamlit Dashboard 和单企业风险报告；之后完成 Render 线上部署验证。

## 已知事项

- `data/processed/` 是本地流水线产物，按 `.gitignore` 规则默认不提交。
- 数据库连接配置仍需通过环境变量读取，避免明文配置进入仓库。
- 当前评分为规则版 MVP，适合演示和解释，后续可基于特征表训练机器学习模型。
