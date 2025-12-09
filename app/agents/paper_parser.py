"""
论文解析Agent - 负责PDF解析和文本结构化提取
Paper Parser Agent
"""

import logging
from typing import Dict, Any, Optional, List
import fitz  # PyMuPDF (imported as fitz)
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class PaperParserAgent:
    """论文解析Agent"""
    
    def __init__(self):
        self.logger = logger
        
    def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        解析PDF文件，提取结构化信息
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            包含元数据、全文、章节等信息的字典
        """
        try:
            doc = pymupdf.open(pdf_path)
            
            # 提取文本内容
            full_text = ""
            sections = {}
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text += text + "\n"
            
            # 识别主要章节
            sections = self._identify_sections(full_text)
            
            # 提取元数据
            metadata = self._extract_metadata(doc, full_text)
            
            doc.close()
            
            return {
                "metadata": metadata,
                "full_text": full_text,
                "sections": sections,
                "total_pages": len(doc),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"PDF解析错误: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_metadata(self, doc, full_text: str) -> Dict[str, Any]:
        """提取论文元数据"""
        first_page = doc[0].get_text()
        lines = [l.strip() for l in first_page.split("\n") if l.strip()]
        
        return {
            "title": self._extract_title(lines, full_text),
            "authors": self._extract_authors(lines, full_text),
            "abstract": self._extract_abstract(full_text),
            "num_pages": len(doc),
            "extraction_date": datetime.now().isoformat()
        }
    
    def _extract_title(self, first_page_lines: List[str], full_text: str) -> str:
        """提取论文标题"""
        # 通常标题在首页前3行
        for line in first_page_lines[:5]:
            if len(line) > 10 and len(line) < 200:  # 标题长度限制
                return line
        return "Unknown Title"
    
    def _extract_authors(self, first_page_lines: List[str], full_text: str) -> List[str]:
        """提取作者信息"""
        authors = []
        # 简单的正则表达式匹配
        for line in first_page_lines[:15]:
            # 查找可能的作者行
            if any(keyword in line.lower() for keyword in ["author", "by", "et al"]):
                # 提取括号内的内容（通常是机构）
                authors.append(line)
        
        return authors[:5] if authors else ["Unknown Authors"]
    
    def _extract_abstract(self, full_text: str) -> str:
        """提取摘要"""
        abstract_match = re.search(
            r"(?:ABSTRACT|Abstract|摘要|abstract)(.*?)(?:INTRODUCTION|Introduction|引言|introduction|1\s|1\.)",
            full_text,
            re.IGNORECASE | re.DOTALL
        )
        
        if abstract_match:
            abstract_text = abstract_match.group(1).strip()
            # 限制长度
            return abstract_text[:500] if len(abstract_text) > 500 else abstract_text
        
        return "Abstract not found"
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """识别论文主要章节"""
        sections = {}
        section_keywords = {
            "abstract": [r"(?:ABSTRACT|Abstract|摘要)"],
            "introduction": [r"(?:INTRODUCTION|Introduction|引言|1\s+Introduction)"],
            "methodology": [r"(?:METHOD|METHODOLOGY|Methods|方法|3\s+Method)"],
            "results": [r"(?:RESULT|RESULTS|Results|结果|4\s+Result)"],
            "discussion": [r"(?:DISCUSSION|Discussion|讨论|5\s+Discussion)"],
            "conclusion": [r"(?:CONCLUSION|CONCLUSIONS|Conclusion|结论|6\s+Conclusion)"],
        }
        
        for section_name, patterns in section_keywords.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    # 获取该章节的内容（从匹配位置到下一个章节）
                    start = match.start()
                    # 简化处理：获取接下来的2000字符
                    sections[section_name] = text[start:start+2000]
                    break
        
        return sections


def extract_paper_info_from_text(text: str) -> Dict[str, Any]:
    """从文本中提取论文信息的辅助函数"""
    agent = PaperParserAgent()
    
    # 从纯文本提取信息（不需要PDF）
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    return {
        "title": agent._extract_title(lines, text),
        "authors": agent._extract_authors(lines, text),
        "abstract": agent._extract_abstract(text),
        "sections": agent._identify_sections(text)
    }
