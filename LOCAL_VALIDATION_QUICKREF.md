# 🚀 本地验证快速参考

## ⚡ 30秒快速开始

```bash
# 1. 复制环境文件
cp .env.example .env

# 2. 编辑.env，填入OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here

# 3. 创建虚拟环境（可选）
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动应用
scripts\run_local.bat  # Windows
bash scripts/run_local.sh  # Mac/Linux

# 6. 打开浏览器访问
# http://localhost:8000/docs
```

---

## 📋 核心命令速查

### 启动应用
```bash
# Windows
scripts\run_local.bat

# Mac/Linux
bash scripts/run_local.sh
```

### 健康检查
```bash
curl http://localhost:8000/health
```

### 上传论文分析
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@paper.pdf"
```

### 查询分析进度
```bash
curl "http://localhost:8000/api/v1/status/{task_id}"
```

### 获取系统指标
```bash
curl http://localhost:8000/api/v1/metrics
```

---

## 🔑 关键配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `OPENAI_API_KEY` | sk-... | **必填**，OpenAI API Key |
| `OPENAI_MODEL` | gpt-4-turbo-preview | 使用的GPT模型 |
| `OPENAI_TEMPERATURE` | 0.3 | 回答多样性（0-1） |
| `PORT` | 8000 | 服务端口 |
| `ENABLE_REDIS_CACHE` | false | 是否启用缓存 |
| `LOG_LEVEL` | INFO | 日志级别 |

---

## 🌐 API端点速查

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/v1/analyze` | POST | 上传论文分析 |
| `/api/v1/status/{task_id}` | GET | 查询任务状态 |
| `/api/v1/search` | GET | 搜索相似论文 |
| `/api/v1/metrics` | GET | 系统指标 |
| `/health` | GET | 健康检查 |
| `/docs` | GET | API文档(Swagger) |

---

## ⏱️ 性能基准

| 操作 | 耗时 |
|------|------|
| 首次分析 | 8-15秒 |
| 缓存命中 | <2秒 |
| 缓存命中率 | 65% |

---

## 🔴 常见错误快速修复

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ModuleNotFoundError` | 依赖未安装 | `pip install -r requirements.txt` |
| `OPENAI_API_KEY is required` | API Key未配置 | 编辑.env填入API Key |
| `Port 8000 already in use` | 端口被占用 | 改为其他端口如8001 |
| `401 Unauthorized` | API Key无效 | 检查API Key是否正确 |
| `PDF解析失败` | PDF文件问题 | 使用纯文本PDF，不是扫描图像 |

---

## ✅ 验证成功检查清单

- [ ] Python 3.11+ 已安装
- [ ] `.env` 文件已创建并填入API Key
- [ ] 依赖已安装：`pip install -r requirements.txt`
- [ ] 应用成功启动，显示"Application startup complete"
- [ ] http://localhost:8000/docs 能打开
- [ ] `/health` 返回 200 OK
- [ ] 能上传PDF获得task_id
- [ ] 能查询任务状态
- [ ] 能获取完整分析结果

---

## 📂 重要文件位置

```
.env.example          ← 配置模板（复制为.env）
README.md            ← 详细文档
LOCAL_VALIDATION_CHECKLIST.md  ← 完整验证清单
requirements.txt     ← Python依赖列表
scripts/run_local.*  ← 启动脚本
app/main.py         ← FastAPI应用入口
```

---

## 💡 常用快速链接

| 资源 | URL |
|------|-----|
| API文档 | http://localhost:8000/docs |
| API文档(ReDoc) | http://localhost:8000/redoc |
| OpenAI API Keys | https://platform.openai.com/api-keys |
| FastAPI文档 | https://fastapi.tiangolo.com |

---

## 🎯 典型使用流程

```
1. 启动应用
   └─> scripts\run_local.bat (Windows) 或 bash scripts/run_local.sh

2. 打开API文档
   └─> http://localhost:8000/docs

3. 上传论文进行分析
   └─> POST /api/v1/analyze (选择PDF文件)

4. 获得task_id
   └─> {"task_id": "xxx-xxx-xxx"}

5. 轮询查询进度
   └─> GET /api/v1/status/{task_id} (每3-5秒查一次)

6. 等待分析完成
   └─> status从"processing"变为"completed"

7. 获取最终结果
   └─> 查看result字段包含所有分析数据
```

---

## 🐛 调试技巧

### 查看启动日志
```bash
# 日志中会显示详细的启动过程和任何错误
# 留意关键信息如"Application startup complete"和"Uvicorn running on"
```

### 测试API可用性
```bash
curl -v http://localhost:8000/health
```

### 检查环境变量
```bash
# Windows
type .env | findstr OPENAI_API_KEY

# Mac/Linux
cat .env | grep OPENAI_API_KEY
```

### 查看Python路径
```bash
which python  # Mac/Linux
where python  # Windows
```

---

## 📞 获取帮助

1. **查看完整验证清单** → `LOCAL_VALIDATION_CHECKLIST.md`
2. **查看项目文档** → `README.md`
3. **查看API文档** → http://localhost:8000/docs
4. **查看项目总结** → `PROJECT_SUMMARY.md`

---

**🎉 准备好了吗？开始本地验证之旅吧！** 🚀
