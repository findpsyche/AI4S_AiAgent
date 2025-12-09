#!/bin/bash

# 项目完整性检查脚本
# Project Completeness Verification Script

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 统计变量
TOTAL=0
FOUND=0

# 检查函数
check_file() {
    local file=$1
    local description=$2
    
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        echo "  📝 $description"
        FOUND=$((FOUND + 1))
    else
        echo -e "${RED}✗${NC} $file"
        echo "  ❌ 缺失：$description"
    fi
}

check_directory() {
    local dir=$1
    local description=$2
    
    TOTAL=$((TOTAL + 1))
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $dir/"
        echo "  📁 $description"
        FOUND=$((FOUND + 1))
    else
        echo -e "${RED}✗${NC} $dir/"
        echo "  ❌ 缺失：$description"
    fi
}

# 开始检查
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  学术助手系统 - 项目完整性检查${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}[1/5] 检查核心应用文件...${NC}"
check_file "app/main.py" "FastAPI应用入口"
check_file "app/config.py" "全局配置管理"
check_file "app/__init__.py" "包初始化文件"
echo ""

echo -e "${YELLOW}[2/5] 检查Agent模块...${NC}"
check_file "app/agents/__init__.py" "Agent模块入口"
check_file "app/agents/orchestrator.py" "主编排器"
check_file "app/agents/paper_parser.py" "论文解析Agent"
check_file "app/agents/math_model_agent.py" "数学模型Agent"
check_file "app/agents/domain_analyzer.py" "领域分析Agent"
check_file "app/agents/scholar_analyzer.py" "学者分析Agent"
check_file "app/agents/tech_roadmap.py" "技术路线Agent"
echo ""

echo -e "${YELLOW}[3/5] 检查服务和数据模型...${NC}"
check_file "app/services/__init__.py" "服务模块入口"
check_file "app/services/cache_service.py" "Redis缓存服务"
check_file "app/services/rag_service.py" "RAG检索服务"
check_file "app/models/__init__.py" "数据模型入口"
check_file "app/models/schemas.py" "Pydantic数据定义"
check_file "app/utils/__init__.py" "工具函数"
echo ""

echo -e "${YELLOW}[4/5] 检查Docker和脚本...${NC}"
check_file "docker/Dockerfile" "Docker镜像定义"
check_file "docker/docker-compose.yml" "Docker Compose配置"
check_file "docker/nginx.conf" "Nginx反向代理配置"
check_file "scripts/run_local.sh" "本地启动脚本(Unix)"
check_file "scripts/run_local.bat" "本地启动脚本(Windows)"
check_file "scripts/run_docker.sh" "Docker启动脚本"
check_file "scripts/deploy.py" "通用部署脚本"
check_file "scripts/deploy_tencent_cloud.sh" "腾讯云部署脚本"
echo ""

echo -e "${YELLOW}[5/5] 检查文档和配置...${NC}"
check_file "requirements.txt" "Python依赖列表"
check_file ".env.example" "环境变量示例"
check_file "README.md" "详细项目文档"
check_file "QUICKSTART.md" "快速开始指南"
check_file "DEPLOYMENT_CHECKLIST.md" "部署检查清单"
check_file "PROJECT_SUMMARY.md" "项目总结文档"
echo ""

echo -e "${YELLOW}检查目录结构...${NC}"
check_directory "app" "应用主代码"
check_directory "app/agents" "Agent模块"
check_directory "app/services" "服务层"
check_directory "app/models" "数据模型"
check_directory "app/utils" "工具函数"
check_directory "docker" "Docker配置"
check_directory "scripts" "启动和部署脚本"
check_directory "data" "数据存储"
check_directory "data/uploads" "论文上传目录"
check_directory "data/vector_db" "向量数据库"
check_directory "tests" "测试目录"
echo ""

# 显示结果
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}检查结果${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"

PERCENTAGE=$((FOUND * 100 / TOTAL))

echo "✓ 已找到: $FOUND"
echo "✗ 缺失: $((TOTAL - FOUND))"
echo "总计: $TOTAL"
echo ""
echo "完整度: $PERCENTAGE%"

if [ $PERCENTAGE -eq 100 ]; then
    echo -e "${GREEN}✅ 项目完整！可以开始使用。${NC}"
    exit 0
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  项目基本完整，但有部分文件缺失。${NC}"
    exit 0
else
    echo -e "${RED}❌ 项目不完整，请检查缺失的文件。${NC}"
    exit 1
fi
