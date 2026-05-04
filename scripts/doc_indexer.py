"""
doc_indexer.py - 文档索引器

解析 mkdocs.yml 的 nav 部分，提取所有文档路径和元数据。
"""
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _ignore_python_tags(loader, tag_suffix, node):
    """忽略 Python 特定的 YAML 标签"""
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None


class SafeLoaderIgnorePython(yaml.SafeLoader):
    """自定义 SafeLoader，忽略 Python 特定标签"""
    pass


SafeLoaderIgnorePython.add_multi_constructor(
    'tag:yaml.org,2002:python/',
    _ignore_python_tags
)


class MkdocsIndexer:
    """文档索引器：解析 mkdocs.yml 并加载文档内容"""
    
    def __init__(self, config_path: str = "mkdocs.yml", docs_dir: str = "docs"):
        self.config_path = Path(config_path)
        self.docs_dir = Path(docs_dir)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载 mkdocs.yml 配置"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"mkdocs.yml 不存在: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=SafeLoaderIgnorePython)
    
    def extract_nav_tree(self) -> List[Dict]:
        """提取导航树，返回结构化文档索引"""
        nav = self.config.get("nav", [])
        return self._parse_nav(nav)
    
    def _parse_nav(self, nav_items: List, parent_category: str = "") -> List[Dict]:
        """递归解析导航树"""
        docs = []
        
        for item in nav_items:
            if isinstance(item, dict):
                for title, path_or_children in item.items():
                    if isinstance(path_or_children, str):
                        category = self._classify_category(path_or_children)
                        docs.append({
                            "title": title,
                            "path": path_or_children,
                            "category": category,
                            "parent": parent_category
                        })
                    elif isinstance(path_or_children, list):
                        docs.extend(
                            self._parse_nav(path_or_children, parent_category=title)
                        )
        
        return docs
    
    def _classify_category(self, path: str) -> str:
        """根据文件路径分类"""
        path_lower = path.lower()
        
        if any(kw in path_lower for kw in ["stock", "chips", "indicator", "strategy"]):
            return "stock"
        elif any(kw in path_lower for kw in ["vibe", "per/"]):
            return "personal"
        elif any(kw in path_lower for kw in ["ielts"]):
            return "learning"
        else:
            return "technical"
    
    def load_all_documents(self, nav_tree: List[Dict]) -> List[Dict]:
        """加载所有文档内容"""
        documents = []
        
        for item in nav_tree:
            content = self._load_document_content(item["path"])
            if content:
                documents.append({
                    **item,
                    "content": content
                })
        
        return documents
    
    def _load_document_content(self, path: str) -> Optional[str]:
        """加载单个文档内容"""
        full_path = self.docs_dir / path
        
        if not full_path.exists():
            logger.warning(f"文档不存在: {full_path}")
            return None
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"文档为空: {full_path}")
                return None
            
            return content
        
        except UnicodeDecodeError:
            logger.warning(f"文档编码错误: {full_path}")
            return None
        except Exception as e:
            logger.error(f"读取文档失败 {full_path}: {e}")
            return None
    
    def get_stats(self) -> Dict:
        """获取文档统计信息"""
        nav_tree = self.extract_nav_tree()
        
        categories = {}
        for item in nav_tree:
            cat = item["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_documents": len(nav_tree),
            "categories": categories
        }


if __name__ == "__main__":
    indexer = MkdocsIndexer()
    nav_tree = indexer.extract_nav_tree()
    stats = indexer.get_stats()
    
    print(f"文档总数: {stats['total_documents']}")
    print("类别分布:")
    for cat, count in stats["categories"].items():
        print(f"  - {cat}: {count}")
