"""
领域分析Agent - 识别研究领域和专业范围
Domain Analyzer Agent
"""

import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import re

from app.models.schemas import DomainInfo
from app.config import settings

logger = logging.getLogger(__name__)


class DomainAnalyzerAgent:
    """研究领域分析Agent"""
    
    def __init__(self):
        self.logger = logger
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是学科分类专家。根据论文的标题、摘要和内容,分析其研究领域。

请提供:
1. 主要研究领域 (Computer Vision, NLP, Machine Learning等)
2. 子领域列表 (3-5个相关的更具体的领域)
3. 关键词 (5-10个核心概念)
4. 相关领域 (2-3个交叉学科)
5. 置信度评分 (0-1)

返回JSON格式:
{
  "primary_field": "Computer Vision",
  "sub_fields": ["Object Detection", "Deep Learning"],
  "keywords": ["YOLO", "CNN"],
  "related_fields": ["Machine Learning"],
  "confidence": 0.95
}"""),
            ("user", "请分析以下论文的研究领域:\n\n标题: {title}\n摘要: {abstract}\n内容: {content}")
        ])
    
    async def analyze_domain(self, 
                           title: str, 
                           abstract: str, 
                           content: str) -> DomainInfo:
        """
        分析论文的研究领域
        
        Args:
            title: 论文标题
            abstract: 论文摘要
            content: 论文内容
            
        Returns:
            DomainInfo对象
        """
        try:
            # 截取内容前10000字符
            content_preview = content[:10000]
            
            response = self.llm.invoke(
                self.prompt.format_messages(
                    title=title,
                    abstract=abstract,
                    content=content_preview
                )
            )
            
            # 解析JSON响应
            content = response.content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return DomainInfo(**data)
                except Exception as e:
                    self.logger.warning(f"DomainInfo解析失败: {e}")
            
            # 降级方案
            return self._extract_domain_heuristic(title, abstract)
            
        except Exception as e:
            self.logger.error(f"领域分析错误: {str(e)}")
            return DomainInfo(
                primary_field="Unknown",
                sub_fields=[],
                keywords=[],
                related_fields=[],
                confidence=0.0
            )
    
    def _extract_domain_heuristic(self, title: str, abstract: str) -> DomainInfo:
        """使用启发式方法提取领域信息"""
        
        # 关键词到领域的映射
        domain_keywords = {
            "Computer Vision": ["image", "vision", "visual", "detect", "segment", "pose"],
            "NLP": ["language", "nlp", "text", "semantic", "parsing", "translation"],
            "ML": ["learning", "neural", "network", "deep", "model", "algorithm"],
            "Reinforcement Learning": ["reinforcement", "reward", "policy", "agent"],
        }
        
        text = (title + " " + abstract).lower()
        domain_scores = {}
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            domain_scores[domain] = score
        
        primary_field = max(domain_scores, key=domain_scores.get) if domain_scores else "Unknown"
        
        # 提取关键词
        words = title.split() + abstract.split()
        keywords = [w for w in words if len(w) > 4][:10]
        
        return DomainInfo(
            primary_field=primary_field,
            sub_fields=[],
            keywords=keywords,
            related_fields=[],
            confidence=0.6
        )
