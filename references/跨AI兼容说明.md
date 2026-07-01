# 跨 AI 兼容说明

## 使用目标

这个 skill 要能给 Codex、Claude、Kimi、Gemini、通义、DeepSeek 等不同 AI 使用。不同 AI 不一定支持 Codex 的 skill 机制，所以所有关键资料都写成普通 Markdown，方便复制或上传。

## 两种使用模式

### 模式一：无本地 HTML

当 AI 不能访问 `D:\wx-export` 或没有李晨文章原文时，使用以下文件：

- `SKILL.md`
- `references/李晨式分析方法.md`
- `references/单点问题处理指南.md`
- `references/文章资料库/索引.md`
- 按问题选择 `references/文章资料库/` 下的专题文件
- 如需原文证据，读取 `references/文章资料库/原文快照/` 下的对应文章
- 必要时读 `references/输出模板与案例.md`

此时回答应区分资料来源：如果读取了 `原文快照/`，可以说依据来自内置原文快照；如果只读了专题 Markdown，则说明依据来自资料库摘要。

### 模式二：有本地 HTML

当 AI 能访问本地文章时，优先搜索和阅读原文。完整文章可以由用户从 `down.mptext.top` 自行导出到本地：

```bash
python3 Lichen-LOVE-skill/scripts/search_articles.py --root . --keyword "分析人" --keyword "原生家庭" --limit 20
```

没有完整文章库、只搜 skill 内置快照时：

```bash
python3 Lichen-LOVE-skill/scripts/search_articles.py --root Lichen-LOVE-skill --keyword "分析人" --include-skill --limit 20
```

如果文章包含长图或截图，需要读取正文图片。遇到明显广告、课程报名、二维码、推广图，可以跳过。

公开仓库默认不上传完整 HTML 和图片；需要高可信原文证据时，由使用者在本机导出文章并运行 `scripts/refresh_article_snapshots.py`。

本地原文优先级高于资料库摘要。若摘要和原文不一致，以原文为准。

## 给其他 AI 的启动提示词

可以直接复制：

```text
请使用 lichen-love-skill 的思路分析这个问题。先读 SKILL.md，再按问题选择 references 中的资料。回答时不要停在默认温和 AI 建议，要按照“直判断、拆人、验人、做事”的结构，重点分析家庭训练、心理兴奋机制、权力位置、欲望结构、道德与人性的冲突。不要引用用户私人经历作为示例。
```

如果用户只给了一个单点问题：

```text
请使用 lichen-love-skill 分析这个单点情感问题。先读 references/单点问题处理指南.md，再按问题类型选择资料。信息不足时不要只要求补充背景，而是先给可验证的强假设、验证动作和下一步操作。
```

如果有本地 HTML：

```text
本地有李晨文章 HTML。请先用 scripts/search_articles.py 搜索关键词，打开相关文章和正文图片，再结合 skill 的 references 输出分析。没有读到原文时，不要假装已经读过。
```

## 风格要求

- 中文输出。
- 直接、具体、有力度。
- 不要像心理咨询科普文。
- 不要只讲边界、尊重、沟通、稳定。
- 可以提出刺耳但可验证的判断。
- 不要鼓励欺骗、胁迫、越过同意或恶意操控。

## 与普通 PUA 内容的区别

这个 skill 的重点不是套路别人，而是看懂人和训练自己。

可以分析拿捏、权力、兴奋、欲望，但最终要落到：

- 用户是否更清醒。
- 用户是否更有生命力。
- 用户是否能承担自己的选择。
- 用户是否能减少拖泥带水和自欺欺人。
