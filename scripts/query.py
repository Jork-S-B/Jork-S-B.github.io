"""
query.py - 命令行查询工具

提供友好的命令行界面，用于查询 RAG 知识库。
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag_engine import LightweightRAG


def format_result(result: dict, index: int) -> str:
    """格式化单个检索结果"""
    lines = []
    
    lines.append(f"\n[{index}] {result['metadata']['source']}")
    
    heading = result['metadata'].get('heading', '')
    if heading:
        lines.append(f"    标题: {heading}")
    
    parent = result['metadata'].get('parent', '')
    if parent:
        lines.append(f"    分类: {parent}")
    
    lines.append(f"    得分: {result['score']:.4f}")
    
    content = result['content']
    summary = content[:150].replace('\n', ' ').strip()
    if len(content) > 150:
        summary += "..."
    lines.append(f"    摘要: {summary}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="RAG 知识库查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/query.py "pytest fixture"
  python scripts/query.py "pytest fixture" --category technical
  python scripts/query.py "炒股策略" --top-k 5
  python scripts/query.py --rebuild
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="查询内容"
    )
    parser.add_argument(
        "--category",
        choices=["technical", "stock", "personal", "learning", "all"],
        default="all",
        help="文档类别过滤"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="返回结果数量（默认: 3）"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="索引存储目录"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="重建索引"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="显示索引统计信息"
    )
    
    args = parser.parse_args()
    
    if args.stats:
        rag = LightweightRAG(data_dir=args.data_dir)
        if rag.load_index():
            stats = rag.get_stats()
            print("索引统计信息:")
            print(f"  状态: {stats['status']}")
            print(f"  总分块数: {stats['total_chunks']}")
            print(f"  嵌入模型: {stats['model_name']}")
            print("  类别分布:")
            for cat, count in stats['categories'].items():
                print(f"    - {cat}: {count}")
        else:
            print("索引不存在，请先运行: python scripts/build_index.py")
        return
    
    if args.rebuild:
        print("重建索引...")
        from build_index import main as build_main
        sys.argv = ["build_index.py"]
        build_main()
        print("\n索引重建完成，请重新运行查询")
        return
    
    if not args.query:
        parser.print_help()
        return
    
    rag = LightweightRAG(data_dir=args.data_dir)
    
    if not rag.load_index():
        print("索引不存在，正在构建...")
        from build_index import main as build_main
        sys.argv = ["build_index.py"]
        build_main()
        print("\n索引构建完成，正在查询...")
        rag.load_index()
    
    print("=" * 60)
    print(f"查询: {args.query}")
    if args.category != "all":
        print(f"类别: {args.category}")
    print("=" * 60)
    
    category = None if args.category == "all" else args.category
    results = rag.query(args.query, top_k=args.top_k, category=category)
    
    if not results:
        print("\n未找到相关结果")
        return
    
    print(f"\n找到 {len(results)} 个相关结果:")
    
    for i, result in enumerate(results, 1):
        print(format_result(result, i))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
