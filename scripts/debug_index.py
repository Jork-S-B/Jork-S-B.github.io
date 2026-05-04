"""
debug_index.py - 索引调试工具

检查索引内容，排查检索问题。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag_engine import LightweightRAG


def main():
    rag = LightweightRAG()
    
    if not rag.load_index():
        print("索引不存在，请先运行: python scripts/build_index.py")
        return
    
    stats = rag.get_stats()
    print("=" * 60)
    print("索引统计信息")
    print("=" * 60)
    print(f"总分块数: {stats['total_chunks']}")
    print(f"嵌入模型: {stats['model_name']}")
    print("\n类别分布:")
    for cat, count in stats['categories'].items():
        print(f"  - {cat}: {count}")
    
    print("\n" + "=" * 60)
    print("检查 pytest 相关分块")
    print("=" * 60)
    
    pytest_chunks = []
    for i, chunk in enumerate(rag.chunks):
        content = chunk.get("content", "").lower()
        source = chunk.get("metadata", {}).get("source", "")
        
        if "pytest" in source.lower() or "pytest" in content or "fixture" in content:
            pytest_chunks.append((i, chunk))
    
    if pytest_chunks:
        print(f"\n✓ 找到 {len(pytest_chunks)} 个 pytest 相关分块:")
        for idx, chunk in pytest_chunks[:10]:
            meta = chunk.get("metadata", {})
            print(f"\n[{idx}] {meta.get('source', 'unknown')}")
            print(f"    标题: {meta.get('heading', 'N/A')}")
            print(f"    内容长度: {len(chunk.get('content', ''))}")
            print(f"    内容预览: {chunk.get('content', '')[:100]}...")
    else:
        print("\n⚠️ 未找到 pytest 相关分块！")
        print("\n检查所有包含 'autotest' 的分块:")
        
        autotest_chunks = []
        for i, chunk in enumerate(rag.chunks):
            source = chunk.get("metadata", {}).get("source", "")
            if "autotest" in source.lower():
                autotest_chunks.append((i, chunk))
        
        if autotest_chunks:
            print(f"\n找到 {len(autotest_chunks)} 个 autotest 相关分块:")
            for idx, chunk in autotest_chunks[:10]:
                meta = chunk.get("metadata", {})
                print(f"  [{idx}] {meta.get('source', 'unknown')}")
        else:
            print("也未找到 autotest 相关分块！")
    
    print("\n" + "=" * 60)
    print("前 10 个分块预览")
    print("=" * 60)
    
    for i, chunk in enumerate(rag.chunks[:10]):
        meta = chunk.get("metadata", {})
        print(f"\n[{i}] {meta.get('source', 'unknown')}")
        print(f"    标题: {meta.get('heading', 'N/A')}")
        print(f"    内容长度: {len(chunk.get('content', ''))}")
    
    print("\n" + "=" * 60)
    print("测试查询: pytest fixture")
    print("=" * 60)
    
    results = rag.query("pytest fixture", top_k=5)
    
    print(f"\n返回 {len(results)} 个结果:")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r['metadata']['source']}")
        print(f"    标题: {r['metadata'].get('heading', 'N/A')}")
        print(f"    得分: {r['score']:.4f}")
        print(f"    内容预览: {r['content'][:80]}...")
    
    print("\n" + "=" * 60)
    print("检查 BM25 分词效果")
    print("=" * 60)
    
    from text_processor import ChineseTextProcessor
    processor = ChineseTextProcessor()
    
    test_query = "pytest fixture"
    tokens = processor.tokenize(test_query)
    keywords = processor.extract_keywords(test_query)
    bm25_tokens = processor.tokenize_for_bm25(test_query)
    
    print(f"\n查询: {test_query}")
    print(f"分词结果: {tokens}")
    print(f"关键词提取: {keywords}")
    print(f"BM25 分词: {bm25_tokens}")


if __name__ == "__main__":
    main()
