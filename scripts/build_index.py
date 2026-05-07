"""
build_index.py - 索引构建脚本

一键构建 RAG 索引，包括向量索引和 BM25 索引。
支持增量更新，只处理变更的文档。
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from doc_indexer import MkdocsIndexer
from rag_engine import LightweightRAG


def main():
    parser = argparse.ArgumentParser(description="构建 RAG 索引")
    parser.add_argument(
        "--config",
        default="mkdocs.yml",
        help="mkdocs.yml 配置文件路径"
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="文档目录路径"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="索引存储目录"
    )
    parser.add_argument(
        "--model",
        default="shibing624/text2vec-base-chinese",
        help="嵌入模型名称"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重建索引"
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="增量更新索引（仅处理变更文档）"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RAG 索引构建工具")
    print("=" * 60)
    
    print("\n[1/4] 解析 mkdocs.yml...")
    indexer = MkdocsIndexer(
        config_path=args.config,
        docs_dir=args.docs_dir
    )
    nav_tree = indexer.extract_nav_tree()
    stats = indexer.get_stats()
    
    print(f"  ✓ 找到 {stats['total_documents']} 个文档")
    print("  ✓ 类别分布:")
    for cat, count in stats["categories"].items():
        print(f"      - {cat}: {count}")
    
    print("\n[2/4] 加载文档内容...")
    documents = indexer.load_all_documents(nav_tree)
    print(f"  ✓ 成功加载 {len(documents)} 个文档")
    
    print("\n[3/4] 构建 RAG 索引...")
    print(f"  - 嵌入模型: {args.model}")
    print(f"  - 索引目录: {args.data_dir}")
    
    rag = LightweightRAG(
        model_name=args.model,
        data_dir=args.data_dir
    )
    
    docs_dir = Path(args.docs_dir)
    
    if args.force:
        print("  - 模式: 强制全量重建")
        rag.build_index(documents)
    elif args.incremental:
        print("  - 模式: 增量更新")
        updated = rag.incremental_update(docs_dir, documents)
        if not updated:
            print("  ✓ 文档无变更，跳过索引更新")
    else:
        if rag.load_index():
            print("  - 模式: 增量更新（检测到已有索引）")
            updated = rag.incremental_update(docs_dir, documents)
            if not updated:
                print("  ✓ 文档无变更，跳过索引更新")
        else:
            print("  - 模式: 全量构建（无已有索引）")
            rag.build_index(documents)
    
    print("\n[4/4] 保存索引文件...")
    rag.save_index()
    rag.save_index_state(docs_dir, documents)
    
    index_stats = rag.get_stats()
    print(f"  ✓ 总分块数: {index_stats['total_chunks']}")
    print("  ✓ 分块类别分布:")
    for cat, count in index_stats["categories"].items():
        print(f"      - {cat}: {count}")
    
    print("\n" + "=" * 60)
    print("✓ 索引构建完成!")
    print("=" * 60)
    print(f"\n索引文件已保存到: {args.data_dir}/")
    print("  - faiss_index.bin  (向量索引)")
    print("  - bm25_index.pkl   (BM25 索引)")
    print("  - metadata.json    (元数据)")
    print("  - index_state.json (索引状态)")
    print("\n使用以下命令测试查询:")
    print(f"  python scripts/query.py \"pytest fixture\"")


if __name__ == "__main__":
    main()
