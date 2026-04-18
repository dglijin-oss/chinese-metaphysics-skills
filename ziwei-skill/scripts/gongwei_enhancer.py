#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数宫位关系分析模块 v1.0.0
天工长老开发 - Self-Evolve 进化实验 #6

功能：
- 宫位三方四正关系分析
- 宫位冲合刑害判断
- 星曜宫位互动分析
- 宫位强弱评分
目标：宫位关系分析准确度≥95%
"""

import json
from typing import Dict, List, Optional, Tuple

# ============== 基础数据 ==============

# 十二宫
SHI_ER_GONG = [
    '命宫', '兄弟', '夫妻', '子女', '财帛', '疾厄',
    '迁移', '奴仆', '官禄', '田宅', '福德', '相貌'
]

# 十四主星
ZHU_XING = [
    '紫微', '天机', '太阳', '武曲', '天同', '廉贞', '天府',
    '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军'
]

# 主星五行
ZHU_XING_WUXING = {
    '紫微': '土', '天机': '木', '太阳': '火', '武曲': '金',
    '天同': '水', '廉贞': '火', '天府': '土', '太阴': '水',
    '贪狼': '水', '巨门': '土', '天相': '水', '天梁': '土',
    '七杀': '金', '破军': '水'
}

# 主星阴阳
ZHU_XING_YINYANG = {
    '紫微': '阴', '天机': '阴', '太阳': '阳', '武曲': '阳',
    '天同': '阳', '廉贞': '阴', '天府': '阳', '太阴': '阴',
    '贪狼': '阳', '巨门': '阴', '天相': '阳', '天梁': '阳',
    '七杀': '阳', '破军': '阴'
}

# 主星庙旺落陷
ZHU_XING_MIAO_WANG = {
    '紫微': {'庙': '午', '旺': '巳', '平': '寅申', '陷': '卯'},
    '天机': {'庙': '丑', '旺': '辰', '平': '寅', '陷': '亥'},
    '太阳': {'庙': '卯', '旺': '辰巳', '平': '寅', '陷': '酉'},
    '武曲': {'庙': '卯', '旺': '辰巳', '平': '寅', '陷': '申'},
    '天同': {'庙': '卯', '旺': '辰', '平': '寅', '陷': '戌'},
    '廉贞': {'庙': '申', '旺': '酉', '平': '寅', '陷': '巳'},
    '天府': {'庙': '戌', '旺': '卯', '平': '寅', '陷': '丑'},
    '太阴': {'庙': '酉', '旺': '亥', '平': '卯', '陷': '巳'},
    '贪狼': {'庙': '辰', '旺': '寅', '平': '卯', '陷': '戌'},
    '巨门': {'庙': '子', '旺': '丑', '平': '寅', '陷': '午'},
    '天相': {'庙': '卯', '旺': '辰', '平': '寅', '陷': '戌'},
    '天梁': {'庙': '子', '旺': '丑', '平': '寅', '陷': '巳'},
    '七杀': {'庙': '寅', '旺': '申', '平': '卯', '陷': '未'},
    '破军': {'庙': '子', '旺': '辰', '平': '寅', '陷': '午'}
}

# 十二宫地支
GONG_DIZHI = {
    '命宫': '子', '兄弟': '丑', '夫妻': '寅', '子女': '卯',
    '财帛': '辰', '疾厄': '巳', '迁移': '午', '奴仆': '未',
    '官禄': '申', '田宅': '酉', '福德': '戌', '相貌': '亥'
}

# 三方四正关系
# 三方：对宫、左邻、右邻
# 四正：三方加上本宫
SAN_FANG = {
    '命宫': ['迁移', '财帛', '官禄'],
    '兄弟': ['奴仆', '子女', '田宅'],
    '夫妻': ['官禄', '子女', '福德'],
    '子女': ['田宅', '夫妻', '兄弟'],
    '财帛': ['福德', '命宫', '迁移'],
    '疾厄': ['相貌', '奴仆', '兄弟'],
    '迁移': ['命宫', '财帛', '官禄'],
    '奴仆': ['兄弟', '疾厄', '相貌'],
    '官禄': ['夫妻', '迁移', '命宫'],
    '田宅': ['子女', '兄弟', '奴仆'],
    '福德': ['财帛', '夫妻', '官禄'],
    '相貌': ['疾厄', '奴仆', '兄弟']
}

# 对宫关系
DUI_GONG = {
    '命宫': '迁移', '迁移': '命宫',
    '兄弟': '奴仆', '奴仆': '兄弟',
    '夫妻': '官禄', '官禄': '夫妻',
    '子女': '田宅', '田宅': '子女',
    '财帛': '福德', '福德': '财帛',
    '疾厄': '相貌', '相貌': '疾厄'
}

# 宫位五行
GONG_WUXING = {
    '命宫': '水', '兄弟': '土', '夫妻': '木', '子女': '木',
    '财帛': '土', '疾厄': '火', '迁移': '火', '奴仆': '土',
    '官禄': '金', '田宅': '金', '福德': '土', '相貌': '水'
}

# 宫位主要事项
GONG_SHIXIANG = {
    '命宫': '自身、性格、命运',
    '兄弟': '兄弟姐妹、朋友、同事',
    '夫妻': '婚姻、感情、配偶',
    '子女': '子女、后代、学生',
    '财帛': '财运、收入、资产',
    '疾厄': '健康、疾病、灾厄',
    '迁移': '出行、迁移、外运',
    '奴仆': '下属、员工、人际',
    '官禄': '事业、工作、官位',
    '田宅': '房产、家宅、祖业',
    '福德': '福气、精神、享受',
    '相貌': '外貌、名誉、形象'
}


class GongWeiAnalyzer:
    """宫位关系分析器"""
    
    def __init__(self):
        pass
    
    def analyze_sanfang(self, gong_name: str, pan: Dict) -> Dict:
        """
        分析三方四正关系
        
        Args:
            gong_name: 宫位名称
            pan: 命盘数据
        
        Returns:
            三方四正分析结果
        """
        result = {
            '本宫': gong_name,
            '三方宫位': [],
            '四正关系': [],
            '三方星曜': [],
            '三方吉凶': '',
        }
        
        # 获取三方宫位
        sanfang_list = SAN_FANG.get(gong_name, [])
        result['三方宫位'] = sanfang_list
        
        # 分析每个三方宫位
        sanfang_xing = []
        sanfang_ji_count = 0
        sanfang_xiong_count = 0
        
        for gong in sanfang_list + [gong_name]:
            gong_data = pan.get(gong, {})
            xing_list = gong_data.get('主星', [])
            
            for xing in xing_list:
                sanfang_xing.append(f"{xing}({gong})")
                
                # 判断星曜吉凶（简化）
                if xing in ['紫微', '天府', '天相', '天梁', '天同']:
                    sanfang_ji_count += 1
                elif xing in ['七杀', '破军', '贪狼', '廉贞']:
                    sanfang_xiong_count += 1
        
        result['三方星曜'] = sanfang_xing
        
        # 三方吉凶判断
        if sanfang_ji_count >= 3 and sanfang_xiong_count <= 1:
            result['三方吉凶'] = '三方吉'
            result['三方评分'] = 80
        elif sanfang_ji_count >= sanfang_xiong_count:
            result['三方吉凶'] = '三方平吉'
            result['三方评分'] = 60
        elif sanfang_xiong_count >= 3:
            result['三方吉凶'] = '三方凶'
            result['三方评分'] = 30
        else:
            result['三方吉凶'] = '三方平'
            result['三方评分'] = 50
        
        return result
    
    def analyze_duigong(self, gong_name: str, pan: Dict) -> Dict:
        """
        分析对宫关系
        
        Args:
            gong_name: 宫位名称
            pan: 命盘数据
        
        Returns:
            对宫关系分析
        """
        duigong = DUI_GONG.get(gong_name, '')
        
        if not duigong:
            return {'对宫': '无', '对宫关系': '无'}
        
        # 本宫星曜
        ben_gong_xing = pan.get(gong_name, {}).get('主星', [])
        
        # 对宫星曜
        dui_gong_xing = pan.get(duigong, {}).get('主星', [])
        
        # 对宫关系判断
        relation = []
        
        # 检查星曜冲合
        for ben_xing in ben_gong_xing:
            for dui_xing in dui_gong_xing:
                ben_wx = ZHU_XING_WUXING.get(ben_xing, '土')
                dui_wx = ZHU_XING_WUXING.get(dui_xing, '土')
                
                # 五行相冲（对冲）
                if self._is_chong(ben_wx, dui_wx):
                    relation.append(f'{ben_xing}与{dui_xing}冲')
                
                # 五行相合
                if self._is_he(ben_wx, dui_wx):
                    relation.append(f'{ben_xing}与{dui_xing}合')
        
        return {
            '本宫': gong_name,
            '本宫星曜': ben_gong_xing,
            '对宫': duigong,
            '对宫星曜': dui_gong_xing,
            '对宫关系': relation if relation else ['无冲合'],
        }
    
    def _is_chong(self, wx1: str, wx2: str) -> bool:
        """判断五行相冲"""
        chong_pairs = [('金', '火'), ('火', '金'), ('木', '金'), ('金', '木'), ('水', '土'), ('土', '水')]
        return (wx1, wx2) in chong_pairs or (wx2, wx1) in chong_pairs
    
    def _is_he(self, wx1: str, wx2: str) -> bool:
        """判断五行相合"""
        he_pairs = [('金', '水'), ('水', '金'), ('木', '火'), ('火', '木'), ('土', '金'), ('金', '土')]
        return (wx1, wx2) in he_pairs or (wx2, wx1) in he_pairs
    
    def analyze_xing_gong_relation(self, xing: str, gong: str) -> Dict:
        """
        分析星曜与宫位关系
        
        Args:
            xing: 星曜名称
            gong: 宫位名称
        
        Returns:
            星宫关系分析
        """
        xing_wx = ZHU_XING_WUXING.get(xing, '土')
        gong_wx = GONG_WUXING.get(gong, '土')
        
        # 星曜五行与宫位五行关系
        relation = []
        strength = 50
        
        # 星生宫（星曜五行生宫位五行）
        sheng_map = {'金': '水', '水': '木', '木': '火', '火': '土', '土': '金'}
        if sheng_map.get(xing_wx) == gong_wx:
            relation.append(f'{xing}({xing_wx})生{gong}({gong_wx})')
            strength = 70
        
        # 宫生星（宫位五行生星曜五行）
        if sheng_map.get(gong_wx) == xing_wx:
            relation.append(f'{gong}({gong_wx})生{xing}({xing_wx})')
            strength = 80
        
        # 星克宫
        ke_map = {'金': '木', '木': '土', '土': '水', '水': '火', '火': '金'}
        if ke_map.get(xing_wx) == gong_wx:
            relation.append(f'{xing}({xing_wx})克{gong}({gong_wx})')
            strength = 30
        
        # 宫克星
        if ke_map.get(gong_wx) == xing_wx:
            relation.append(f'{gong}({gong_wx})克{xing}({xing_wx})')
            strength = 25
        
        # 星宫同五行
        if xing_wx == gong_wx:
            relation.append(f'{xing}与{gong}五行相同')
            strength = 60
        
        if not relation:
            relation.append('无特殊关系')
        
        return {
            '星曜': xing,
            '星曜五行': xing_wx,
            '宫位': gong,
            '宫位五行': gong_wx,
            '星宫关系': relation,
            '星宫强度': strength,
        }
    
    def analyze_all_gong(self, pan: Dict) -> Dict:
        """
        综合分析所有宫位关系
        
        Args:
            pan: 命盘数据
        
        Returns:
            全盘宫位关系分析
        """
        result = {
            '宫位分析': {},
            '重要宫位': [],
            '强宫': [],
            '弱宫': [],
            '综合评分': 50,
        }
        
        # 分析每个宫位
        for gong in SHI_ER_GONG:
            gong_data = pan.get(gong, {})
            xing_list = gong_data.get('主星', [])
            
            # 三方分析
            sanfang_result = self.analyze_sanfang(gong, pan)
            
            # 对宫分析
            duigong_result = self.analyze_duigong(gong, pan)
            
            # 星宫关系
            xing_gong_result = []
            for xing in xing_list:
                xg = self.analyze_xing_gong_relation(xing, gong)
                xing_gong_result.append(xg)
            
            # 宫位评分
            gong_score = sanfang_result.get('三方评分', 50)
            for xg in xing_gong_result:
                gong_score = (gong_score + xg.get('星宫强度', 50)) / 2
            
            result['宫位分析'][gong] = {
                '主星': xing_list,
                '三方': sanfang_result,
                '对宫': duigong_result,
                '星宫关系': xing_gong_result,
                '宫位评分': gong_score,
            }
            
            # 分类强宫弱宫
            if gong_score >= 70:
                result['强宫'].append(gong)
            elif gong_score <= 35:
                result['弱宫'].append(gong)
        
        # 重要宫位（命宫、财帛、官禄、夫妻）
        result['重要宫位'] = ['命宫', '财帛', '官禄', '夫妻']
        
        # 综合评分
        important_scores = []
        for gong in result['重要宫位']:
            important_scores.append(result['宫位分析'].get(gong, {}).get('宫位评分', 50))
        
        result['综合评分'] = sum(important_scores) / len(important_scores) if important_scores else 50
        
        return result


# ============== 测试验证 ==============

def validate_gongwei():
    """
    验证宫位关系分析准确度
    """
    analyzer = GongWeiAnalyzer()
    
    # 测试案例
    test_cases = [
        {
            'name': '例1-命宫紫微',
            'pan': {
                '命宫': {'主星': ['紫微', '天府']},
                '迁移': {'主星': ['天机']},
                '财帛': {'主星': ['武曲', '天相']},
                '官禄': {'主星': ['太阳']},
            },
            'expected_sanfang_ji': True,
        },
        {
            'name': '例2-命宫七杀',
            'pan': {
                '命宫': {'主星': ['七杀', '破军']},
                '迁移': {'主星': ['贪狼']},
                '财帛': {'主星': ['廉贞']},
                '官禄': {'主星': ['巨门']},
            },
            'expected_sanfang_ji': False,
        },
    ]
    
    results = []
    
    for case in test_cases:
        sanfang_result = analyzer.analyze_sanfang('命宫', case['pan'])
        
        matched = (sanfang_result['三方吉凶'] in ['三方吉', '三方平吉']) == case['expected_sanfang_ji']
        
        results.append({
            '案例': case['name'],
            '三方吉凶': sanfang_result['三方吉凶'],
            '三方评分': sanfang_result['三方评分'],
            '三方星曜': sanfang_result['三方星曜'],
            '期望吉': case['expected_sanfang_ji'],
            '匹配': matched,
        })
    
    # 统计
    passed = sum(1 for r in results if r['匹配'])
    total = len(results)
    
    return {
        'gongwei_accuracy': passed / total * 100 if total > 0 else 0,
        'test_cases_passed': passed,
        'test_cases_total': total,
        'details': results,
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='紫微斗数宫位关系分析模块')
    parser.add_argument('--validate', '-v', action='store_true', help='验证测试')
    parser.add_argument('--pan', '-p', type=str, help='命盘JSON文件')
    
    args = parser.parse_args()
    
    if args.validate:
        result = validate_gongwei()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.pan:
        with open(args.pan, 'r') as f:
            pan = json.load(f)
        analyzer = GongWeiAnalyzer()
        result = analyzer.analyze_all_gong(pan)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法：python3 gongwei_enhancer.py --validate 或 --pan <命盘文件>")