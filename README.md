# EnterpriseRisk-Pro

> 基于多源公开数据的企业风险画像与预警分析项目。

项目面向金融风控、供应链金融和企业尽调场景，整合工商、财务、司法、行政处罚与舆情数据，输出可解释的企业风险评分、风险等级和风险摘要。

## 当前进度

- [x] MySQL 建库、建表与索引脚本
- [x] 演示样例数据生成与 CSV 数据链路
- [x] 企业级风险特征聚合
- [x] 规则版 Smoke Index 风险评分 MVP
- [x] 日志配置与自动化测试
- [x] FastAPI 查询与评分接口
- [x] Streamlit 风险画像看板
- [x] 单企业风险报告生成
- [x] Render 部署配置
- [ ] Render 线上部署验证

## 数据链路

```text
样例企业数据生成
-> data/sample/*.csv
-> 企业风险特征聚合
-> data/processed/enterprise_risk_features.csv
-> Smoke Index 规则评分
-> data/processed/enterprise_smoke_index.csv
```

## 快速运行

```powershell
.\.venv\Scripts\python.exe -m src.generator.generate_company_data
.\.venv\Scripts\python.exe -m src.analysis.risk_analysis
.\.venv\Scripts\python.exe -m src.scoring.smoke_index
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

启动 Dashboard：

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

默认地址：`http://localhost:8501`

单企业报告地址：`http://127.0.0.1:8000/reports/1`
```

项目优先读取 `data/sample/*.csv`，当样例 CSV 不存在时再尝试读取 MySQL，因此无需数据库也可以完成本地演示和测试。

## 项目结构

```text
config/                 配置文件
 data/sample/           样例源数据
 data/processed/        特征表与评分结果（本地生成，默认不提交）
docs/                   项目上下文与数据库设计
sql/                    建库、建表和索引脚本
src/analysis/           风险特征工程
src/database/           数据库连接与导入
src/generator/          样例数据生成
src/scoring/            风险评分逻辑
src/utils/              配置与日志工具
tests/                  自动化测试
```

## 技术栈

Python 3.12、Pandas、NumPy、SQLAlchemy、MySQL 8.0。后续计划接入 FastAPI、Streamlit 和 Plotly。

## 下一步

1. 搭建展示企业画像、评分、风险因素和 Top 风险企业的 Dashboard。
2. 增加单企业风险报告生成。
3. 完成 Render 线上部署验证和项目演示材料。

## 作者

Wendy Li
## FastAPI 服务

启动接口服务：

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --reload
```

接口文档地址：`http://127.0.0.1:8000/docs`

核心接口：

- `GET /health`：服务健康检查
- `GET /companies?limit=20`：企业列表，可使用 `keyword` 搜索
- `GET /companies/{company_id}`：企业详情及多源记录
- `GET /companies/{company_id}/risk`：企业 Smoke Index 风险评分
## Render 部署

项目包含 `render.yaml`，在 Render 中选择 New Blueprint，连接 GitHub 仓库后即可自动创建 Web Service。

部署完成后访问：

```text
https://你的服务名.onrender.com/docs
```

服务启动命令：

```text
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```
## 导入 MySQL

确认本地 MySQL 已启动并完成建库建表后，运行：

```powershell
.\.venv\Scripts\python.exe -m src.database.import_demo_data
.\.venv\Scripts\python.exe -m src.database.persist_risk_results
```

当前演示数据库已导入 500 家企业、1500 条财务记录、399 条司法记录、281 条处罚记录和 1250 条舆情记录。可执行 `sql/05_verify_demo_data.sql` 验证数据量。

评分结果持久化命令会将最新评分写入 `risk_score` 和 `smoke_index_result` 表。
