@echo off
REM 学术助手系统 - 本地启动脚本（Windows）

setlocal enabledelayedexpansion

color 0B
cls

echo =====================================
echo   学术助手系统 - 本地启动
echo =====================================

REM 检查Python版本
echo.
echo [1/5] 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Python
    pause
    exit /b 1
)
python --version

REM 创建虚拟环境
echo.
echo [2/5] 创建虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo ✅ 虚拟环境创建完成
) else (
    echo ✅ 虚拟环境已存在
)

REM 激活虚拟环境
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活

REM 安装依赖
echo.
echo [3/5] 安装Python依赖...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo ✅ 依赖安装完成

REM 环境配置
echo.
echo [4/5] 配置环境...
if not exist ".env" (
    copy .env.example .env
    echo ✅ 已创建.env文件（请编辑配置OpenAI API Key）
) else (
    echo ✅ .env文件已存在
)

REM 创建必要目录
if not exist "data\uploads" mkdir data\uploads
if not exist "data\vector_db" mkdir data\vector_db
if not exist "logs" mkdir logs
echo ✅ 目录结构已创建

REM 启动应用
echo.
echo [5/5] 启动应用...
echo =====================================
echo ✅ 系统启动成功！
echo =====================================
echo.
echo 访问地址:
echo   🌐 API:     http://localhost:8000
echo   📚 文档:    http://localhost:8000/docs
echo   🔍 健康检查: http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
