#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七政四余流年推演测试脚本
天工长老开发 - Self-Evolve 进化实验 #4 验证
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from liu_nian_enhancer import validate_liu_nian

def main():
    """运行流年推演验证测试"""
    print("=" * 50)
    print("七政四余流年推演验证测试")
    print("=" * 50)
    
    result = validate_liu_nian()
    
    print(f"\n📊 测试统计:")
    print(f"• 流年准确度: {result['liu_nian_accuracy']}%")
    print(f"• 大限准确度: {result['da_xian_accuracy']}%")
    print(f"• 小限准确度: {result['xiao_xian_accuracy']}%")
    print(f"• 通过案例: {result['test_cases_passed']}/{result['test_cases_total']}")
    
    print(f"\n📋 详细结果:")
    for detail in result['details']:
        da_xian_status = "✅" if detail['大限匹配'] else "❌"
        xiao_xian_status = "✅" if detail['小限匹配'] else "❌"
        print(f"{detail['案例']}: 年龄{detail['年龄']}岁")
        print(f"  大限: {detail['大限宫位']} (期望{detail['大限期望']}) {da_xian_status}")
        print(f"  小限: {detail['小限宫位']} (期望{detail['小限期望']}) {xiao_xian_status}")
        print(f"  流年判断: {detail['流年判断']} (评分{detail['流年评分']})")
    
    print("\n" + "=" * 50)
    
    import json
    print(json.dumps({
        "liu_nian_accuracy": result['liu_nian_accuracy'],
        "da_xian_accuracy": result['da_xian_accuracy'],
        "xiao_xian_accuracy": result['xiao_xian_accuracy'],
        "test_cases_passed": result['test_cases_passed']
    }, ensure_ascii=False))
    
    return 0 if result['liu_nian_accuracy'] >= 50 else 1

if __name__ == '__main__':
    sys.exit(main())