#!/bin/bash

# 学术助手系统 - 腾讯云部署一键脚本（改进版）
# Academic Paper Assistant - Tencent Cloud One-Click Deployment Script

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置变量
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="/home/academic-agent"
SERVICE_NAME="academic-agent"

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# 系统检查
check_system() {
    log_info "系统检查中..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log_success "Linux系统检测"
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        log_success "macOS系统检测"
        OS="macos"
    else
        log_error "暂不支持的操作系统: $OSTYPE"
        return 1
    fi
    
    # 检查必要命令
    for cmd in git docker docker-compose; do
        if ! command -v $cmd &> /dev/null; then
            log_warning "$cmd 未安装"
        else
            log_success "$cmd 已安装"
        fi
    done
    
    return 0
}

# SSH连接测试
test_ssh_connection() {
    local server_ip=$1
    local ssh_key=$2
    local username=${3:-root}
    
    log_info "测试SSH连接..."
    
    if [ -n "$ssh_key" ]; then
        if ssh -i "$ssh_key" -o ConnectTimeout=10 "$username@$server_ip" "echo 'SSH连接成功'" &>/dev/null; then
            log_success "SSH连接正常"
            return 0
        else
            log_error "SSH连接失败，请检查IP、密钥或用户名"
            return 1
        fi
    else
        log_warning "未提供SSH密钥，将尝试密码登录"
        return 0
    fi
}

# 部署函数
deploy_to_server() {
    local server_ip=$1
    local ssh_key=$2
    local username=${3:-root}
    
    log_info "开始部署到腾讯云服务器: $server_ip"
    
    # 准备SSH命令
    if [ -n "$ssh_key" ]; then
        SSH_CMD="ssh -i $ssh_key"
    else
        SSH_CMD="ssh"
    fi
    
    SSH_CMD="$SSH_CMD $username@$server_ip"
    
    # 1. 建立项目目录
    log_info "[1/6] 准备项目目录..."
    $SSH_CMD "
        set -e
        mkdir -p $APP_DIR
        cd $APP_DIR
        log_success '目录已创建'
    " || true
    
    # 2. 上传项目文件
    log_info "[2/6] 上传项目文件..."
    if [ -n "$ssh_key" ]; then
        scp -r -i "$ssh_key" "$PROJECT_DIR" "$username@$server_ip:$APP_DIR/" 2>/dev/null || {
            log_warning "文件上传失败，尝试使用git克隆..."
        }
    else
        scp -r "$PROJECT_DIR" "$username@$server_ip:$APP_DIR/" 2>/dev/null || {
            log_warning "文件上传失败"
        }
    fi
    log_success "项目文件已上传"
    
    # 3. 安装系统依赖
    log_info "[3/6] 安装系统依赖..."
    $SSH_CMD "
        set -e
        apt-get update -qq
        apt-get install -y -qq \
            curl \
            git \
            wget \
            build-essential \
            python3-pip \
            python3-dev
        echo '系统依赖安装完成'
    "
    log_success "系统依赖已安装"
    
    # 4. 安装Docker和Docker Compose
    log_info "[4/6] 安装Docker和Docker Compose..."
    $SSH_CMD "
        set -e
        
        # 安装Docker
        if ! command -v docker &> /dev/null; then
            curl -fsSL https://get.docker.com -o get-docker.sh 2>/dev/null
            bash get-docker.sh 2>/dev/null
            rm -f get-docker.sh
        fi
        
        # 启动Docker
        systemctl start docker 2>/dev/null || service docker start 2>/dev/null || true
        systemctl enable docker 2>/dev/null || true
        
        # 安装Docker Compose
        if ! command -v docker-compose &> /dev/null; then
            LATEST=\$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d'\"' -f4)
            curl -L \"https://github.com/docker/compose/releases/download/\$LATEST/docker-compose-Linux-x86_64\" -o /usr/local/bin/docker-compose 2>/dev/null
            chmod +x /usr/local/bin/docker-compose
        fi
        
        echo '✓ Docker已安装'
        docker --version
        docker-compose --version
    "
    log_success "Docker已安装"
    
    # 5. 配置环境和启动服务
    log_info "[5/6] 配置环境和启动服务..."
    $SSH_CMD "
        set -e
        cd $APP_DIR/academic-paper-agent
        
        # 复制环境文件
        if [ ! -f .env ]; then
            cp .env.example .env
            echo '⚠️  已创建.env文件，请手动编辑配置OpenAI API Key'
        fi
        
        # 创建必要目录
        mkdir -p data/uploads data/vector_db logs
        
        # 启动Docker服务
        docker-compose -f docker/docker-compose.yml down 2>/dev/null || true
        docker-compose -f docker/docker-compose.yml build
        docker-compose -f docker/docker-compose.yml up -d
        
        echo '✓ 服务启动中...'
    "
    log_success "环境已配置，服务已启动"
    
    # 6. 健康检查
    log_info "[6/6] 进行健康检查..."
    sleep 10
    
    for i in {1..10}; do
        if curl -sf http://$server_ip:8000/health > /dev/null 2>&1; then
            log_success "健康检查通过"
            break
        fi
        log_warning "健康检查重试 $i/10..."
        sleep 3
    done
}

# 显示部署信息
show_deployment_info() {
    local server_ip=$1
    
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ 部署完成！${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}\n"
    
    echo "服务器信息："
    echo "  IP地址:        $server_ip"
    echo "  应用目录:      /home/academic-agent/academic-paper-agent"
    echo ""
    
    echo "访问地址："
    echo "  🌐 API:        http://$server_ip:8000"
    echo "  📚 文档:       http://$server_ip:8000/docs"
    echo "  🔍 健康检查:   http://$server_ip:8000/health"
    echo ""
    
    echo "常用命令（通过SSH执行）："
    echo "  查看日志:      docker-compose -f /home/academic-agent/academic-paper-agent/docker/docker-compose.yml logs -f api"
    echo "  重启服务:      docker-compose -f /home/academic-agent/academic-paper-agent/docker/docker-compose.yml restart"
    echo "  停止服务:      docker-compose -f /home/academic-agent/academic-paper-agent/docker/docker-compose.yml down"
    echo ""
    
    echo "⚠️  重要提示："
    echo "  1. 请编辑.env文件，填入OPENAI_API_KEY"
    echo "  2. 通过以下命令编辑.env:"
    echo "     ssh root@$server_ip"
    echo "     nano /home/academic-agent/academic-paper-agent/.env"
    echo "  3. 编辑后重启服务: docker-compose restart"
    echo ""
    
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}\n"
}

# 主函数
main() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  学术助手系统 - 腾讯云部署脚本${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"
    
    # 参数检查
    if [ $# -lt 1 ]; then
        echo "使用方法:"
        echo "  bash $0 <server_ip> [ssh_key] [username]"
        echo ""
        echo "示例:"
        echo "  # 使用密钥登录"
        echo "  bash $0 43.143.210.81 ~/.ssh/id_rsa root"
        echo ""
        echo "  # 使用密码登录"
        echo "  bash $0 43.143.210.81"
        exit 1
    fi
    
    local server_ip=$1
    local ssh_key=${2:-}
    local username=${3:-root}
    
    # 系统检查
    if ! check_system; then
        log_error "系统检查失败"
        exit 1
    fi
    
    # 测试SSH连接
    if ! test_ssh_connection "$server_ip" "$ssh_key" "$username"; then
        log_error "无法连接到服务器"
        exit 1
    fi
    
    # 执行部署
    if ! deploy_to_server "$server_ip" "$ssh_key" "$username"; then
        log_error "部署失败"
        exit 1
    fi
    
    # 显示部署信息
    show_deployment_info "$server_ip"
}

# 执行主函数
main "$@"
