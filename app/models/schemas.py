"""
Pydantic数据模型定义
Data Schema Definitions
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    """分析任务状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class PaperInput(BaseModel):
    """论文输入模型"""
    file_path: Optional[str] = Field(None, description="本地PDF文件路径")
    arxiv_id: Optional[str] = Field(None, description="arXiv论文ID")
    doi: Optional[str] = Field(None, description="DOI标识符")
    url: Optional[str] = Field(None, description="论文URL")
    title: Optional[str] = Field(None, description="论文标题")


class MathModel(BaseModel):
    """数学模型"""
    formula: str = Field(..., description="公式名称或描述")
    latex: str = Field(..., description="LaTeX格式公式")
    description: str = Field(..., description="公式含义解释")
    formula_type: str = Field(..., description="公式类型: equation/theorem/algorithm/property")
    location: str = Field(..., description="公式在论文中的位置")
    importance: float = Field(default=0.5, description="重要性评分 0-1")


class DomainInfo(BaseModel):
    """研究领域信息"""
    primary_field: str = Field(..., description="主要研究领域")
    sub_fields: List[str] = Field(default_factory=list, description="子领域列表")
    keywords: List[str] = Field(default_factory=list, description="关键词")
    related_fields: List[str] = Field(default_factory=list, description="相关领域")
    confidence: float = Field(default=0.8, description="分类置信度 0-1")


class ScholarInfo(BaseModel):
    """学者信息"""
    name: str = Field(..., description="学者名字")
    affiliation: Optional[str] = Field(None, description="所属机构")
    h_index: Optional[int] = Field(None, description="H指数")
    citation_count: Optional[int] = Field(None, description="总引用数")
    representative_works: List[str] = Field(default_factory=list, description="代表作")
    role: str = Field(default="contributor", description="角色: founder/pioneer/contributor")


class TechRoadmapNode(BaseModel):
    """技术路线节点"""
    method_name: str = Field(..., description="方法或技术名称")
    year: int = Field(..., description="发布年份")
    key_papers: List[str] = Field(default_factory=list, description="关键论文标题")
    improvement: str = Field(..., description="相对前作的改进点")
    impact_score: float = Field(default=0.5, description="影响力评分 0-1")


class ResearchGap(BaseModel):
    """研究空白/机会"""
    gap_description: str = Field(..., description="空白描述")
    importance: float = Field(default=0.5, description="重要性 0-1")
    feasibility: float = Field(default=0.5, description="可行性 0-1")
    suggested_approach: Optional[str] = Field(None, description="建议研究方向")


class PaperAnalysis(BaseModel):
    """完整论文分析结果"""
    # 基本信息
    paper_id: str = Field(..., description="论文唯一ID")
    title: str = Field(..., description="论文标题")
    authors: List[str] = Field(default_factory=list, description="作者列表")
    abstract: str = Field(default="", description="摘要")
    year: int = Field(..., description="发表年份")
    url: Optional[str] = Field(None, description="论文链接")
    
    # 核心分析结果
    math_models: List[MathModel] = Field(default_factory=list, description="提取的数学模型")
    domain_info: Optional[DomainInfo] = Field(None, description="研究领域信息")
    key_scholars: List[ScholarInfo] = Field(default_factory=list, description="关键学者")
    tech_roadmap: List[TechRoadmapNode] = Field(default_factory=list, description="技术发展路线")
    
    # 深度分析
    innovation_points: List[str] = Field(default_factory=list, description="创新点")
    limitations: List[str] = Field(default_factory=list, description="论文局限性")
    research_gaps: List[ResearchGap] = Field(default_factory=list, description="研究空白")
    reproducibility_score: float = Field(default=0.5, description="可复现性评分 0-1")
    
    # 引用统计
    citations_count: int = Field(default=0, description="被引用次数")
    references_count: int = Field(default=0, description="参考文献数")
    related_papers: List[str] = Field(default_factory=list, description="相关论文标题")
    
    # 元数据
    status: AnalysisStatus = Field(default=AnalysisStatus.COMPLETED, description="分析状态")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    analysis_duration: float = Field(default=0.0, description="分析耗时（秒）")
    summary: Optional[str] = Field(None, description="分析摘要")


class TaskResponse(BaseModel):
    """异步任务响应"""
    task_id: str = Field(..., description="任务ID")
    status: AnalysisStatus = Field(..., description="任务状态")
    progress: int = Field(default=0, description="进度百分比 0-100")
    message: Optional[str] = Field(None, description="提示消息")
    result: Optional[PaperAnalysis] = Field(None, description="分析结果")
    error: Optional[str] = Field(None, description="错误信息")
    created_at: datetime = Field(default_factory=datetime.now)


class SearchResult(BaseModel):
    """搜索结果项"""
    title: str
    authors: List[str]
    year: Optional[int]
    similarity: float
    snippet: Optional[str]


class DomainStats(BaseModel):
    """领域统计信息"""
    domain: str
    paper_count: int
    top_scholars: List[str]
    trending_topics: List[str]
    recent_breakthroughs: List[str]
