"""
主编排器 - 协调所有Agent的执行
Main Orchestrator
"""

import logging
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from app.config import settings
from app.models.schemas import PaperInput, PaperAnalysis, AnalysisStatus
from app.agents.paper_parser import PaperParserAgent
from app.agents.math_model_agent import MathModelAgent
from app.agents.domain_analyzer import DomainAnalyzerAgent
from app.agents.scholar_analyzer import ScholarAnalyzerAgent
from app.agents.tech_roadmap import TechRoadmapAgent

logger = logging.getLogger(__name__)


class AcademicAnalysisOrchestrator:
    """学术论文分析编排器"""
    
    def __init__(self):
        self.logger = logger
        
        # 初始化所有Agent
        self.parser_agent = PaperParserAgent()
        self.math_agent = MathModelAgent()
        self.domain_agent = DomainAnalyzerAgent()
        self.scholar_agent = ScholarAnalyzerAgent()
        self.tech_roadmap_agent = TechRoadmapAgent()
    
    async def analyze_paper(self, paper_input: PaperInput) -> PaperAnalysis:
        """
        执行完整的论文分析流程
        
        Args:
            paper_input: 论文输入信息
            
        Returns:
            完整的分析结果
        """
        start_time = datetime.now()
        
        try:
            # 1. 解析论文
            self.logger.info(f"开始解析论文: {paper_input.title or paper_input.file_path}")
            
            if paper_input.file_path:
                parsed_data = self.parser_agent.parse_pdf(paper_input.file_path)
            else:
                parsed_data = self._get_paper_from_source(paper_input)
            
            if not parsed_data.get("success"):
                raise Exception(f"论文解析失败: {parsed_data.get('error')}")
            
            metadata = parsed_data["metadata"]
            full_text = parsed_data["full_text"]
            
            # 2. 并行执行多个分析任务
            self.logger.info("开始并行分析...")
            
            analysis_tasks = [
                self._analyze_math_models(full_text),
                self._analyze_domain(metadata, full_text),
                self._analyze_scholars(metadata, full_text),
                self._analyze_tech_roadmap(metadata, full_text),
            ]
            
            math_models, domain_info, scholars, tech_roadmap = await asyncio.gather(
                *analysis_tasks,
                return_exceptions=True
            )
            
            # 处理异常
            if isinstance(math_models, Exception):
                self.logger.warning(f"数学模型分析异常: {math_models}")
                math_models = []
            if isinstance(domain_info, Exception):
                self.logger.warning(f"领域分析异常: {domain_info}")
                domain_info = None
            if isinstance(scholars, Exception):
                self.logger.warning(f"学者分析异常: {scholars}")
                scholars = []
            if isinstance(tech_roadmap, Exception):
                self.logger.warning(f"技术路线分析异常: {tech_roadmap}")
                tech_roadmap = []
            
            # 3. 创建分析结果
            analysis_duration = (datetime.now() - start_time).total_seconds()
            
            paper_analysis = PaperAnalysis(
                paper_id=str(uuid.uuid4()),
                title=metadata.get("title", "Unknown"),
                authors=metadata.get("authors", []),
                abstract=metadata.get("abstract", ""),
                year=self._extract_year(full_text),
                math_models=math_models or [],
                domain_info=domain_info,
                key_scholars=scholars or [],
                tech_roadmap=tech_roadmap or [],
                innovation_points=self._extract_innovations(full_text),
                limitations=self._extract_limitations(full_text),
                citations_count=0,
                references_count=0,
                reproducibility_score=self._calculate_reproducibility(full_text),
                status=AnalysisStatus.COMPLETED,
                analysis_duration=analysis_duration,
                summary=self._generate_summary(metadata, full_text)
            )
            
            self.logger.info(f"论文分析完成，耗时: {analysis_duration:.2f}秒")
            
            return paper_analysis
            
        except Exception as e:
            self.logger.error(f"分析过程出错: {str(e)}")
            raise
    
    async def _analyze_math_models(self, text: str):
        """分析数学模型"""
        return await self.math_agent.extract_math_models(text)
    
    async def _analyze_domain(self, metadata: Dict, text: str):
        """分析研究领域"""
        return await self.domain_agent.analyze_domain(
            title=metadata.get("title", ""),
            abstract=metadata.get("abstract", ""),
            content=text
        )
    
    async def _analyze_scholars(self, metadata: Dict, text: str):
        """分析学者信息"""
        return await self.scholar_agent.analyze_scholars(
            title=metadata.get("title", ""),
            abstract=metadata.get("abstract", ""),
            content=text
        )
    
    async def _analyze_tech_roadmap(self, metadata: Dict, text: str):
        """分析技术路线"""
        return await self.tech_roadmap_agent.generate_tech_roadmap(
            title=metadata.get("title", ""),
            abstract=metadata.get("abstract", ""),
            content=text
        )
    
    def _get_paper_from_source(self, paper_input: PaperInput) -> Dict[str, Any]:
        """从外部源获取论文（arXiv, DOI等）"""
        # 简化实现，实际需要调用API
        return {
            "success": True,
            "metadata": {
                "title": paper_input.title or "Unknown",
                "authors": [],
                "abstract": ""
            },
            "full_text": "",
            "total_pages": 0
        }
    
    def _extract_year(self, text: str) -> int:
        """从文本中提取发表年份"""
        import re
        year_match = re.search(r'(20|19)\d{2}', text)
        if year_match:
            return int(year_match.group(0))
        return 2024
    
    def _extract_innovations(self, text: str) -> list:
        """提取创新点"""
        keywords = ["novel", "new", "propose", "first", "innovative"]
        innovations = []
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                innovations.append(f"Mentioned {keyword} approach")
        
        return innovations[:5]
    
    def _extract_limitations(self, text: str) -> list:
        """提取局限性"""
        keywords = ["limitation", "challenge", "future work", "limitation"]
        limitations = []
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                limitations.append(f"Addresses {keyword}")
        
        return limitations[:5]
    
    def _calculate_reproducibility(self, text: str) -> float:
        """计算可复现性评分"""
        keywords = ["code", "dataset", "github", "implementation", "reproducible"]
        count = sum(1 for kw in keywords if kw.lower() in text.lower())
        return min(count / len(keywords), 1.0)
    
    def _generate_summary(self, metadata: Dict, text: str) -> str:
        """生成分析摘要"""
        title = metadata.get("title", "Unknown Paper")
        return f"Analysis of paper: {title[:50]}..."
