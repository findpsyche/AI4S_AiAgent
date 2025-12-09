# 🚀 本地验证 - 开始指南

欢迎！本指南帮助你快速验证学术论文分析系统是否能在本地正常工作。

---

## ⏱️ 需要多少时间？

- **快速验证** - 5分钟
- **完整验证** - 15分钟
- **深度测试** - 30分钟

选择你的验证方式：

---

## 🏃 5分钟快速验证

### 步骤1：准备API Key
```bash
# 从 https://platform.openai.com/api-keys 获取API Key
# 复制你的Key（以 sk- 开头）
```

### 步骤2：配置文件
```bash
cp .env.example .env
# 用编辑器打开 .env，替换：
# OPENAI_API_KEY=sk-your-api-key-here
```

### 步骤3：启动应用
```bash
# Windows:
scripts\run_local.bat

# Mac/Linux:
bash scripts/run_local.sh
```

### 步骤4：打开浏览器
访问 http://localhost:8000/docs

✅ **完成！** 你已经成功启动了应用

---

## 🧪 15分钟完整验证

### 在Swagger UI中测试（推荐）

1. **打开** http://localhost:8000/docs
2. **找到** `POST /api/v1/analyze` 端点
3. **点击** "Try it out"
4. **选择** 一个PDF文件上传（或用示例）
5. **执行** 并等待结果
6. **查看** 分析结果中的数据

### 使用curl命令测试

```bash
# 上传PDF
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@your_paper.pdf"

# 记录返回的 task_id

# 查询进度（重复执行直到status为completed）
curl "http://localhost:8000/api/v1/status/your_task_id"
```

### 关键验证点

- ✅ 应用启动成功（无错误）
- ✅ API文档可以打开
- ✅ 能上传PDF获得task_id
- ✅ 能查询任务状态
- ✅ 能获取分析结果

---

## 📖 详细文档

### 新手入门
1. **[本地验证快速参考](./LOCAL_VALIDATION_QUICKREF.md)**
   - 30秒快速开始
   - 常用命令速查
   - 常见错误快速修复

2. **[README.md](./README.md)**
   - 完整的本地验证指南
   - 所有API端点说明
   - 故障排查指南

### 深度测试
3. **[本地验证检查清单](./LOCAL_VALIDATION_CHECKLIST.md)**
   - 逐步验证指南
   - 多种验证方法
   - 详细的故障排除

4. **[项目总结](./PROJECT_SUMMARY.md)**
   - 项目架构和技术栈
   - 性能基准
   - 功能列表

---

## 🐛 遇到问题？

### 常见错误快速修复

| 错误 | 修复方式 |
|------|----------|
| `OPENAI_API_KEY is required` | 编辑.env填入API Key |
| `ModuleNotFoundError` | 运行 `pip install -r requirements.txt` |
| `Port 8000 already in use` | 编辑.env改为 `PORT=8001` |
| `401 Unauthorized` | 检查API Key是否正确有效 |

### 需要帮助？

1. **查看完整文档** → [README.md](./README.md)
2. **查看故障排查** → [LOCAL_VALIDATION_CHECKLIST.md](./LOCAL_VALIDATION_CHECKLIST.md)
3. **查看快速参考** → [LOCAL_VALIDATION_QUICKREF.md](./LOCAL_VALIDATION_QUICKREF.md)
4. **使用API文档** → http://localhost:8000/docs (Swagger UI)

---

## 📚 文档导航

```
开始验证
    ↓
【快速参考】LOCAL_VALIDATION_QUICKREF.md (5分钟)
    ↓
【完整指南】README.md (15分钟)
    ↓
【详细清单】LOCAL_VALIDATION_CHECKLIST.md (30分钟)
    ↓
【API文档】http://localhost:8000/docs
    ↓
【项目信息】PROJECT_SUMMARY.md
```

---

## ✅ 验证完成标志

看到以下现象说明验证成功：

- ✅ 应用启动显示 "Application startup complete"
- ✅ http://localhost:8000/docs 能打开
- ✅ 能成功上传PDF文件
- ✅ 能查询任务进度
- ✅ 能获取分析结果

---

## 🎯 后续步骤

**验证成功后，你可以：**

1. **测试更多论文** - 用不同的PDF文件测试
2. **优化配置** - 调整参数如OPENAI_TEMPERATURE
3. **学习代码** - 查看 `app/` 目录的源代码
4. **扩展功能** - 修改Agent或添加新功能
5. **性能优化** - 启用Redis缓存、调整参数

---

## 💡 快速提示

### 如何关闭应用？
- 按 `Ctrl+C` 停止服务

### 如何重新启动？
- 重新运行启动脚本

### 如何查看日志？
- 日志会显示在启动应用的命令行窗口

### 如何测试不同的模型？
- 编辑 `.env` 改变 `OPENAI_MODEL`
- 支持的模型：`gpt-4`, `gpt-4-turbo-preview`, `gpt-3.5-turbo`

### 如何改变端口？
- 编辑 `.env` 改为 `PORT=8001` (或其他端口)
- 重启应用后访问 http://localhost:8001/docs

---

## 🎉 准备好了吗？

### 方式1：快速开始（推荐）
```bash
cp .env.example .env
# 编辑 .env 填入API Key
scripts\run_local.bat  # 或 bash scripts/run_local.sh
# 打开 http://localhost:8000/docs
```

### 方式2：按步骤验证
按照 [LOCAL_VALIDATION_CHECKLIST.md](./LOCAL_VALIDATION_CHECKLIST.md) 逐步执行

### 方式3：查看快速参考
使用 [LOCAL_VALIDATION_QUICKREF.md](./LOCAL_VALIDATION_QUICKREF.md) 查询命令

---

## 📞 需要帮助？

| 问题类型 | 查看文档 |
|----------|----------|
| 不知道怎么开始 | 本文档（你正在看） |
| 需要快速参考 | LOCAL_VALIDATION_QUICKREF.md |
| 逐步验证指南 | LOCAL_VALIDATION_CHECKLIST.md |
| 完整文档 | README.md |
| API端点文档 | http://localhost:8000/docs |
| 项目信息 | PROJECT_SUMMARY.md |

---

**祝你验证顺利！有任何问题都可以查看相关文档。** 🚀

---

**更新时间：2024年12月**
