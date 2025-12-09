#!/bin/bash

# 学术助手系统 - 本地启动脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  学术助手系统 - 本地启动${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# 检查Python版本
echo -e "${YELLOW}[1/5] 检查Python版本...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安装Python3"
    exit 1
fi
python3 --version

# 创建虚拟环境
echo -e "\n${YELLOW}[2/5] 创建虚拟环境...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
source venv/bin/activate
echo "✅ 虚拟环境已激活"

# 安装依赖
echo -e "\n${YELLOW}[3/5] 安装Python依赖...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 环境配置
echo -e "\n${YELLOW}[4/5] 配置环境...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ 已创建.env文件（请编辑配置OpenAI API Key）"
else
    echo "✅ .env文件已存在"
fi

# 创建必要目录
mkdir -p data/uploads data/vector_db logs
echo "✅ 目录结构已创建"

# 启动应用
echo -e "\n${YELLOW}[5/5] 启动应用...${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}✅ 系统启动成功！${NC}"
echo -e "${GREEN}=====================================${NC}\n"
echo -e "访问地址:"
echo -e "  🌐 API:     http://localhost:8000"
echo -e "  📚 文档:    http://localhost:8000/docs"
echo -e "  🔍 健康检查: http://localhost:8000/health\n"
echo "按 Ctrl+C 停止服务"

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
