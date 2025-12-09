"""
数学模型Agent - 识别和解析数学公式
Math Model Extraction Agent
"""

import logging
import re
import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import ConfigDict

from app.models.schemas import MathModel
from app.config import settings

logger = logging.getLogger(__name__)


class MathModelAgent:
    """数学模型提取Agent"""
    
    def __init__(self):
        self.logger = logger
        # 禁用代理验证，防止 Pydantic 验证错误
        import os
        os.environ['OPENAI_PROXY'] = ''
        
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是数学公式提取专家。分析论文文本,提取所有重要的数学模型、公式和算法。

对每个公式,提供:
1. 公式名称或简短描述
2. LaTeX格式的公式
3. 公式的含义和用途
4. 公式类型(equation/theorem/algorithm/property)
5. 重要性评分(0-1)
6. 论文中的位置

返回JSON格式的列表,例如:
[
  {
    "formula": "Loss Function",
    "latex": "\\\\mathcal{L} = -\\\\sum y \\\\log(\\\\hat{y})",
    "description": "交叉熵损失函数",
    "formula_type": "equation",
    "importance": 0.9,
    "location": "Section 3.2"
  }
]"""),
            ("user", "请分析以下论文文本并提取数学模型:\n\n{input}")
        ])
    
    async def extract_math_models(self, paper_text: str) -> List[MathModel]:
        """
        提取论文中的数学模型
        
        Args:
            paper_text: 论文文本内容
            
        Returns:
            MathModel对象列表
        """
        try:
            # 截取前20000字符避免token超限
            text_to_analyze = paper_text[:20000]
            
            response = self.llm.invoke(
                self.prompt.format_messages(input=text_to_analyze)
            )
            
            # 解析LLM响应
            content = response.content
            
            # 尝试提取JSON
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                try:
                    models_data = json.loads(json_match.group())
                    models = []
                    for item in models_data:
                        try:
                            model = MathModel(**item)
                            models.append(model)
                        except Exception as e:
                            self.logger.warning(f"模型解析失败: {e}")
                    return models
                except json.JSONDecodeError:
                    pass
            
            # 降级方案：使用正则表达式提取
            return self._extract_formulas_regex(paper_text)
            
        except Exception as e:
            self.logger.error(f"数学模型提取错误: {str(e)}")
            return []
    
    def _extract_formulas_regex(self, text: str) -> List[MathModel]:
        """使用正则表达式提取公式的降级方案"""
        models = []
        
        # 匹配LaTeX公式
        latex_pattern = r'\$\$?(.*?)\$\$?'
        matches = re.finditer(latex_pattern, text)
        
        for i, match in enumerate(matches):
            if i >= 10:  # 限制数量
                break
            
            latex = match.group(1).strip()
            
            # 创建简单的MathModel
            model = MathModel(
                formula=f"Formula_{i+1}",
                latex=latex,
                description="Extracted formula",
                formula_type="equation",
                location=f"Text position {match.start()}",
                importance=0.5
            )
            models.append(model)
        
        return models
