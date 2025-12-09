# 学术助手系统 - 部署检查清单

## 📋 部署前检查

### 本地环境检查
- [ ] Python 3.11+ 已安装
- [ ] pip 已安装
- [ ] Git 已安装  
- [ ] 获取了OpenAI API Key (https://platform.openai.com/api-keys)
- [ ] 复制了 .env.example 为 .env
- [ ] 编辑了 .env，填入 OPENAI_API_KEY

### Docker相关（用于Docker部署）
- [ ] Docker 已安装 (https://www.docker.com/products/docker-desktop)
- [ ] Docker Compose 已安装
- [ ] Docker daemon 正在运行
- [ ] 用户有Docker权限 (不需要sudo)

### 腾讯云服务器信息（用于云部署）
- [ ] 获取了服务器IP地址: 43.143.210.81
- [ ] 准备了SSH密钥或密码
- [ ] SSH端口22已开放（防火墙配置）
- [ ] 确认服务器已运行且可SSH访问

### 网络和防火墙
- [ ] 端口8000已开放（HTTP API）
- [ ] 端口6379已开放（Redis，仅内部通信）
- [ ] 端口80已开放（Nginx反向代理）

---

## 🚀 部署步骤（选择一种）

### 方式1: 本地开发环境（推荐用于开发）

```bash
# 1. 进入项目目录
cd academic-paper-agent

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 编辑.env文件配置
# OPENAI_API_KEY=sk-your-key-here

# 6. 运行应用
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. 访问
# http://localhost:8000
# http://localhost:8000/docs (API文档)
```

### 方式2: Docker本地运行（推荐用于生产仿真）

```bash
# 1. 进入docker目录
cd docker

# 2. 编辑.env文件
# OPENAI_API_KEY=sk-your-key-here

# 3. 启动所有服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f api

# 5. 访问
# http://localhost:8000

# 6. 停止服务
docker-compose down
```

### 方式3: 部署到腾讯云（一键自动化）

```bash
# 使用SSH密钥（推荐）
bash scripts/deploy_tencent_cloud.sh 43.143.210.81 ~/.ssh/id_rsa root

# 或使用密码登录（会提示输入密码）
bash scripts/deploy_tencent_cloud.sh 43.143.210.81
```

**部署流程自动执行：**
1. ✅ 系统检查
2. ✅ SSH连接测试
3. ✅ 项目文件上传
4. ✅ 系统依赖安装
5. ✅ Docker安装
6. ✅ 环境配置
7. ✅ 服务启动
8. ✅ 健康检查

**部署完成后：**
- 访问: http://43.143.210.81:8000
- 文档: http://43.143.210.81:8000/docs

---

## ✅ 部署验证

### 1. 健康检查
```bash
curl http://localhost:8000/health
# 或
curl http://43.143.210.81:8000/health (云部署)
```

**预期响应：**
```json
{"status": "healthy"}
```

### 2. 查看系统信息
```bash
curl http://localhost:8000/
```

### 3. 查看API文档
浏览器访问: http://localhost:8000/docs

### 4. 测试上传论文
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "file=@paper.pdf"
```

### 5. 查看容器日志（Docker部署）
```bash
docker-compose logs -f api
```

---

## 🔧 常见部署问题

### 问题1: OpenAI API错误
**症状：** 返回 "OpenAI API error"
**解决：**
1. 检查.env中的OPENAI_API_KEY是否正确
2. 访问 https://platform.openai.com/api-keys 验证Key有效性
3. 检查API配额是否充足

### 问题2: Redis连接失败
**症状：** 返回 "Redis connection error"
**解决：**
- 本地开发：设置 ENABLE_REDIS_CACHE=false
- Docker部署：redis容器应自动启动，检查 docker-compose logs redis
- 云部署：检查安全组是否允许6379端口

### 问题3: 端口已被占用
**症状：** "Address already in use"
**解决：**
- 本地开发：
  ```bash
  python -m uvicorn app.main:app --port 8001  # 改用8001
  ```
- Docker部署：编辑docker-compose.yml改端口映射

### 问题4: 内存不足
**症状：** 应用崩溃或变慢
**解决：**
- Docker部署：编辑docker-compose.yml添加内存限制
  ```yaml
  api:
    mem_limit: 1g
  ```
- 腾讯云：升级实例配置

### 问题5: PDF解析失败
**症状：** "PDF parsing failed"
**解决：**
1. 确保PDF文件不损坏
2. 某些扫描型PDF需要配置Mathpix OCR
3. 检查文件大小是否超过100MB

---

## 📊 部署后监控

### Docker部署日志检查
```bash
# 查看实时日志
docker-compose logs -f

# 只查看API日志
docker-compose logs -f api

# 查看历史日志
docker-compose logs api | head -100
```

### 查看系统指标
```bash
curl http://localhost:8000/api/v1/metrics
```

**返回示例：**
```json
{
  "total_tasks": 5,
  "completed_tasks": 4,
  "failed_tasks": 1,
  "success_rate": 0.8,
  "timestamp": "2024-01-01T00:00:00"
}
```

### Docker容器监控
```bash
# 查看容器状态
docker-compose ps

# 查看容器资源使用
docker stats

# 进入容器交互式shell
docker-compose exec api bash
```

---

## 🔒 生产环境建议

### 1. 安全配置
```bash
# 修改Redis密码
REDIS_PASSWORD=your-secure-password

# 启用HTTPS（Nginx配置）
# 上传SSL证书到 docker/ssl/

# 限制API访问IP
# 在Nginx配置中添加allow/deny
```

### 2. 备份策略
```bash
# 定期备份向量数据库
docker-compose exec api tar -czf backup.tar.gz /app/data/

# 导出Redis数据
docker-compose exec redis redis-cli BGSAVE
```

### 3. 监控告警
```bash
# 使用healthcheck监控
docker-compose ps  # 查看HEALTH状态

# 配置日志收集（可选）
# 将日志输出到ELK或其他日志系统
```

### 4. 性能优化
```bash
# 增加worker进程数
WORKERS=8  # 根据CPU核心数调整

# 启用Redis缓存
ENABLE_REDIS_CACHE=true
REDIS_TTL=3600
```

---

## 📞 获取帮助

### 文档
- 详细文档: [README.md](README.md)
- 快速开始: [QUICKSTART.md](QUICKSTART.md)
- API文档: http://localhost:8000/docs

### 联系方式
- 问题反馈: GitHub Issues
- 邮件支持: support@academic-assistant.ai
- 文档地址: https://docs.academic-assistant.ai

---

## ✨ 部署完成后

1. **测试应用功能**
   - 上传测试论文
   - 验证各个分析功能
   - 检查结果准确性

2. **配置域名（可选）**
   - 购买域名
   - 配置DNS解析
   - 修改Nginx配置

3. **设置监控告警**
   - 配置日志收集
   - 设置异常告警
   - 监控性能指标

4. **制定维护计划**
   - 定期备份数据
   - 更新依赖包
   - 监控系统资源

---

**🎉 部署完成！祝你使用愉快！**
