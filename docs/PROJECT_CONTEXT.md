# EnterpriseRisk-Pro 项目上下文记录

最后更新日期：2026-08-03

## 项目定位

EnterpriseRisk-Pro 是一个面向金融风控场景的企业风险画像与预警项目。项目通过企业工商、财务、司法、行政处罚、舆情等多源公开数据，构建企业风险特征，输出可解释的风险评分、风险等级和风险摘要。

主要展示能力：

- Python 数据工程
- SQL / MySQL 数据建模
- 企业风险指标体系设计
- 规则评分与后续机器学习建模
- Dashboard 与接口化交付能力

## 当前仓库路径

`D:\github\EnterpriseRisk-Pro`

## 已完成内容

- 项目目录结构初始化
- MySQL 建库、建表、索引脚本
- 数据库连接模块：`src/database/db_connect.py`
- 演示数据生成模块：`src/generator/generate_company_data.py`
- 演示数据导入模块：`src/database/import_demo_data.py`
- 企业风险特征聚合模块：`src/analysis/risk_analysis.py`
- 规则版风险评分模块：`src/scoring/smoke_index.py`
- README 当前进度更新

## 当前数据闭环

```text
src/generator/generate_company_data.py
-> data/sample/*.csv
-> src/analysis/risk_analysis.py
-> data/processed/enterprise_risk_features.csv
-> src/scoring/smoke_index.py
-> data/processed/enterprise_smoke_index.csv
```

## 当前样例数据规模

最近一次运行结果：

- `company_basic`: 100 行
- `company_financial`: 300 行
- `company_lawsuit`: 86 行
- `company_penalty`: 43 行
- `company_opinion`: 261 行
- `enterprise_risk_features`: 100 行
- `enterprise_smoke_index`: 100 行

## 核心表设计

当前 SQL 已落地以下核心表：

- `company_basic`
- `company_financial`
- `company_lawsuit`
- `company_penalty`
- `company_opinion`
- `risk_tag`
- `risk_score`
- `risk_warning`
- `smoke_index_result`
- `risk_report`

后续开发应以当前 SQL 表结构为准，不再使用早期简化表结构。

## 风险指标体系

当前规则版评分使用四类子分：

- `financial_score`：资产负债率、亏损状态、营收资产比、经营状态
- `lawsuit_score`：诉讼数量、中高风险案件、近 12 个月案件
- `penalty_score`：处罚数量、处罚金额、近 12 个月处罚
- `opinion_score`：负面舆情占比、负面舆情数量、近 90 天舆情

综合分权重：

- 财务风险：35%
- 司法风险：25%
- 行政处罚风险：20%
- 舆情风险：20%

风险等级：

- A-低风险：0-19.99
- B-一般风险：20-39.99
- C-关注风险：40-59.99
- D-高风险：60-79.99
- E-严重风险：80-100

## 运行方式

```powershell
.\.venv\Scripts\python.exe -m src.generator.generate_company_data
.\.venv\Scripts\python.exe -m src.analysis.risk_analysis
.\.venv\Scripts\python.exe -m src.scoring.smoke_index
```

说明：

- 特征聚合模块优先读取 `data/sample/*.csv`。
- 如果样例 CSV 不存在，模块会尝试读取 MySQL 表。
- 这让项目可以在没有本机数据库连接的情况下完成演示链路验证。

## 当前仍需补齐

优先级建议：

1. `src/utils/logger.py`：统一日志输出
2. `tests/`：增加样例生成、特征聚合、评分逻辑测试
3. 数据库存储：将评分结果写入 `risk_score` 或 `smoke_index_result`
4. FastAPI：实现企业查询和风险评分查询接口
5. Streamlit Dashboard：展示企业画像、评分、风险因素和 Top 风险企业
6. 报告生成：输出单企业风险分析报告

## 已识别问题

- 部分旧文档和 SQL 注释仍可能存在中文乱码，需要逐步统一为 UTF-8。
- `config/config.yaml` 中存在明文数据库配置，后续应改为环境变量读取。
- `sql/03_insert_demo_data.sql` 仍为空；当前演示数据通过 CSV 生成与 Python 导入脚本处理。
- 当前评分为规则版 MVP，适合演示和解释；后续机器学习模型可基于特征表继续训练。

## 下一步推荐

下一步建议补齐测试和日志模块，再进入接口层。这样项目会从“能跑通”升级到“更像正式工程项目”，也更适合简历和面试展示。
