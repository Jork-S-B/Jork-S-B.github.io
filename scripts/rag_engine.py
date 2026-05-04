"""
rag_engine.py - 轻量级 RAG 引擎

实现混合检索（BM25 + 向量），使用 RRF 融合算法。
"""
import os
import re
import json
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

if "HF_ENDPOINT" not in os.environ:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from text_processor import ChineseTextProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LightweightRAG:
    """轻量级 RAG 引擎"""
    
    def __init__(
        self,
        model_name: str = "shibing624/text2vec-base-chinese",
        data_dir: str = "data"
    ):
        self.model_name = model_name
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.model = None
        self.text_processor = ChineseTextProcessor()
        
        self.vector_index = None
        self.bm25_index = None
        self.chunks = []
        self.metadata = []
    
    def _load_model(self) -> None:
        """延迟加载嵌入模型"""
        if self.model is None:
            logger.info(f"加载嵌入模型: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("模型加载完成")
    
    def build_index(self, documents: List[Dict]) -> None:
        """构建混合索引（向量 + BM25）"""
        self._load_model()
        
        logger.info("开始构建索引...")
        
        self.chunks = self._split_by_markdown(documents)
        logger.info(f"文档分块完成: {len(self.chunks)} 个分块")
        
        texts = [chunk["content"] for chunk in self.chunks]
        
        logger.info("构建向量索引...")
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(embeddings)
        self.vector_index.add(embeddings.astype('float32'))
        logger.info(f"向量索引构建完成: {dimension} 维")
        
        logger.info("构建 BM25 索引...")
        tokenized = [self.text_processor.tokenize_for_bm25(text) for text in texts]
        self.bm25_index = BM25Okapi(tokenized)
        logger.info("BM25 索引构建完成")
        
        self.metadata = [chunk.get("metadata", {}) for chunk in self.chunks]
        
        logger.info("索引构建完成")
    
    def query(
        self,
        question: str,
        top_k: int = 3,
        category: Optional[str] = None
    ) -> List[Dict]:
        """混合检索：BM25 + 向量，RRF 融合"""
        if not self.chunks:
            logger.warning("索引为空，请先构建索引")
            return []
        
        self._load_model()
        
        keywords = self.text_processor.extract_keywords(question)
        query_text = " ".join(keywords) if keywords else question
        
        bm25_scores = self._bm25_search(query_text)
        vector_scores = self._vector_search(question)
        
        combined_scores = self._rrf_fusion(
            bm25_scores, 
            vector_scores, 
            bm25_weight=2.0,
            vector_weight=1.0
        )
        
        if category:
            combined_scores = self._filter_by_category(combined_scores, category)
        
        return self._format_results(combined_scores, top_k)
    
    def _split_by_markdown(self, documents: List[Dict]) -> List[Dict]:
        """按 Markdown 标题层级分块，支持多种分块策略"""
        chunks = []
        
        for doc in documents:
            content = doc.get("content", "")
            
            sections = self._smart_split(content, doc.get("title", ""))
            
            for section in sections:
                text = section["text"].strip()
                if len(text) < 50:
                    continue
                
                chunks.append({
                    "content": text,
                    "metadata": {
                        "source": doc["path"],
                        "category": doc["category"],
                        "heading": section["heading"],
                        "parent": doc.get("parent", ""),
                        "title": doc["title"]
                    }
                })
        
        return chunks
    
    def _smart_split(self, content: str, doc_title: str = "") -> List[Dict]:
        """智能分块：优先标题分块，fallback 到段落分块"""
        sections = self._split_by_headings(content, doc_title)
        
        if len(sections) <= 1:
            sections = self._split_by_paragraphs(content, doc_title)
        
        final_sections = []
        for section in sections:
            text = section["text"]
            if len(text) > 1000:
                sub_sections = self._split_by_length(text, section["heading"])
                final_sections.extend(sub_sections)
            else:
                final_sections.append(section)
        
        return final_sections if final_sections else [{"heading": doc_title, "text": content}]
    
    def _split_by_headings(self, content: str, doc_title: str = "") -> List[Dict]:
        """按标题分割内容，支持任意层级标题"""
        sections = []
        heading_stack = []
        current_content = []
        
        lines = content.split("\n")
        
        for line in lines:
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if heading_match:
                if current_content:
                    text = "\n".join(current_content).strip()
                    if text:
                        heading_path = " > ".join(heading_stack) if heading_stack else doc_title
                        sections.append({
                            "heading": heading_path,
                            "text": text
                        })
                
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                while len(heading_stack) >= level:
                    heading_stack.pop()
                
                heading_stack.append(title)
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            text = "\n".join(current_content).strip()
            if text:
                heading_path = " > ".join(heading_stack) if heading_stack else doc_title
                sections.append({
                    "heading": heading_path,
                    "text": text
                })
        
        return sections
    
    def _split_by_paragraphs(self, content: str, doc_title: str = "") -> List[Dict]:
        """按段落分割内容，保持代码块完整性"""
        sections = []
        current_para = []
        in_code_block = False
        
        lines = content.split("\n")
        
        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                current_para.append(line)
            elif line.strip() == "" and not in_code_block:
                if current_para:
                    text = "\n".join(current_para).strip()
                    if text:
                        sections.append({
                            "heading": doc_title,
                            "text": text
                        })
                    current_para = []
            else:
                current_para.append(line)
        
        if current_para:
            text = "\n".join(current_para).strip()
            if text:
                sections.append({
                    "heading": doc_title,
                    "text": text
                })
        
        return sections
    
    def _split_by_length(self, text: str, heading: str, max_length: int = 800) -> List[Dict]:
        """按固定长度分割，使用滑动窗口保持语义完整"""
        sections = []
        
        if len(text) <= max_length:
            return [{"heading": heading, "text": text}]
        
        sentences = re.split(r'([。！？\n])', text)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        sentences = [s for s in sentences if s.strip()]
        
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sent_len = len(sentence)
            
            if current_length + sent_len > max_length and current_chunk:
                sections.append({
                    "heading": heading,
                    "text": "".join(current_chunk)
                })
                current_chunk = [sentence]
                current_length = sent_len
            else:
                current_chunk.append(sentence)
                current_length += sent_len
        
        if current_chunk:
            sections.append({
                "heading": heading,
                "text": "".join(current_chunk)
            })
        
        return sections
    
    def _bm25_search(self, query: str) -> np.ndarray:
        """BM25 检索"""
        tokens = self.text_processor.tokenize_for_bm25(query)
        scores = self.bm25_index.get_scores(tokens)
        return np.array(scores)
    
    def _vector_search(self, query: str) -> np.ndarray:
        """向量检索"""
        self._load_model()
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        scores, _ = self.vector_index.search(query_embedding.astype('float32'), len(self.chunks))
        return scores[0]
    
    def _rrf_fusion(
        self,
        bm25_scores: np.ndarray,
        vector_scores: np.ndarray,
        k: int = 60,
        bm25_weight: float = 2.0,
        vector_weight: float = 1.0
    ) -> np.ndarray:
        """
        加权 RRF 融合算法
        
        Args:
            bm25_scores: BM25 得分
            vector_scores: 向量得分
            k: RRF 平滑参数
            bm25_weight: BM25 权重（默认 2.0，对技术文档关键词匹配更重要）
            vector_weight: 向量权重（默认 1.0）
        """
        rrf_scores = np.zeros(len(bm25_scores))
        
        bm25_ranks = np.argsort(-bm25_scores)
        for rank, idx in enumerate(bm25_ranks):
            rrf_scores[idx] += bm25_weight / (k + rank + 1)
        
        vector_ranks = np.argsort(-vector_scores)
        for rank, idx in enumerate(vector_ranks):
            rrf_scores[idx] += vector_weight / (k + rank + 1)
        
        return rrf_scores
    
    def _filter_by_category(self, scores: np.ndarray, category: str) -> np.ndarray:
        """按类别过滤"""
        filtered_scores = scores.copy()
        
        for i, meta in enumerate(self.metadata):
            if meta.get("category") != category:
                filtered_scores[i] = -np.inf
        
        return filtered_scores
    
    def _format_results(self, scores: np.ndarray, top_k: int) -> List[Dict]:
        """格式化检索结果"""
        top_indices = np.argsort(-scores)[:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] == -np.inf:
                continue
            
            results.append({
                "content": self.chunks[idx]["content"],
                "metadata": self.metadata[idx],
                "score": float(scores[idx])
            })
        
        return results
    
    def save_index(self, path: Optional[str] = None) -> None:
        """保存索引到文件"""
        if path:
            save_dir = Path(path)
        else:
            save_dir = self.data_dir
        
        save_dir.mkdir(exist_ok=True, parents=True)
        
        faiss.write_index(self.vector_index, str(save_dir / "faiss_index.bin"))
        
        with open(save_dir / "bm25_index.pkl", "wb") as f:
            pickle.dump(self.bm25_index, f)
        
        with open(save_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump({
                "chunks": self.chunks,
                "metadata": self.metadata,
                "model_name": self.model_name
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"索引已保存到: {save_dir}")
    
    def load_index(self, path: Optional[str] = None) -> bool:
        """从文件加载索引"""
        if path:
            load_dir = Path(path)
        else:
            load_dir = self.data_dir
        
        faiss_path = load_dir / "faiss_index.bin"
        bm25_path = load_dir / "bm25_index.pkl"
        meta_path = load_dir / "metadata.json"
        
        if not all(p.exists() for p in [faiss_path, bm25_path, meta_path]):
            logger.warning("索引文件不完整，需要重新构建")
            return False
        
        try:
            self.vector_index = faiss.read_index(str(faiss_path))
            
            with open(bm25_path, "rb") as f:
                self.bm25_index = pickle.load(f)
            
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.chunks = data["chunks"]
                self.metadata = data["metadata"]
                self.model_name = data.get("model_name", self.model_name)
            
            logger.info(f"索引已加载: {len(self.chunks)} 个分块")
            return True
        
        except Exception as e:
            logger.error(f"加载索引失败: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """获取索引统计信息"""
        if not self.chunks:
            return {"status": "empty"}
        
        categories = {}
        for meta in self.metadata:
            cat = meta.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "status": "ready",
            "total_chunks": len(self.chunks),
            "categories": categories,
            "model_name": self.model_name
        }


if __name__ == "__main__":
    from doc_indexer import MkdocsIndexer
    
    indexer = MkdocsIndexer()
    nav_tree = indexer.extract_nav_tree()
    documents = indexer.load_all_documents(nav_tree)
    
    rag = LightweightRAG()
    rag.build_index(documents)
    rag.save_index()
    
    print("\n测试查询:")
    results = rag.query("pytest fixture 怎么用", top_k=3)
    
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r['metadata']['source']}")
        print(f"    标题: {r['metadata']['heading']}")
        print(f"    得分: {r['score']:.4f}")
        print(f"    摘要: {r['content'][:100]}...")
