"""
debug_retrieval.py - 检索算法调试工具

详细检查向量检索和 BM25 检索的单独结果。
"""
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag_engine import LightweightRAG


def main():
    rag = LightweightRAG()
    
    if not rag.load_index():
        print("索引不存在，请先运行: python scripts/build_index.py")
        return
    
    query = "pytest fixture"
    
    print("=" * 60)
    print(f"查询: {query}")
    print("=" * 60)
    
    print("\n[1] BM25 检索结果:")
    bm25_scores = rag._bm25_search(query)
    bm25_top_indices = np.argsort(-bm25_scores)[:10]
    
    for rank, idx in enumerate(bm25_top_indices, 1):
        score = bm25_scores[idx]
        meta = rag.metadata[idx]
        print(f"\n  [{rank}] {meta['source']}")
        print(f"      标题: {meta.get('heading', 'N/A')}")
        print(f"      BM25 得分: {score:.4f}")
        print(f"      内容预览: {rag.chunks[idx]['content'][:60]}...")
    
    print("\n" + "=" * 60)
    print("[2] 向量检索结果:")
    vector_scores = rag._vector_search(query)
    vector_top_indices = np.argsort(-vector_scores)[:10]
    
    for rank, idx in enumerate(vector_top_indices, 1):
        score = vector_scores[idx]
        meta = rag.metadata[idx]
        print(f"\n  [{rank}] {meta['source']}")
        print(f"      标题: {meta.get('heading', 'N/A')}")
        print(f"      向量得分: {score:.4f}")
        print(f"      内容预览: {rag.chunks[idx]['content'][:60]}...")
    
    print("\n" + "=" * 60)
    print("[3] RRF 融合结果 (BM25权重=2.0):")
    combined_scores = rag._rrf_fusion(bm25_scores, vector_scores, bm25_weight=2.0, vector_weight=1.0)
    combined_top_indices = np.argsort(-combined_scores)[:10]
    
    for rank, idx in enumerate(combined_top_indices, 1):
        score = combined_scores[idx]
        meta = rag.metadata[idx]
        print(f"\n  [{rank}] {meta['source']}")
        print(f"      标题: {meta.get('heading', 'N/A')}")
        print(f"      RRF 得分: {score:.4f}")
        print(f"      BM25 排名: {np.where(bm25_top_indices == idx)[0][0] + 1 if idx in bm25_top_indices else 'N/A'}")
        print(f"      向量排名: {np.where(vector_top_indices == idx)[0][0] + 1 if idx in vector_top_indices else 'N/A'}")
    
    print("\n" + "=" * 60)
    print("[4] pytest 分块的得分:")
    pytest_indices = []
    for i, meta in enumerate(rag.metadata):
        if "pytest" in meta.get("source", "").lower():
            pytest_indices.append(i)
    
    print(f"\n找到 {len(pytest_indices)} 个 pytest 分块:")
    for idx in pytest_indices[:5]:
        meta = rag.metadata[idx]
        bm25_rank = np.where(np.argsort(-bm25_scores) == idx)[0][0] + 1
        vector_rank = np.where(np.argsort(-vector_scores) == idx)[0][0] + 1
        combined_rank = np.where(np.argsort(-combined_scores) == idx)[0][0] + 1
        
        print(f"\n  [{idx}] {meta['source']}")
        print(f"      标题: {meta.get('heading', 'N/A')}")
        print(f"      BM25 排名: {bm25_rank}/{len(bm25_scores)}")
        print(f"      向量排名: {vector_rank}/{len(vector_scores)}")
        print(f"      RRF 排名: {combined_rank}/{len(combined_scores)}")


if __name__ == "__main__":
    main()
