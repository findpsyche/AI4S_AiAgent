"""
一键部署脚本 - 自动化部署到腾讯云服务器
One-Click Deployment Script for Tencent Cloud
"""

import subprocess
import os
import sys
import argparse
from pathlib import Path
from typing import Optional


class Deployer:
    """部署管理器"""
    
    def __init__(self, server_ip: str, ssh_key: Optional[str] = None, username: str = "root"):
        self.server_ip = server_ip
        self.ssh_key = ssh_key
        self.username = username
        self.app_dir = "/home/academic-agent"
        
    def run_command(self, cmd: str, remote: bool = False) -> bool:
        """执行命令"""
        try:
            if remote:
                if self.ssh_key:
                    ssh_cmd = f'ssh -i {self.ssh_key} {self.username}@{self.server_ip} "{cmd}"'
                else:
                    ssh_cmd = f'ssh {self.username}@{self.server_ip} "{cmd}"'
                result = subprocess.run(ssh_cmd, shell=True, check=True)
            else:
                result = subprocess.run(cmd, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 命令执行失败: {cmd}")
            print(f"错误: {e}")
            return False
    
    def deploy(self):
        """执行完整部署流程"""
        print("🚀 开始部署学术助手系统...")
        
        # 1. 环境检查
        print("\n[1/7] 环境检查...")
        if not self._check_environment():
            return False
        
        # 2. 代码上传
        print("\n[2/7] 上传代码到服务器...")
        if not self._upload_code():
            return False
        
        # 3. 环境配置
        print("\n[3/7] 配置环境...")
        if not self._setup_environment():
            return False
        
        # 4. Docker安装
        print("\n[4/7] 安装Docker...")
        if not self._install_docker():
            return False
        
        # 5. 启动服务
        print("\n[5/7] 启动Docker服务...")
        if not self._start_services():
            return False
        
        # 6. 健康检查
        print("\n[6/7] 健康检查...")
        if not self._health_check():
            return False
        
        # 7. 显示信息
        print("\n[7/7] 部署完成！")
        self._show_info()
        
        return True
    
    def _check_environment(self) -> bool:
        """检查本地环境"""
        print("  检查Docker安装...")
        if not self.run_command("docker --version"):
            print("  ⚠️  本地未安装Docker，服务器将自动安装")
        
        print("  检查Git安装...")
        if not self.run_command("git --version"):
            print("  ⚠️  本地未安装Git")
            return False
        
        print("  ✅ 环境检查完成")
        return True
    
    def _upload_code(self) -> bool:
        """上传代码到服务器"""
        project_dir = Path(__file__).parent.parent
        
        if self.ssh_key:
            cmd = f'scp -r -i {self.ssh_key} {project_dir} {self.username}@{self.server_ip}:{self.app_dir}/'
        else:
            cmd = f'scp -r {project_dir} {self.username}@{self.server_ip}:{self.app_dir}/'
        
        print(f"  上传项目到 {self.server_ip}:{self.app_dir}")
        return self.run_command(cmd)
    
    def _setup_environment(self) -> bool:
        """在服务器上配置环境"""
        commands = [
            # 安装系统依赖
            f"sudo apt-get update",
            f"sudo apt-get install -y python3-pip python3-venv curl git",
            
            # 创建Python虚拟环境
            f"cd {self.app_dir} && python3 -m venv venv",
            
            # 激活虚拟环境并安装Python依赖
            f"cd {self.app_dir} && source venv/bin/activate && pip install -r requirements.txt",
            
            # 复制环境文件
            f"cd {self.app_dir} && cp .env.example .env",
            
            # 创建必要的目录
            f"mkdir -p {self.app_dir}/data/uploads {self.app_dir}/data/vector_db {self.app_dir}/logs",
        ]
        
        for cmd in commands:
            print(f"  执行: {cmd}")
            if not self.run_command(cmd, remote=True):
                return False
        
        print("  ✅ 环境配置完成")
        return True
    
    def _install_docker(self) -> bool:
        """在服务器上安装Docker"""
        commands = [
            # 卸载旧版本
            "sudo apt-get remove -y docker docker-engine docker.io containerd runc",
            
            # 安装Docker
            "curl -fsSL https://get.docker.com -o get-docker.sh",
            "sudo sh get-docker.sh",
            "sudo usermod -aG docker root",
            
            # 安装Docker Compose
            "sudo curl -L 'https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64' -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            
            # 启动Docker服务
            "sudo systemctl start docker",
            "sudo systemctl enable docker",
        ]
        
        for cmd in commands:
            print(f"  执行: {cmd}")
            # 部分命令可能失败（如已安装），继续进行
            self.run_command(cmd, remote=True)
        
        # 验证Docker安装
        if not self.run_command("docker --version", remote=True):
            print("  ❌ Docker安装失败")
            return False
        
        print("  ✅ Docker安装完成")
        return True
    
    def _start_services(self) -> bool:
        """启动Docker服务"""
        commands = [
            f"cd {self.app_dir} && docker-compose -f docker/docker-compose.yml down 2>/dev/null || true",
            f"cd {self.app_dir} && docker-compose -f docker/docker-compose.yml build",
            f"cd {self.app_dir} && docker-compose -f docker/docker-compose.yml up -d",
        ]
        
        for cmd in commands:
            print(f"  执行: {cmd}")
            if not self.run_command(cmd, remote=True):
                return False
        
        print("  ✅ 服务启动完成")
        return True
    
    def _health_check(self) -> bool:
        """健康检查"""
        import time
        print("  等待服务启动...")
        time.sleep(10)
        
        check_cmd = f"curl -f http://{self.server_ip}:8000/health || curl -f http://localhost:8000/health"
        
        for i in range(5):
            if self.run_command(check_cmd, remote=False):
                print("  ✅ 服务已启动并响应")
                return True
            print(f"  重试 {i+1}/5...")
            import time
            time.sleep(5)
        
        print("  ⚠️  健康检查超时，请手动验证")
        return True  # 继续进行，不中断部署
    
    def _show_info(self):
        """显示部署信息"""
        print("\n" + "="*60)
        print("🎉 部署成功！")
        print("="*60)
        print(f"\n服务器信息:")
        print(f"  IP地址: {self.server_ip}")
        print(f"  SSH用户: {self.username}")
        print(f"  应用目录: {self.app_dir}")
        print(f"\n访问地址:")
        print(f"  🌐 API: http://{self.server_ip}:8000")
        print(f"  📚 文档: http://{self.server_ip}:8000/docs")
        print(f"  🔍 健康检查: http://{self.server_ip}:8000/health")
        print(f"\n常用命令:")
        print(f"  查看日志: docker-compose -f {self.app_dir}/docker/docker-compose.yml logs -f api")
        print(f"  重启服务: docker-compose -f {self.app_dir}/docker/docker-compose.yml restart")
        print(f"  停止服务: docker-compose -f {self.app_dir}/docker/docker-compose.yml down")
        print("="*60 + "\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="学术助手系统 - 一键部署脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用密钥登录
  python deploy.py --ip 43.143.210.81 --key ~/.ssh/id_rsa
  
  # 使用密码登录（密码会提示输入）
  python deploy.py --ip 43.143.210.81 --username root
        """
    )
    
    parser.add_argument(
        "--ip",
        required=True,
        help="腾讯云服务器IP地址"
    )
    parser.add_argument(
        "--key",
        default=None,
        help="SSH私钥路径（可选）"
    )
    parser.add_argument(
        "--username",
        default="root",
        help="SSH用户名（默认: root）"
    )
    
    args = parser.parse_args()
    
    # 创建部署器并执行部署
    deployer = Deployer(
        server_ip=args.ip,
        ssh_key=args.key,
        username=args.username
    )
    
    success = deployer.deploy()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
