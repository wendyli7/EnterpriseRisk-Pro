# EnterpriseRisk-Pro

> 基于多源公开数据的企业风险画像与预警分析项目

EnterpriseRisk-Pro 面向金融风控、供应链金融、企业尽调等场景，使用企业工商、财务、司法、行政处罚、舆情等公开数据构建企业风险画像，并输出可解释的风险评分与风险等级。

## 项目目标

- 构建企业多源风险数据集
- 形成企业级风险特征表
- 设计可解释的规则版风险评分模型
- 输出企业风险等级、风险摘要和预警信号
- 后续扩展 FastAPI 接口与 Streamlit Dashboard

## 当前进度

- [x] 项目目录与 Git 仓库初始化
- [x] MySQL 建库、建表与索引脚本
- [x] 数据库连接模块
- [x] 演示样例数据生成器
- [x] 样例 CSV 数据集
- [x] 企业风险特征聚合模块
- [x] 规则版风险评分 MVP
- [ ] FastAPI 查询与预测接口
- [ ] Streamlit 风险画像看板
- [ ] 自动化测试与报告生成
- [ ] 部署与项目展示优化

## 核心数据链路

```text
样例企业数据生成
-> 多表风险数据 CSV
-> 企业级风险特征聚合
-> 规则版 Smoke Index 风险评分
-> 风险等级与风险摘要输出
```

## 项目结构

```text
EnterpriseRisk-Pro/
├── config/                 # 配置文件
├── data/
│   ├── sample/             # 样例源数据 CSV
│   └── processed/          # 特征表与评分结果
├── docs/                   # PRD、数据库设计、项目上下文
├── sql/                    # 建库、建表、索引脚本
├── src/
│   ├── analysis/           # 风险特征工程
│   ├── database/           # 数据库连接与数据导入
│   ├── generator/          # 样例数据生成
│   ├── scoring/            # 风险评分逻辑
│   └── utils/              # 工具模块
├── dashboard/              # 后续 Streamlit 看板
├── models/                 # 后续模型文件
├── reports/                # 后续报告输出
└── tests/                  # 后续测试用例
```

## 快速运行

使用项目虚拟环境运行：

```powershell
.\.venv\Scripts\python.exe -m src.generator.generate_company_data
.\.venv\Scripts\python.exe -m src.analysis.risk_analysis
.\.venv\Scripts\python.exe -m src.scoring.smoke_index
```

运行后会生成：

- `data/sample/company_basic.csv`
- `data/sample/company_financial.csv`
- `data/sample/company_lawsuit.csv`
- `data/sample/company_penalty.csv`
- `data/sample/company_opinion.csv`
- `data/processed/enterprise_risk_features.csv`
- `data/processed/enterprise_smoke_index.csv`

## 技术栈

- Python 3.12
- Pandas / NumPy
- SQLAlchemy / PyMySQL
- MySQL 8.0
- Scikit-learn / XGBoost / SHAP（后续模型阶段）
- Streamlit / Plotly（后续看板阶段）

## 下一步计划

1. 补齐 `src/utils/logger.py` 和基础测试用例
2. 将规则评分结果写入 `risk_score` 或 `smoke_index_result` 表
3. 增加 FastAPI 接口：企业查询、风险评分查询、风险预测
4. 搭建 Streamlit Dashboard MVP
5. 增加项目展示截图与案例报告

## 作者

Wendy Li

金融风险分析方向项目，用于展示 Python、SQL、数据分析与企业风控建模能力。
