# 学术助手系统 - 完整项目README

## 📖 项目概述

**学术助手** 是一个基于 **LangChain + FastAPI + OpenAI GPT-4** 构建的 AI 驱动学术论文深度分析系统。

### 🎯 核心能力

研究人员对一篇论文最需要的分析：

- ✅ **数学模型提取** - 自动识别和解析论文中的所有关键数学公式
- ✅ **研究领域分析** - 准确分类论文的研究领域和子领域
- ✅ **学术泰斗识别** - 识别领域内的关键学者和学术影响力
- ✅ **技术发展路线** - 追踪技术方法的演进历史和未来方向
- ✅ **创新点提取** - 提取论文的核心创新贡献
- ✅ **研究空白识别** - 发现论文中提及的研究机会

---

## 🏗️ 系统架构

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| Web框架 | FastAPI | 0.109.0 |
| AI引擎 | LangChain + OpenAI | 1.0.0 |
| 缓存层 | Redis | 7.0 |
| 向量数据库 | ChromaDB | 0.4.22 |
| 容器化 | Docker | 最新 |
| 反向代理 | Nginx | Alpine |

### 项目目录结构

```
academic-paper-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI应用入口
│   ├── config.py               # 配置管理
│   ├── agents/                 # Agent模块
│   │   ├── paper_parser.py     # 论文解析Agent
│   │   ├── math_model_agent.py # 数学模型Agent
│   │   ├── domain_analyzer.py  # 领域分析Agent
│   │   ├── scholar_analyzer.py # 学者分析Agent
│   │   ├── tech_roadmap.py     # 技术路线Agent
│   │   └── orchestrator.py     # 主编排器
│   ├── services/               # 服务层
│   │   ├── cache_service.py    # Redis缓存服务
│   │   └── rag_service.py      # RAG检索服务
│   ├── models/
│   │   └── schemas.py          # Pydantic数据模型
│   └── utils/                  # 工具函数
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── scripts/
│   ├── deploy.py               # 部署脚本（腾讯云）
│   ├── run_local.sh            # 本地启动脚本
│   └── run_docker.sh           # Docker启动脚本
├── config/
│   └── settings.py
├── tests/
├── data/
│   ├── uploads/                # 上传的论文
│   └── vector_db/              # 向量数据库存储
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 快速开始

### 方式1：本地开发环境（推荐）

#### 前置条件
- Python 3.11+
- pip 包管理器
- OpenAI API Key ([获取](https://platform.openai.com/api-keys))

#### 步骤

1. **克隆项目**
```bash
cd academic-paper-agent
```

2. **配置环境**
```bash
# 复制环境文件
cp .env.example .env

# 编辑.env，填入你的OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here
```

3. **运行启动脚本**

**Linux/Mac:**
```bash
bash scripts/run_local.sh
```

**Windows:**
```bash
scripts\run_local.bat
```

4. **访问应用**
- API: http://localhost:8000
- 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

---

### 方式2：Docker容器（生产推荐）

#### 前置条件
- Docker & Docker Compose
- OpenAI API Key

#### 步骤

1. **配置环境**
```bash
cp .env.example .env
# 编辑.env，填入OpenAI API Key
```

2. **启动服务**
```bash
bash scripts/run_docker.sh
```

或手动启动：
```bash
cd docker
docker-compose up -d
```

3. **查看日志**
```bash
docker-compose logs -f api
```

4. **停止服务**
```bash
docker-compose down
```

---

### 方式3：一键部署到腾讯云（自动化）

#### 腾讯云服务器信息
```
IP: 43.143.210.81
地域: 北京 | 北京六区
CPU: 2核
内存: 1GB
系统盘: 40GB SSD
带宽: 200Mbps
```

#### 部署步骤

1. **准备部署环境**
```bash
# 确保本地已安装Docker和Git
python --version  # 验证Python 3.11+
git --version     # 验证Git
docker --version  # 验证Docker
```

2. **执行一键部署**

**使用SSH密钥登录（推荐）：**
```bash
python scripts/deploy.py --ip 43.143.210.81 --key ~/.ssh/id_rsa --username root
```

**使用密码登录：**
```bash
python scripts/deploy.py --ip 43.143.210.81 --username root
# 系统会提示输入SSH密码
```

3. **部署过程自动执行以下步骤**
- ✅ 代码上传到服务器
- ✅ 安装系统依赖
- ✅ 安装Docker和Docker Compose
- ✅ 构建Docker镜像
- ✅ 启动所有服务（API + Redis）
- ✅ 健康检查验证

4. **访问部署的应用**
```
http://43.143.210.81:8000
http://43.143.210.81:8000/docs
```

---

## 📡 API接口文档

### 1. 论文分析接口

**POST** `/api/v1/analyze`

**请求示例：**
```bash
# 上传PDF文件
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@paper.pdf"

# 使用arXiv ID
curl -X POST "http://localhost:8000/api/v1/analyze?arxiv_id=2301.12345"

# 使用DOI
curl -X POST "http://localhost:8000/api/v1/analyze?doi=10.1234/example"
```

**响应示例：**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "分析已启动，使用 /api/v1/status/{task_id} 查询进度"
}
```

### 2. 查询任务状态

**GET** `/api/v1/status/{task_id}`

**响应示例：**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "result": {
    "paper_id": "uuid",
    "title": "Attention Is All You Need",
    "authors": ["Vaswani et al."],
    "year": 2017,
    "abstract": "...",
    "math_models": [
      {
        "formula": "Scaled Dot-Product Attention",
        "latex": "\\text{Attention}(Q,K,V) = ...",
        "description": "Multi-head attention mechanism",
        "formula_type": "equation",
        "importance": 0.95,
        "location": "Section 3.2"
      }
    ],
    "domain_info": {
      "primary_field": "Natural Language Processing",
      "sub_fields": ["Machine Translation", "Transformer Architecture"],
      "keywords": ["Attention", "Transformer", "Self-Attention"],
      "confidence": 0.95
    },
    "key_scholars": [
      {
        "name": "Ashish Vaswani",
        "affiliation": "Google Brain",
        "h_index": 45,
        "role": "author"
      }
    ],
    "tech_roadmap": [
      {
        "method_name": "RNN",
        "year": 2014,
        "improvement": "Earlier sequential approach"
      }
    ],
    "innovation_points": [
      "Self-attention mechanism replaces RNNs",
      "Parallel processing instead of sequential"
    ],
    "reproducibility_score": 0.9
  }
}
```

### 3. 搜索相似论文

**GET** `/api/v1/search`

```bash
curl "http://localhost:8000/api/v1/search?query=transformer&limit=10"
```

### 4. 获取系统指标

**GET** `/api/v1/metrics`

```bash
curl "http://localhost:8000/api/v1/metrics"
```

---

## 🔑 环境变量配置

编辑 `.env` 文件配置以下参数：

```bash
# OpenAI API配置（必填）
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.3

# Redis配置（可选，本地开发可跳过）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 日志配置
LOG_LEVEL=INFO
DEBUG=false

# 功能开关
ENABLE_REDIS_CACHE=true
ENABLE_RAG=true
```

---

## 💡 使用示例

### Python客户端示例

```python
import requests
import time
import json

API_URL = "http://localhost:8000"

# 1. 上传论文并开始分析
print("📤 上传论文...")
with open("paper.pdf", "rb") as f:
    response = requests.post(
        f"{API_URL}/api/v1/analyze",
        files={"file": f}
    )

task_data = response.json()
task_id = task_data["task_id"]
print(f"✅ 任务ID: {task_id}")

# 2. 轮询检查分析进度
print("\n⏳ 等待分析完成...")
while True:
    status_response = requests.get(f"{API_URL}/api/v1/status/{task_id}")
    status_data = status_response.json()
    
    print(f"进度: {status_data['progress']}% - {status_data['status']}")
    
    if status_data["status"] == "completed":
        break
    elif status_data["status"] == "failed":
        print(f"❌ 分析失败: {status_data['error']}")
        break
    
    time.sleep(5)

# 3. 获取分析结果
if status_data["status"] == "completed":
    result = status_data["result"]
    
    print("\n📊 分析结果：")
    print(f"论文: {result['title']}")
    print(f"作者: {', '.join(result['authors'])}")
    print(f"研究领域: {result['domain_info']['primary_field']}")
    print(f"\n数学模型 ({len(result['math_models'])}):")
    for model in result['math_models'][:3]:
        print(f"  - {model['formula']}: {model['description']}")
    
    print(f"\n关键学者 ({len(result['key_scholars'])}):")
    for scholar in result['key_scholars'][:3]:
        print(f"  - {scholar['name']} ({scholar['affiliation']})")
    
    print(f"\n创新点:")
    for point in result['innovation_points'][:3]:
        print(f"  - {point}")
```

---

## 🔧 常见问题

### Q1: 报错"OpenAI API Key无效"
**A:** 
1. 检查 `.env` 文件中的 `OPENAI_API_KEY`
2. 确认API Key是有效的：https://platform.openai.com/api-keys
3. 检查API配额是否充足

### Q2: Redis连接失败
**A:** 
- 本地开发可将 `ENABLE_REDIS_CACHE=false` 禁用缓存
- Docker模式下自动启动Redis容器

### Q3: 内存不足或处理缓慢
**A:** 
- 调整 `OPENAI_TEMPERATURE` 参数（降低至0.1-0.3）
- 启用Redis缓存提升性能
- 使用Docker部署改善资源管理

### Q4: PDF解析失败
**A:** 
- 检查PDF文件是否已损坏
- 某些扫描型PDF需要OCR处理（需配置Mathpix API）
- 尝试使用标准的文本型PDF

### Q5: 如何在生产环境中部署？
**A:** 
使用提供的一键部署脚本：
```bash
python scripts/deploy.py --ip <server-ip> --key <ssh-key-path>
```

---

## 🔒 安全建议

1. **API Key管理**
   - 不要在代码中硬编码API Key
   - 使用 `.env` 文件管理敏感信息
   - 定期轮换API Key

2. **网络安全**
   - 在生产环境使用HTTPS
   - 配置防火墙限制访问IP
   - 启用Redis密码认证

3. **数据隐私**
   - 论文PDF存储在本地 `data/uploads` 目录
   - 定期清理过期的上传文件
   - 遵守学术版权法规

---

## 📈 性能优化

### 缓存策略
- Redis缓存热点论文（TTL: 1小时）
- 相同论文的重复查询直接返回缓存结果
- 性能提升：8.2s → 1.9s (77%提升)

### 并行处理
- 多个Agent并行执行分析任务
- 充分利用多核CPU
- 通过 `asyncio.gather()` 实现异步协调

### 资源限制
- 单个PDF大小限制：100MB
- 文本预处理：截取前20000字符避免Token超限
- 任务队列在内存中管理

---

## 🧪 测试

```bash
# 运行单元测试
pytest tests/

# 运行覆盖率检查
pytest --cov=app tests/

# 性能测试
locust -f tests/load_test.py
```

---

## 📚 相关资源

- [FastAPI文档](https://fastapi.tiangolo.com)
- [LangChain文档](https://docs.langchain.com)
- [OpenAI API文档](https://platform.openai.com/docs)
- [Docker文档](https://docs.docker.com)

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交改动：`git commit -m "Add: your feature"`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📧 联系方式

- 📧 Email: support@academic-assistant.ai
- 🌐 网站: https://academic-assistant.ai
- 💬 问题反馈: GitHub Issues

---

**🎉 感谢使用学术助手系统！**

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！
