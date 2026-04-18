#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
太乙神数格局分析模块 v1.0.0
天工长老开发 - Self-Evolve 进化实验 #8

功能：
- 十六神将格局判断
- 主客算强弱分析
- 太乙格局组合分析
- 格局评分系统
目标：格局识别准确度≥95%
"""

import json
from typing import Dict, List, Optional, Tuple

# ============== 基础数据 ==============

# 十六神将
SHI_SHI_SHEN_JIANG = [
    '文昌', '始击', '主大将', '客大将', '主参将', '客参将',
    '计神', '定计', '君基', '臣基', '民基', '五福',
    '大游', '小游', '四神', '天乙'
]

# 十六神将吉凶
SHEN_JIANG_JI_XIONG = {
    '文昌': '吉', '始击': '凶', '主大将': '吉', '客大将': '吉',
    '主参将': '吉', '客参将': '吉', '计神': '吉', '定计': '吉',
    '君基': '大吉', '臣基': '吉', '民基': '吉', '五福': '大吉',
    '大游': '凶', '小游': '凶', '四神': '中', '天乙': '大吉'
}

# 十六神将五行
SHEN_JIANG_WUXING = {
    '文昌': '木', '始击': '火', '主大将': '金', '客大将': '金',
    '主参将': '金', '客参将': '金', '计神': '土', '定计': '土',
    '君基': '土', '臣基': '土', '民基': '土', '五福': '土',
    '大游': '水', '小游': '水', '四神': '火', '天乙': '土'
}

# 太乙格局
TAI_YI_GEJU = {
    '太乙临吉宫': {
        '条件': '太乙落坎/震/巽宫',
        '含义': '主方吉利，宜主动进取',
        '强度': 80
    },
    '太乙临凶宫': {
        '条件': '太乙落坤/艮/乾宫',
        '含义': '主方不利，宜谨慎行事',
        'strength': -70
    },
    '文昌遇主大将': {
        'condition': '文昌+主大将同宫',
        '含义': '主方有贵人助力',
        '强度': 90
    },
    '始击遇客大将': {
        'condition': '始击+客大将同宫',
        '含义': '客方有贵人助力',
        'strength': 85
    },
    '五福临命宫': {
        'condition': '五福落命宫',
        '含义': '大吉格局，百事皆宜',
        '强度': 95
    },
    '大游临命宫': {
        'condition': '大游落命宫',
        '含义': '大凶格局，诸事不宜',
        'strength': -90
    },
}

# 太乙九宫
TAI_YI_GONG = ['乾', '离', '艮', '兑', '中', '坎', '坤', '震', '巽']

# 九宫五行
JIU_GONG_WUXING = {
    '乾': '金', '离': '火', '艮': '土', '兑': '金',
    '中': '土', '坎': '水', '坤': '土', '震': '木', '巽': '木'
}

# 九宫吉凶（太乙视角）
JIU_GONG_JI_XIONG = {
    '坎': '吉', '震': '吉', '巽': '吉',
    '坤': '凶', '艮': '凶', '乾': '凶',
    '离': '中', '兑': '中', '中': '中'
}


class TaiYiGeJuAnalyzer:
    """太乙格局分析器"""
    
    def __init__(self):
        pass
    
    def analyze_shen_jiang(self, shen_jiang_data: Dict) -> Dict:
        """
        分析十六神将格局
        
        Args:
            shen_jiang_data: 神将数据
        
        Returns:
            神将分析结果
        """
        result = {
            '神将格局': [],
            '神将评分': 50,
        }
        
        # 分析每个神将
        ji_count = 0
        xiong_count = 0
        
        for shen_name in SHI_SHI_SHEN_JIANG:
            shen_data = shen_jiang_data.get(shen_name, {})
            gong = shen_data.get('宫', '')
            
            if not gong:
                continue
            
            # 神将本身吉凶
            shen_ji = SHEN_JIANG_JI_XIONG.get(shen_name, '中')
            
            # 神将落宫吉凶
            gong_ji = JIU_GONG_JI_XIONG.get(gong, '中')
            
            # 综合判断
            if shen_ji in ['吉', '大吉'] and gong_ji in ['吉', '中']:
                ji_count += 1
                result['神将格局'].append({
                    '神将': shen_name,
                    '落宫': gong,
                    '吉凶': '吉',
                    '含义': f'{shen_name}临{gong}宫，吉利'
                })
            elif shen_ji in ['凶', '大凶'] or gong_ji in ['凶']:
                xiong_count += 1
                result['神将格局'].append({
                    '神将': shen_name,
                    '落宫': gong,
                    '吉凶': '凶',
                    '含义': f'{shen_name}临{gong}宫，凶险'
                })
        
        # 计算评分
        result['神将评分'] = 50 + (ji_count - xiong_count) * 5
        
        return result
    
    def analyze_zhu_ke_suan(self, suan_data: Dict) -> Dict:
        """
        分析主客算
        
        Args:
            suan_data: 算数据
        
        Returns:
            主客算分析结果
        """
        result = {
            '主算分析': {},
            '客算分析': {},
            '主客对比': '',
            '主客评分': 50,
        }
        
        # 主算
        zhu_suan = suan_data.get('主算', {})
        zhu_num = zhu_suan.get('数', 0)
        
        # 客算
        ke_suan = suan_data.get('客算', {})
        ke_num = ke_suan.get('数', 0)
        
        # 分析主算
        result['主算分析'] = {
            '数': zhu_num,
            '判断': self._analyze_suan_number(zhu_num),
            '含义': self._get_suan_meaning(zhu_num, '主')
        }
        
        # 分析客算
        result['客算分析'] = {
            '数': ke_num,
            '判断': self._analyze_suan_number(ke_num),
            '含义': self._get_suan_meaning(ke_num, '客')
        }
        
        # 主客对比
        if zhu_num > ke_num:
            result['主客对比'] = '主算大于客算，主方优势'
            result['主客评分'] = 60
        elif zhu_num < ke_num:
            result['主客对比'] = '客算大于主算，客方优势'
            result['主客评分'] = 40
        else:
            result['主客对比'] = '主客算相等，势均力敌'
            result['主客评分'] = 50
        
        return result
    
    def _analyze_suan_number(self, num: int) -> str:
        """分析算数"""
        if num >= 10:
            return '大算'
        elif num >= 5:
            return '中算'
        else:
            return '小算'
    
    def _get_suan_meaning(self, num: int, side: str) -> str:
        """获取算数含义"""
        if num >= 10:
            return f'{side}方大算，力量强劲'
        elif num >= 5:
            return f'{side}方中算，力量适中'
        else:
            return f'{side}方小算，力量不足'
    
    def analyze_taiyi_geju(self, pan_data: Dict) -> Dict:
        """
        综合分析太乙格局
        
        Args:
            pan_data: 太乙盘数据
        
        Returns:
            太乙格局分析结果
        """
        result = {
            '格局判断': '',
            '格局评分': 50,
            '格局建议': '',
        }
        
        # 神将分析
        shen_jiang_result = self.analyze_shen_jiang(pan_data.get('神将', {}))
        
        # 主客算分析
        suan_result = self.analyze_zhu_ke_suan(pan_data.get('算', {}))
        
        # 综合评分
        result['格局评分'] = (shen_jiang_result['神将评分'] + suan_result['主客评分']) / 2
        
        # 格局判断
        if result['格局评分'] >= 70:
            result['格局判断'] = '吉局'
            result['格局建议'] = '格局吉利，宜积极进取'
        elif result['格局评分'] >= 50:
            result['格局判断'] = '平局'
            result['格局建议'] = '格局平稳，宜守不宜攻'
        elif result['格局评分'] >= 30:
            result['格局判断'] = '凶局'
            result['格局建议'] = '格局偏凶，宜谨慎行事'
        else:
            result['格局判断'] = '大凶局'
            result['格局建议'] = '格局大凶，宜韬光养晦'
        
        result['神将分析'] = shen_jiang_result
        result['主客算分析'] = suan_result
        
        return result


# ============== 测试验证 ==============

def validate_geju():
    """
    验证格局识别准确度
    """
    analyzer = TaiYiGeJuAnalyzer()
    
    # 测试案例
    test_cases = [
        {
            'name': '例1-吉局',
            'pan_data': {
                '神将': {
                    '五福': {'宫': '坎'},
                    '天乙': {'宫': '震'},
                    '文昌': {'宫': '巽'},
                    '主大将': {'宫': '坎'},
                },
                '算': {
                    '主算': {'数': 12},
                    '客算': {'数': 8},
                }
            },
            'expected_ji': True,
        },
        {
            'name': '例2-凶局',
            'pan_data': {
                '神将': {
                    '大游': {'宫': '坤'},
                    '小游': {'宫': '艮'},
                    '始击': {'宫': '乾'},
                },
                '算': {
                    '主算': {'数': 3},
                    '客算': {'数': 10},
                }
            },
            'expected_ji': False,
        },
    ]
    
    results = []
    
    for case in test_cases:
        result = analyzer.analyze_taiyi_geju(case['pan_data'])
        
        matched = (result['格局判断'] in ['吉局', '平局']) == case['expected_ji']
        
        results.append({
            '案例': case['name'],
            '格局判断': result['格局判断'],
            '格局评分': result['格局评分'],
            '主客对比': result['主客算分析']['主客对比'],
            '期望吉': case['expected_ji'],
            '匹配': matched,
        })
    
    # 统计
    passed = sum(1 for r in results if r['匹配'])
    total = len(results)
    
    return {
        'geju_accuracy': passed / total * 100 if total > 0 else 0,
        'test_cases_passed': passed,
        'test_cases_total': total,
        'details': results,
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='太乙神数格局分析模块')
    parser.add_argument('--validate', '-v', action='store_true', help='验证测试')
    
    args = parser.parse_args()
    
    if args.validate:
        result = validate_geju()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法：python3 geju_enhancer.py --validate")