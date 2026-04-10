#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily 智能搜索工具
天工长老开发 v1.0.0

功能：使用 Tavily API 进行智能网络搜索
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Dict, List, Optional

# ============== 配置 ==============

# API 密钥（从环境变量读取）
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')

# API 端点
API_ENDPOINT = 'https://api.tavily.com/search'

# 默认参数
DEFAULT_MAX_RESULTS = 5
DEFAULT_SEARCH_DEPTH = 'basic'


# ============== Tavily 搜索 ==============

class TavilySearch:
    """Tavily 搜索类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化 Tavily 搜索
        
        参数：
            api_key: Tavily API 密钥，如不传则从环境变量读取
        """
        self.api_key = api_key or TAVILY_API_KEY
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY 未配置，请在 /home/node/.openclaw/.env 中设置")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def search(
        self,
        query: str,
        search_depth: str = 'basic',
        max_results: int = DEFAULT_MAX_RESULTS,
        include_answer: bool = False,
        include_domains: List[str] = None,
        exclude_domains: List[str] = None
    ) -> Dict:
        """
        执行 Tavily 搜索
        
        参数：
            query: 搜索关键词
            search_depth: 搜索深度（basic/advanced）
            max_results: 最大结果数
            include_answer: 是否包含 AI 生成的答案
            include_domains: 只搜索指定域名
            exclude_domains: 排除指定域名
        
        返回：
            搜索结果字典
        """
        payload = {
            'query': query,
            'search_depth': search_depth,
            'max_results': max_results,
            'include_answer': include_answer
        }
        
        if include_domains:
            payload['include_domains'] = include_domains
        
        if exclude_domains:
            payload['exclude_domains'] = exclude_domains
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                API_ENDPOINT,
                data=data,
                headers=self.headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
            
        except urllib.error.URLError as e:
            return {
                'error': str(e.reason),
                'query': query
            }
        except Exception as e:
            return {
                'error': str(e),
                'query': query
            }
    
    def get_news(
        self,
        query: str,
        max_results: int = 5,
        days: int = 7
    ) -> Dict:
        """
        搜索新闻
        
        参数：
            query: 搜索关键词
            max_results: 最大结果数
            days: 最近 N 天的新闻
        
        返回：
            新闻搜索结果
        """
        payload = {
            'query': query,
            'topic': 'news',
            'time_range': f'{days}d',
            'max_results': max_results
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                API_ENDPOINT,
                data=data,
                headers=self.headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
            
        except urllib.error.URLError as e:
            return {
                'error': str(e.reason),
                'query': query
            }
        except Exception as e:
            return {
                'error': str(e),
                'query': query
            }


# ============== 格式化输出 ==============

def format_output(result: Dict) -> str:
    """格式化搜索结果输出"""
    output = []
    
    # 错误处理
    if 'error' in result:
        return f"搜索错误：{result['error']}"
    
    # 基本信息
    output.append("【搜索结果】")
    output.append(f"查询：{result.get('query', '未知')}")
    output.append(f"响应时间：{result.get('response_time', 'N/A')}s")
    output.append("")
    
    # 答案（如有）
    if result.get('answer'):
        output.append("【答案】")
        output.append(result['answer'])
        output.append("")
    
    # 结果列表
    results = result.get('results', [])
    if results:
        output.append("【结果列表】")
        for i, r in enumerate(results, 1):
            output.append(f"{i}. {r.get('title', '无标题')}")
            output.append(f"   链接：{r.get('url', 'N/A')}")
            content = r.get('content', '')
            if content:
                # 截断过长的内容
                if len(content) > 200:
                    content = content[:200] + '...'
                output.append(f"   摘要：{content}")
            score = r.get('score', 0)
            output.append(f"   相关性：{score:.2%}")
            output.append("")
    else:
        output.append("【结果列表】")
        output.append("未找到相关结果")
    
    return "\n".join(output)


def format_compact(result: Dict) -> str:
    """简洁格式输出"""
    output = []
    
    if 'error' in result:
        return f"搜索错误：{result['error']}"
    
    # 答案（如有）
    if result.get('answer'):
        output.append(f"💡 {result['answer']}")
        output.append("")
    
    # 结果列表
    results = result.get('results', [])
    if results:
        output.append("📌 搜索结果：")
        for i, r in enumerate(results, 1):
            title = r.get('title', '无标题')
            url = r.get('url', '')
            output.append(f"{i}. **{title}**")
            output.append(f"   <{url}>")
    
    return "\n".join(output)


# ============== 主函数 ==============

def main():
    parser = argparse.ArgumentParser(description='Tavily 智能搜索工具')
    parser.add_argument('--query', '-q', type=str, required=True, help='搜索关键词')
    parser.add_argument('--depth', '-d', type=str, choices=['basic', 'advanced'], 
                        default='basic', help='搜索深度（default: basic）')
    parser.add_argument('--max-results', '-m', type=int, default=5, 
                        help='最大结果数（default: 5）')
    parser.add_argument('--answer', '-a', action='store_true', 
                        help='包含 AI 生成的答案')
    parser.add_argument('--news', '-n', action='store_true', 
                        help='搜索新闻')
    parser.add_argument('--days', type=int, default=7, 
                        help='新闻时间范围（天，default: 7）')
    parser.add_argument('--json', '-j', action='store_true', 
                        help='输出 JSON 格式')
    parser.add_argument('--compact', '-c', action='store_true', 
                        help='简洁格式输出')
    
    args = parser.parse_args()
    
    try:
        search = TavilySearch()
        
        if args.news:
            # 新闻搜索
            result = search.get_news(
                query=args.query,
                max_results=args.max_results,
                days=args.days
            )
        else:
            # 普通搜索
            result = search.search(
                query=args.query,
                search_depth=args.depth,
                max_results=args.max_results,
                include_answer=args.answer
            )
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.compact:
            print(format_compact(result))
        else:
            print(format_output(result))
            
    except Exception as e:
        print(f"搜索错误：{e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
