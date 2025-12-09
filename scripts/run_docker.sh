#!/bin/bash

# 学术助手系统 - Docker一键启动脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  学术助手系统 - Docker启动${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# 检查Docker
echo -e "${YELLOW}[1/3] 检查Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ 未安装Docker${NC}"
    echo "请访问 https://docs.docker.com/get-docker/ 安装Docker"
    exit 1
fi
docker --version

# 检查环境文件
echo -e "\n${YELLOW}[2/3] 检查配置...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  已创建.env文件，请编辑配置OpenAI API Key${NC}"
    exit 1
else
    echo "✅ .env文件已存在"
fi

# 启动服务
echo -e "\n${YELLOW}[3/3] 启动Docker服务...${NC}"

cd docker

# 构建镜像
echo "构建Docker镜像..."
docker-compose build

# 启动容器
echo "启动容器..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查健康状态
echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}✅ 服务启动完成！${NC}"
echo -e "${GREEN}=====================================${NC}\n"

# 获取容器ID
API_CONTAINER=$(docker-compose ps -q api)

echo "访问地址:"
echo -e "  🌐 API:      http://localhost:8000"
echo -e "  📚 文档:     http://localhost:8000/docs"
echo -e "  🔍 健康检查: http://localhost:8000/health\n"

echo "常用命令:"
echo -e "  查看日志:   ${BLUE}docker-compose logs -f api${NC}"
echo -e "  停止服务:   ${BLUE}docker-compose down${NC}"
echo -e "  重启服务:   ${BLUE}docker-compose restart${NC}\n"

echo "正在进行健康检查..."
for i in {1..10}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 服务运行正常${NC}\n"
        exit 0
    fi
    echo "重试 $i/10..."
    sleep 2
done

echo -e "${YELLOW}⚠️  健康检查超时，请使用 'docker-compose logs' 查看日志${NC}\n"
