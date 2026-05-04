"""
text_processor.py - 中文文本处理器

使用 jieba 进行中文分词、关键词提取和标签生成。
"""
import jieba
import jieba.analyse
from typing import List, Optional


TECH_TERMS = [
    "pytest", "fixture", "conftest", "parametrize",
    "FastAPI", "FAISS", "BM25", "RAG",
    "Docker", "Kubernetes", "k8s", "kubectl",
    "SQLAlchemy", "Alembic", "Pydantic",
    "threading", "multiprocessing", "asyncio", "coroutine",
    "unittest", "selenium", "playwright", "appium",
    "redis", "kafka", "elasticsearch",
    "numpy", "pandas", "matplotlib",
    "git", "github", "gitlab",
    "linux", "shell", "bash",
    "nginx", "tomcat", "jenkins",
    "oracle", "mysql", "postgresql",
]


class ChineseTextProcessor:
    """中文文本处理器"""
    
    def __init__(self, user_dict_path: Optional[str] = None):
        """初始化，可选加载自定义词典"""
        if user_dict_path:
            jieba.load_userdict(user_dict_path)
        
        self._load_tech_terms()
    
    def _load_tech_terms(self) -> None:
        """加载技术术语词典"""
        for term in TECH_TERMS:
            jieba.add_word(term)
    
    def tokenize(self, text: str) -> List[str]:
        """BM25 分词"""
        return list(jieba.cut(text))
    
    def extract_keywords(self, text: str, topK: int = 5) -> List[str]:
        """提取关键词（TF-IDF）"""
        return jieba.analyse.extract_tags(text, topK=topK)
    
    def generate_tags(self, text: str, topK: int = 5) -> List[str]:
        """生成标签（TextRank）"""
        return jieba.analyse.textrank(text, topK=topK)
    
    def tokenize_for_bm25(self, text: str) -> List[str]:
        """BM25 专用分词（过滤停用词）"""
        tokens = self.tokenize(text)
        return [t.strip() for t in tokens if len(t.strip()) > 1]


if __name__ == "__main__":
    processor = ChineseTextProcessor()
    
    test_text = "pytest fixture 用于定义测试夹具，可以在多个测试用例之间共享"
    
    print("原文:", test_text)
    print("\n分词结果:", processor.tokenize(test_text))
    print("关键词提取:", processor.extract_keywords(test_text, topK=5))
    print("标签生成:", processor.generate_tags(test_text, topK=5))
