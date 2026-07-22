#!/usr/bin/env python3
"""把核心李晨文章目录复制到 skill 的资料库中。

用途：
- 让没有完整本地文章库的 AI 也能读取少量核心原文快照。
- 让资料库可以从新的 `D:\\wx-export` 或其他导出目录重复生成。

注意：
- 默认不复制明确付费、私密截图或用户个人对话资料。
- 如果准备公开发布到 GitHub，请先确认这些原文快照的版权和传播权限。
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


ARTICLES = [
    {"pattern": "2014-01-21_*", "note": "主流教育的好处：敢斗敢胜、精神快乐、情感丰富"},
    {"pattern": "2014-03-08_*", "note": "女生如何克服不安全感：父母生活状态、恐怖气氛、判逆"},
    {"pattern": "2014-03-11_*", "note": "一种独生子女的教育方法：规矩、心计、事理、少讲道德"},
    {"pattern": "2014-04-04_*", "note": "为什么说90后是保守、单一、僵化的"},
    {"pattern": "2015-04-12_*", "note": "不识人是少了江湖文化"},
    {"pattern": "2025-11-14_*", "note": "都没往留她过夜方面想：亲密深入与正向心理空间"},
    {"pattern": "2026-06-01_吃喝玩乐*", "note": "吃喝玩乐从早餐开始"},
    {"pattern": "2026-06-05_*", "note": "暧昧是疲惫生活的解药"},
    {"pattern": "2026-06-09_*", "note": "暧昧的艺术性与美感"},
    {"pattern": "2026-06-16_使用AI看电影*", "note": "使用AI看电影：以双重赔偿为例"},
    {"pattern": "2026-06-20_研究亲密关系*", "note": "研究亲密关系的顶级专家真的会亲密吗"},
    {"pattern": "2026-06-20_男朋友不带我进他的社交圈*", "note": "男朋友不带我进他的社交圈是为什么"},
    {"pattern": "2026-06-22_*", "note": "性能力的心理因素"},
    {"pattern": "2026-02-27_*", "note": "为什么父母压迫会使孩子失去性欲"},
    {"pattern": "2026-06-23_*", "note": "认命活该爽一把：解决屡分屡做"},
    {"pattern": "2026-06-24_*", "note": "我想把第一次留给未来的老公一起探索"},
    {"pattern": "2026-06-29_*", "note": "女朋友突然无端发作是咋回事"},
    {"pattern": "2026-06-30_*", "note": "恋爱一年后突然失去了性欲：AI纠偏与具体人分析"},
    {"pattern": "2026-07-01_谈恋爱干什么*", "note": "谈恋爱干什么：身体觉醒、亲密抗拒与自然过渡"},
    {"pattern": "2026-07-10__骑脖子洗脚*", "note": "极端宠溺、特殊心理兴奋与AI双向迎合"},
    {"pattern": "2026-07-11_两个女生*", "note": "具体细节、爱与刺激的区别"},
    {"pattern": "2026-07-13_亲热中的假性快乐*", "note": "事后能量、真实快乐与充分快乐"},
    {"pattern": "2026-07-22_哈哈哈哈哈*", "note": "喜报：具体异性、身体欲望、事后日常与生命力"},
    {"pattern": "2026-06-12_*", "note": "雍正皇帝讲读"},
    {"pattern": "2026-06-17__拿捏*", "note": "拿捏的绝技：以海上花为例"},
    {"pattern": "2026-06-19_*", "note": "心性、思谋、手段、大义、气度"},
]


def folder_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def copy_snapshots(root: Path, skill_dir: Path) -> list[dict]:
    dest_root = skill_dir / "references" / "文章资料库" / "原文快照"
    dest_root.mkdir(parents=True, exist_ok=True)

    manifest = []
    for article in ARTICLES:
        matches = [
            item
            for item in root.glob(article["pattern"])
            if item.is_dir() and item.name != skill_dir.name
        ]
        if not matches:
            manifest.append({**article, "status": "missing"})
            continue

        source = sorted(matches, key=lambda item: item.name)[0]
        dest = dest_root / source.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(
            source,
            dest,
            ignore=shutil.ignore_patterns("__analysis*", "__pycache__"),
        )
        manifest.append(
            {
                **article,
                "status": "copied",
                "source": source.name,
                "snapshot": dest.relative_to(skill_dir).as_posix(),
                "bytes": folder_size(dest),
            }
        )

    manifest_path = dest_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="复制核心文章快照到 skill references")
    parser.add_argument("--root", default=".", help="李晨文章导出根目录")
    parser.add_argument("--skill-dir", default="Lichen-LOVE-skill", help="skill 目录")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_dir = (root / args.skill_dir).resolve()
    manifest = copy_snapshots(root, skill_dir)
    for item in manifest:
        print(f"{item['status']}: {item['note']} -> {item.get('snapshot', item['pattern'])}")


if __name__ == "__main__":
    main()
