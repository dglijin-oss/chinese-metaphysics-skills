#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数卦气旺衰测试脚本
天工长老开发 - Self-Evolve 进化实验 #2 验证
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gua_qi_enhancer import validate_gua_qi

def main():
    """运行卦气旺衰验证测试"""
    print("=" * 50)
    print("梅花易数卦气旺衰验证测试")
    print("=" * 50)
    
    result = validate_gua_qi()
    
    print(f"\n📊 测试统计:")
    print(f"• 卦气准确度: {result['gua_qi_accuracy']}%")
    print(f"• 应期准确度: {result['yinqi_accuracy']}%")
    print(f"• 平均误差: {result['avg_error_days']} 天")
    print(f"• 通过案例: {result['test_cases_passed']}/{result['test_cases_total']}")
    
    print(f"\n📋 详细结果:")
    for detail in result['details']:
        wuxing_status = "✅" if detail['五行匹配'] else "❌"
        yinqi_status = "✅" if detail['应期匹配'] else "❌"
        print(f"{wuxing_status} {detail['案例']}: {detail['体卦']}({detail['卦五行']}) 卦气{detail['卦气状态']}")
        print(f"   应期: 期望{detail['期望地支']}日 → 预测{detail['预测地支']}日 {yinqi_status}")
    
    print("\n" + "=" * 50)
    
    import json
    print(json.dumps({
        "gua_qi_accuracy": result['gua_qi_accuracy'],
        "yinqi_accuracy": result['yinqi_accuracy'],
        "avg_error_days": result['avg_error_days'],
        "test_cases_passed": result['test_cases_passed']
    }, ensure_ascii=False))
    
    return 0 if result['yinqi_accuracy'] >= 50 else 1

if __name__ == '__main__':
    sys.exit(main())