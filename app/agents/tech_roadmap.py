"""
技术路线Agent - 分析技术发展历程和未来方向
Tech Roadmap Agent
"""

import logging
import re
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json

from app.models.schemas import TechRoadmapNode
from app.config import settings

logger = logging.getLogger(__name__)


class TechRoadmapAgent:
    """技术路线分析Agent"""
    
    def __init__(self):
        self.logger = logger
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )
    
    async def generate_tech_roadmap(self,
                                   title: str,
                                   abstract: str,
                                   content: str) -> List[TechRoadmapNode]:
        """
        生成技术发展路线图
        
        Args:
            title: 论文标题
            abstract: 摘要
            content: 论文内容
            
        Returns:
            技术路线节点列表
        """
        try:
            # 从论文内容中提取技术演进信息
            nodes = []
            
            # 简单启发式：查找论文中提及的年份和方法
            year_patterns = re.finditer(r'((?:20|19)\d{2})', content)
            method_patterns = re.finditer(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)', content)
            
            years = []
            for match in year_patterns:
                year = int(match.group(1))
                if 1990 <= year <= 2024:
                    years.append(year)
            
            years = sorted(list(set(years)))
            
            # 为每个年份创建节点
            for i, year in enumerate(years[:5]):  # 限制5个节点
                node = TechRoadmapNode(
                    method_name=f"Method_{i+1}",
                    year=year,
                    key_papers=[title] if i == len(years) - 1 else [],
                    improvement="Incremental improvement",
                    impact_score=0.5 + i * 0.1
                )
                nodes.append(node)
            
            return nodes
            
        except Exception as e:
            self.logger.error(f"技术路线分析错误: {str(e)}")
            return []
