#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六爻纳甲应期推算测试脚本
天工长老开发 - Self-Evolve 进化实验验证
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yinqi_calculator import validate_yinqi

def main():
    """运行应期推算验证测试"""
    print("=" * 50)
    print("六爻纳甲应期推算验证测试")
    print("=" * 50)
    
    result = validate_yinqi()
    
    print(f"\n📊 测试统计:")
    print(f"• 准确度: {result['yinqi_accuracy']}%")
    print(f"• 平均误差: {result['avg_error_days']} 天")
    print(f"• 通过案例: {result['test_cases_passed']}/{result['test_cases_total']}")
    
    print(f"\n📋 详细结果:")
    for detail in result['details']:
        status = "✅" if detail['匹配'] else "❌"
        print(f"{status} {detail['案例']}: 期望 {detail['期望应期']} → 预测 {detail['预测应期']}")
    
    print("\n" + "=" * 50)
    
    # 返回JSON格式供遥测
    import json
    print(json.dumps({
        "yinqi_accuracy": result['yinqi_accuracy'],
        "avg_error_days": result['avg_error_days'],
        "test_cases_passed": result['test_cases_passed']
    }, ensure_ascii=False))
    
    return 0 if result['yinqi_accuracy'] >= 50 else 1

if __name__ == '__main__':
    sys.exit(main())