"""
FastAPI主应用入口
Main FastAPI Application
"""

import logging
import asyncio
import uuid
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.models.schemas import PaperInput, PaperAnalysis, AnalysisStatus, TaskResponse
from app.agents.orchestrator import AcademicAnalysisOrchestrator
from app.services.cache_service import CacheService
from app.services.rag_service import RAGService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="学术助手 - AI驱动的论文分析系统"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局服务实例
orchestrator = AcademicAnalysisOrchestrator()
cache_service = CacheService()
rag_service = RAGService()

# 内存任务队列
task_queue: dict = {}


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 学术助手系统启动中...")
    
    # 创建必要的目录
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)
    
    # 连接服务
    await cache_service.connect()
    await rag_service.initialize()
    
    logger.info("✅ 系统启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    await cache_service.disconnect()
    logger.info("👋 系统已关闭")


@app.get("/")
async def root():
    """根路由 - 健康检查"""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "status": "/api/v1/status/{task_id}",
            "search": "/api/v1/search",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}


@app.post("/api/v1/analyze", response_model=TaskResponse)
async def analyze_paper(
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile] = File(None),
    arxiv_id: Optional[str] = None,
    doi: Optional[str] = None,
    title: Optional[str] = None
):
    """
    论文分析主接口
    
    支持三种输入方式：
    1. 上传PDF文件
    2. 提供arXiv ID
    3. 提供DOI
    """
    try:
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 检查缓存
        cache_key = None
        if arxiv_id:
            cache_key = f"paper:arxiv:{arxiv_id}"
        elif doi:
            cache_key = f"paper:doi:{doi}"
        
        if cache_key and settings.ENABLE_REDIS_CACHE:
            cached_result = await cache_service.get(cache_key)
            if cached_result:
                logger.info(f"缓存命中: {cache_key}")
                return TaskResponse(
                    task_id=task_id,
                    status=AnalysisStatus.COMPLETED,
                    result=PaperAnalysis(**cached_result)
                )
        
        # 验证输入
        if not file and not arxiv_id and not doi:
            raise HTTPException(
                status_code=400,
                detail="必须提供PDF文件、arXiv ID或DOI之一"
            )
        
        # 保存上传的文件
        file_path = None
        if file:
            file_path = f"{settings.UPLOAD_DIR}/{task_id}_{file.filename}"
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
        
        # 创建任务
        paper_input = PaperInput(
            file_path=file_path,
            arxiv_id=arxiv_id,
            doi=doi,
            title=title
        )
        
        # 初始化任务状态
        task_queue[task_id] = {
            "status": AnalysisStatus.PENDING,
            "progress": 0,
            "result": None,
            "error": None,
            "created_at": datetime.now()
        }
        
        # 后台执行分析
        background_tasks.add_task(
            run_analysis,
            task_id,
            paper_input,
            cache_key
        )
        
        return TaskResponse(
            task_id=task_id,
            status=AnalysisStatus.PROCESSING,
            message=f"分析已启动，使用 /api/v1/status/{task_id} 查询进度"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"分析接口错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def run_analysis(task_id: str, paper_input: PaperInput, cache_key: Optional[str]):
    """后台执行论文分析"""
    try:
        logger.info(f"[{task_id}] 开始分析")
        task_queue[task_id]["status"] = AnalysisStatus.PROCESSING
        task_queue[task_id]["progress"] = 10
        
        # 执行分析
        result = await orchestrator.analyze_paper(paper_input)
        
        task_queue[task_id]["progress"] = 100
        task_queue[task_id]["status"] = AnalysisStatus.COMPLETED
        task_queue[task_id]["result"] = result.dict()
        
        # 缓存结果
        if cache_key and settings.ENABLE_REDIS_CACHE:
            await cache_service.set(cache_key, result.dict())
        
        logger.info(f"[{task_id}] 分析完成")
        
    except Exception as e:
        logger.error(f"[{task_id}] 分析失败: {str(e)}")
        task_queue[task_id]["status"] = AnalysisStatus.FAILED
        task_queue[task_id]["error"] = str(e)


@app.get("/api/v1/status/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """查询任务执行状态"""
    if task_id not in task_queue:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = task_queue[task_id]
    
    return TaskResponse(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        result=PaperAnalysis(**task["result"]) if task["result"] else None,
        error=task["error"]
    )


@app.get("/api/v1/search")
async def search_papers(query: str, limit: int = 10):
    """
    在知识库中搜索相似论文
    """
    try:
        if limit > 50:
            limit = 50
        
        results = await rag_service.search(query, limit=limit)
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"搜索错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/metrics")
async def get_metrics():
    """获取系统性能指标"""
    total_tasks = len(task_queue)
    completed = sum(1 for t in task_queue.values() if t["status"] == AnalysisStatus.COMPLETED)
    failed = sum(1 for t in task_queue.values() if t["status"] == AnalysisStatus.FAILED)
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed,
        "failed_tasks": failed,
        "success_rate": completed / max(total_tasks, 1),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
