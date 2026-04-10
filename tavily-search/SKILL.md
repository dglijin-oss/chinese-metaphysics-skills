---
name: tavily-search
description: 使用 Tavily API 进行智能网络搜索，返回高质量的搜索结果和答案。
version: 1.0.0
author: 天工长老
---

# Tavily 搜索技能

## 1. Description

使用 Tavily AI 的智能搜索 API，返回高质量、经过验证的网络搜索结果。适合需要准确信息的研究、事实核查、新闻查询等场景。

**核心功能：**
- 智能搜索（AI 优化结果）
- 答案生成（直接回答问题）
- 结果评分（相关性排序）
- 可选深度搜索模式

---

## 2. When to use

| 场景 | 示例 |
|------|------|
| 事实核查 | "2026 年奥运会在哪里举办？" |
| 新闻查询 | "最新的 AI 技术突破有哪些？" |
| 研究调研 | "量子计算的最新进展" |
| 产品对比 | "iPhone 16 和 Samsung S25 对比" |
| 深度研究 | "气候变化对经济的影响分析" |

---

## 3. How to use

### 调用方式

```bash
# 基础搜索
python3 ~/.openclaw/skills/tavily-search/scripts/tavily_search.py --query "AI 技术最新进展"

# 深度搜索（更多结果）
python3 ~/.openclaw/skills/tavily-search/scripts/tavily_search.py --query "量子计算" --search-depth "advanced"

# 指定结果数量
python3 ~/.openclaw/skills/tavily-search/scripts/tavily_search.py --query "气候变化" --max-results 10

# 包含答案生成
python3 ~/.openclaw/skills/tavily-search/scripts/tavily_search.py --query "2026 年世界杯" --include-answer

# JSON 输出
python3 ~/.openclaw/skills/tavily-search/scripts/tavily_search.py --query "测试" --json
```

### 执行步骤

1. **提取搜索关键词** — 从用户消息中提取核心问题
2. **调用搜索脚本** — 使用 Tavily API 获取结果
3. **返回格式化结果** — 按标准格式输出

---

## 4. Output Format

```
【搜索结果】
查询：{query}
响应时间：{time}s

【答案】
{直接回答（如有）}

【结果列表】
1. {标题}
   链接：{URL}
   摘要：{内容摘要}
   相关性：{score}

2. ...
```

---

## 5. Edge cases

| 情况 | 处理方式 |
|------|----------|
| 搜索无结果 | 告知用户未找到相关信息，建议更换关键词 |
| API 限流 | 等待后重试，或建议使用其他搜索方式 |
| 敏感话题 | 按 API 返回结果处理，不做额外过滤 |
| 网络错误 | 提示用户检查网络连接 |

---

## 6. Dependencies

| 依赖 | 用途 | 版本 |
|------|------|------|
| Python 3.8+ | 运行环境 | 必需 |
| requests | HTTP 请求 | 必需 |

### 安装依赖

```bash
pip3 install requests
```

---

## 7. API Reference

### Tavily API

| 端点 | 说明 |
|------|------|
| `https://api.tavily.com/search` | 搜索端点 |
| `Authorization: Bearer {API_KEY}` | 认证头 |

### 请求参数

```json
{
  "query": "搜索关键词",
  "search_depth": "basic|advanced",
  "include_answer": true,
  "max_results": 5
}
```

### 响应格式

```json
{
  "query": "搜索关键词",
  "response_time": 1.2,
  "answer": "直接答案（如有）",
  "results": [
    {
      "url": "https://...",
      "title": "标题",
      "content": "摘要内容",
      "score": 0.99
    }
  ]
}
```

---

## 8. 配置

### 环境变量

**API 密钥位置：** `/home/node/.openclaw/.env`

```bash
TAVILY_API_KEY=tvly-xxx
```

### 搜索深度

| 模式 | 说明 | 结果数 |
|------|------|--------|
| basic | 基础搜索，快速 | 5 条 |
| advanced | 深度搜索，全面 | 10-20 条 |

---

## 9. 示例

### 示例 1：事实查询

**用户输入：**
> "2026 年世界杯在哪里举办？"

**技能输出：**
```
【搜索结果】
查询：2026 年世界杯在哪里举办
响应时间：1.5s

【答案】
2026 年 FIFA 世界杯将由美国、加拿大和墨西哥联合举办。

【结果列表】
1. FIFA World Cup 2026 - Official Site
   链接：https://www.fifa.com/worldcup/2026
   摘要：Official information about the 2026 FIFA World Cup...
   相关性：0.98

2. 2026 World Cup Host Countries
   链接：https://www.espn.com/soccer/...
   摘要：The 2026 World Cup will be hosted by USA, Canada, and Mexico...
   相关性：0.95
```

### 示例 2：技术研究

**用户输入：**
> "量子计算的最新突破"

**技能输出：**
```
【搜索结果】
查询：量子计算的最新突破
响应时间：2.1s

【答案】
2026 年量子计算领域的主要突破包括...

【结果列表】
1. Quantum Computing Breakthrough 2026
   链接：https://www.nature.com/articles/...
   摘要：Researchers achieve new milestone in quantum error correction...
   相关性：0.97

2. ...
```

---

## 10. 注意事项

1. **API 配额** — 开发版 API 有月度配额限制，请注意使用频率
2. **结果时效性** — 搜索结果基于最新网络内容，但可能有延迟
3. **语言支持** — 支持多语言搜索，中文查询效果良好
4. **敏感内容** — 某些敏感话题可能返回有限结果

---

> **天工长老按：** 此技能乃获取外部信息之利器，配合奇门解卦，可断天下之事。

🏮 天工长老 敬撰
