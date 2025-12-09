"""
学者分析Agent - 识别领域内的关键学者和学术关系
Scholar Analyzer Agent
"""

import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import re

from app.models.schemas import ScholarInfo
from app.config import settings

logger = logging.getLogger(__name__)


class ScholarAnalyzerAgent:
    """学者信息分析Agent"""
    
    def __init__(self):
        self.logger = logger
        import os
        os.environ['OPENAI_PROXY'] = ''
        
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def analyze_scholars(self, 
                              title: str,
                              abstract: str,
                              content: str) -> List[ScholarInfo]:
        """
        识别论文中引用的关键学者
        
        Args:
            title: 论文标题
            abstract: 摘要
            content: 论文内容
            
        Returns:
            ScholarInfo列表
        """
        try:
            # 从论文内容中提取学者名字
            scholars_names = self._extract_scholar_names(content)
            
            scholars = []
            for name in scholars_names[:5]:  # 限制到5个
                scholar = ScholarInfo(
                    name=name,
                    representative_works=[],
                    role="contributor"
                )
                scholars.append(scholar)
            
            return scholars
            
        except Exception as e:
            self.logger.error(f"学者分析错误: {str(e)}")
            return []
    
    def _extract_scholar_names(self, text: str) -> List[str]:
        """从文本中提取可能的学者名字"""
        # 简单的启发式方法：查找括号内的名字
        names = []
        
        # 匹配 "Name et al." 或 "(Name, Year)" 模式
        patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+et\s+al',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+),\s+\d{4}',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                name = match.group(1).strip()
                if name not in names and len(name) > 5:
                    names.append(name)
        
        return names[:10]
