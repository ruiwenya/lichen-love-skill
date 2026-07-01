#!/usr/bin/env python3
"""在李晨文章导出的 HTML 文件中搜索关键词。

示例：
python3 Lichen-LOVE-skill/scripts/search_articles.py --root . --keyword 原生家庭 --keyword 暧昧 --limit 20
python3 Lichen-LOVE-skill/scripts/search_articles.py --root D:\\wx-export --keyword AI --json
"""

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path


def read_text(path):
    data = Path(path).read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "gbk", "big5"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="ignore")


def strip_html(raw):
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def title_from_dir(path):
    parent = Path(path).parent.name
    return parent.replace("_", " ").strip()


def make_snippet(text, keywords, width):
    lowered = text.lower()
    positions = []
    for keyword in keywords:
        pos = lowered.find(keyword.lower())
        if pos >= 0:
            positions.append(pos)
    if not positions:
        return text[:width]
    center = min(positions)
    start = max(0, center - width // 2)
    end = min(len(text), start + width)
    return text[start:end]


def score_text(text, title, keywords):
    score = 0
    title_lower = title.lower()
    text_lower = text.lower()
    for keyword in keywords:
        k = keyword.lower()
        score += title_lower.count(k) * 8
        score += text_lower.count(k)
    return score


def search(root, keywords, limit, snippet_width):
    results = []
    root_path = Path(root).resolve()
    for path in root_path.rglob("index.html"):
        if "Lichen-LOVE-skill" in path.parts and not getattr(search, "include_skill", False):
            continue
        raw = read_text(path)
        text = strip_html(raw)
        title = title_from_dir(path)
        score = score_text(text, title, keywords)
        if score <= 0:
            continue
        rel = path.relative_to(root_path).as_posix()
        results.append(
            {
                "score": score,
                "title": title,
                "path": rel,
                "snippet": make_snippet(text, keywords, snippet_width),
            }
        )
    results.sort(key=lambda item: (-item["score"], item["path"]))
    return results[:limit]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="搜索本地李晨文章 HTML")
    parser.add_argument("--root", default=".", help="文章根目录，默认当前目录")
    parser.add_argument("--keyword", action="append", required=True, help="关键词，可重复传入")
    parser.add_argument("--limit", type=int, default=20, help="最多输出多少篇")
    parser.add_argument("--snippet-width", type=int, default=220, help="摘要字符数")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--include-skill", action="store_true", help="同时搜索 skill 内置原文快照")
    args = parser.parse_args()

    search.include_skill = args.include_skill
    results = search(args.root, args.keyword, args.limit, args.snippet_width)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    for index, item in enumerate(results, 1):
        print(f"{index}. [{item['score']}] {item['title']}")
        print(f"   {item['path']}")
        print(f"   {item['snippet']}")
        print()


if __name__ == "__main__":
    main()
