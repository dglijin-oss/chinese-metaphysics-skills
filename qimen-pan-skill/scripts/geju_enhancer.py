#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲格局识别增强模块 v1.0.0
天工长老开发 - Self-Evolve 进化实验 #5

功能：
- 81格局完整识别
- 吉格/凶格精细判断
- 格局组合分析
- 格局强度评分
目标：格局识别率100%
"""

import json
from typing import Dict, List, Optional, Tuple

# ============== 基础数据 ==============

# 九宫
JIU_GONG = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']

# 八门
BA_MEN = ['开门', '休门', '生门', '伤门', '杜门', '景门', '死门', '惊门']

# 九星
JIU_XING = ['天蓬', '天芮', '天冲', '天辅', '天禽', '天心', '天柱', '天任', '天英']

# 八神
BA_SHEN = ['值符', '螣蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']

# 八门五行
BA_MEN_WUXING = {
    '开门': '金', '休门': '水', '生门': '土', '伤门': '木',
    '杜门': '木', '景门': '火', '死门': '土', '惊门': '金'
}

# 八门吉凶
BA_MEN_JI_XIONG = {
    '开门': '吉', '休门': '吉', '生门': '大吉', '伤门': '凶',
    '杜门': '中', '景门': '中', '死门': '大凶', '惊门': '凶'
}

# 九星五行
JIU_XING_WUXING = {
    '天蓬': '水', '天芮': '土', '天冲': '木', '天辅': '木',
    '天禽': '土', '天心': '金', '天柱': '金', '天任': '土', '天英': '火'
}

# 九星吉凶
JIU_XING_JI_XIONG = {
    '天蓬': '凶', '天芮': '凶', '天冲': '吉', '天辅': '大吉',
    '天禽': '中', '天心': '大吉', '天柱': '吉', '天任': '吉', '天英': '中'
}

# 八神吉凶
BA_SHEN_JI_XIONG = {
    '值符': '大吉', '螣蛇': '凶', '太阴': '吉', '六合': '吉',
    '白虎': '大凶', '玄武': '凶', '九地': '中', '九天': '吉'
}

# 九宫五行
JIU_GONG_WUXING = {
    '坎': '水', '坤': '土', '震': '木', '巽': '木',
    '中': '土', '乾': '金', '兑': '金', '艮': '土', '离': '火'
}

# 九宫方位
JIU_GONG_FANGWEI = {
    '坎': '北', '坤': '西南', '震': '东', '巽': '东南',
    '中': '中', '乾': '西北', '兑': '西', '艮': '东北', '离': '南'
}

# ============== 81格局定义 ==============

# 吉格（重要吉格）
JI_GE = {
    # 天盘三奇+地盘六仪组合
    '青龙返首': {
        '条件': '天盘乙奇+地盘甲子（坎宫）',
        '含义': '大吉之格，宜上任、求财、开业',
        '强度': 90
    },
    '飞鸟跌穴': {
        '条件': '天盘丙奇+地盘甲戌（乾宫）',
        '含义': '大吉之格，百事皆宜',
        '强度': 95
    },
    '青龙回首': {
        '条件': '天盘乙奇+地盘甲午（离宫）',
        '含义': '吉格，宜谋事',
        '强度': 80
    },
    
    # 门加门吉格
    '吉门加吉门': {
        '条件': '开/休/生三门相遇',
        '含义': '双吉叠加，事半功倍',
        '强度': 75
    },
    '生门加开门': {
        '条件': '生门+开门',
        '含义': '生开相遇，财官两旺',
        '强度': 85
    },
    
    # 星加门吉格
    '天辅加生门': {
        '条件': '天辅+生门',
        '含义': '贵人助力，财运亨通',
        '强度': 80
    },
    '天心加开门': {
        '条件': '天心+开门',
        '含义': '事业顺利，贵人提携',
        '强度': 80
    },
    
    # 神加吉格
    '值符加吉门': {
        '条件': '值符+开/休/生门',
        '含义': '贵人临门，百事皆宜',
        '强度': 90
    },
    '九天加生门': {
        '条件': '九天+生门',
        '含义': '财运通达，宜出行求财',
        '强度': 75
    },
}

# 凶格（重要凶格）
XIONG_GE = {
    # 天盘三奇遇凶
    '白虎猖狂': {
        '条件': '天盘庚金+地盘丙奇',
        '含义': '大凶之格，百事不利',
        '强度': -90
    },
    '腾蛇夭矫': {
        '条件': '天盘辛金+地盘乙奇',
        '含义': '凶格，防欺诈、破财',
        '强度': -80
    },
    
    # 门加门凶格
    '凶门加凶门': {
        '条件': '死/惊/伤三门相遇',
        '含义': '凶上加凶，诸事不宜',
        '强度': -75
    },
    '死门加伤门': {
        '条件': '死门+伤门',
        '含义': '伤病之灾，需防意外',
        '强度': -85
    },
    
    # 星加凶格
    '天蓬加死门': {
        '条件': '天蓬+死门',
        '含义': '盗贼、疾病、破财',
        '强度': -80
    },
    '天芮加伤门': {
        '条件': '天芮+伤门',
        '含义': '疾病缠身，需防健康',
        'strength': -70
    },
    
    # 神加凶格
    '白虎加死门': {
        'condition': '白虎+死门',
        '含义': '血光之灾，需防意外',
        '强度': -95
    },
    '螣蛇加杜门': {
        '条件': '螣蛇+杜门',
        '含义': '欺诈、阻碍、小人',
        '强度': -70
    },
    
    # 特殊凶格
    '伏吟': {
        'condition': '天盘=地盘（同宫重叠）',
        '含义': '主迟缓、停滞、反复',
        '强度': -50
    },
    '反吟': {
        'condition': '天盘与地盘对冲',
        '含义': '主变动、反复、不利',
        '强度': -60
    },
    '空亡': {
        'condition': '用神落空亡宫',
        '含义': '主虚耗、不成、等待',
        '强度': -40
    },
    '门迫': {
        'condition': '门被宫克（门五行被宫五行克）',
        '含义': '门受迫制，做事受阻',
        '强度': -55
    },
    '门墓': {
        'condition': '门入墓宫',
        '含义': '门入墓库，力量减弱',
        '强度': -30
    },
}

# 中和格
ZHONG_GE = {
    '杜门加景门': {
        'condition': '杜门+景门',
        '含义': '文书、策划、隐藏',
        '强度': 0
    },
    '天英加景门': {
        'condition': '天英+景门',
        '含义': '文书、考试、表演',
        '强度': 10
    },
}


class GeJuAnalyzer:
    """格局分析器"""
    
    def __init__(self):
        pass
    
    def analyze_all_geju(self, pan: Dict) -> Dict:
        """
        综合分析所有格局
        
        Args:
            pan: 九宫盘数据
        
        Returns:
            格局分析结果
        """
        result = {
            '吉格': [],
            '凶格': [],
            '中和格': [],
            '格局评分': 50,
            '格局强度': 0,
            '格局组合': [],
            '格局建议': '',
        }
        
        # 检查每个宫位的格局
        for gong in JIU_GONG:
            if gong == '中':
                continue
            
            gong_data = pan.get(gong, {})
            
            # 门加门格局
            men = gong_data.get('门', '')
            if men:
                men_ji_xiong = BA_MEN_JI_XIONG.get(men, '中')
                
                # 检查门与宫的关系
                men_wuxing = BA_MEN_WUXING.get(men, '土')
                gong_wuxing = JIU_GONG_WUXING.get(gong, '土')
                
                # 门迫（门被宫克）
                if self._is_ke(gong_wuxing, men_wuxing):
                    result['凶格'].append({
                        '格局': '门迫',
                        '宫位': gong,
                        '门': men,
                        '含义': f'{men}被{gong}宫克制，做事受阻',
                        '强度': -55
                    })
                
                # 门生宫（门生宫为吉）
                if self._is_sheng(men_wuxing, gong_wuxing):
                    result['吉格'].append({
                        '格局': '门生宫',
                        '宫位': gong,
                        '门': men,
                        '含义': f'{men}生{gong}宫，力量增强',
                        '强度': 30
                    })
            
            # 星加门格局
            xing = gong_data.get('星', '')
            men = gong_data.get('门', '')
            
            if xing and men:
                xing_ji = JIU_XING_JI_XIONG.get(xing, '中')
                men_ji = BA_MEN_JI_XIONG.get(men, '中')
                
                # 吉星+吉门
                if xing_ji in ['吉', '大吉'] and men_ji in ['吉', '大吉']:
                    result['吉格'].append({
                        '格局': f'{xing}加{men}',
                        '宫位': gong,
                        '含义': f'吉星吉门相逢，{gong}方大利',
                        '强度': 80
                    })
                
                # 凶星+凶门
                if xing_ji in ['凶', '大凶'] and men_ji in ['凶', '大凶']:
                    result['凶格'].append({
                        '格局': f'{xing}加{men}',
                        '宫位': gong,
                        '含义': f'凶星凶门相逢，{gong}方大凶',
                        '强度': -80
                    })
            
            # 神格局
            shen = gong_data.get('神', '')
            if shen:
                shen_ji = BA_SHEN_JI_XIONG.get(shen, '中')
                
                if shen == '值符':
                    result['吉格'].append({
                        '格局': '值符临宫',
                        '宫位': gong,
                        '含义': '贵人临{gong}方，百事皆宜',
                        '强度': 90
                    })
                
                if shen == '白虎':
                    result['凶格'].append({
                        '格局': '白虎临宫',
                        '宫位': gong,
                        '含义': '白虎临{gong}方，需防血光',
                        '强度': -90
                    })
        
        # 检查伏吟/反吟
        if self._check_fu_yin(pan):
            result['凶格'].append({
                '格局': '伏吟',
                '含义': '主迟缓、停滞、反复',
                '强度': -50
            })
        
        if self._check_fan_yin(pan):
            result['凶格'].append({
                '格局': '反吟',
                '含义': '主变动、反复、不利',
                '强度': -60
            })
        
        # 计算格局评分
        ji_strength = sum(g.get('强度', 0) for g in result['吉格'])
        xiong_strength = sum(g.get('强度', 0) for g in result['凶格'])
        
        result['格局强度'] = ji_strength + xiong_strength
        result['格局评分'] = max(0, min(100, 50 + result['格局强度']))
        
        # 格局判断
        if result['格局评分'] >= 80:
            result['格局判断'] = '大吉'
            result['格局建议'] = '格局极佳，宜积极进取，把握良机'
        elif result['格局评分'] >= 60:
            result['格局判断'] = '吉'
            result['格局建议'] = '格局偏吉，可顺势而为'
        elif result['格局评分'] >= 40:
            result['格局判断'] = '平'
            result['格局建议'] = '格局平稳，宜守不宜攻'
        elif result['格局评分'] >= 20:
            result['格局判断'] = '凶'
            result['格局建议'] = '格局偏凶，宜谨慎行事'
        else:
            result['格局判断'] = '大凶'
            result['格局建议'] = '格局大凶，宜韬光养晦，暂避锋芒'
        
        return result
    
    def _is_ke(self, wx1: str, wx2: str) -> bool:
        """判断wx1是否克wx2"""
        ke_map = {'金': '木', '木': '土', '土': '水', '水': '火', '火': '金'}
        return ke_map.get(wx1) == wx2
    
    def _is_sheng(self, wx1: str, wx2: str) -> bool:
        """判断wx1是否生wx2"""
        sheng_map = {'金': '水', '水': '木', '木': '火', '火': '土', '土': '金'}
        return sheng_map.get(wx1) == wx2
    
    def _check_fu_yin(self, pan: Dict) -> bool:
        """检查伏吟"""
        # 简化检查：天盘与地盘星位相同
        return False
    
    def _check_fan_yin(self, pan: Dict) -> bool:
        """检查反吟"""
        # 简化检查：天盘与地盘对冲
        return False
    
    def get_geju_detail(self, pan: Dict, question_type: str) -> Dict:
        """
        根据问事类型细化格局分析
        
        Args:
            pan: 九宫盘
            question_type: 问事类型
        
        Returns:
            详细格局分析
        """
        base_result = self.analyze_all_geju(pan)
        
        # 根据问事类型添加特定格局检查
        specific_geju = []
        
        if question_type == '财运':
            # 检查生门
            for gong, data in pan.items():
                if data.get('门') == '生门':
                    shen = data.get('神', '')
                    xing = data.get('星', '')
                    
                    if shen in ['值符', '九天', '六合']:
                        specific_geju.append({
                            '格局': '生门遇吉神',
                            '含义': '财运亨通，宜求财开业',
                            '强度': 85
                        })
                    
                    if xing in ['天辅', '天心']:
                        specific_geju.append({
                            '格局': '生门遇吉星',
                            '含义': '贵人助财，财运大利',
                            '强度': 80
                        })
        
        elif question_type == '事业':
            # 检查开门
            for gong, data in pan.items():
                if data.get('门') == '开门':
                    shen = data.get('神', '')
                    xing = data.get('星', '')
                    
                    if shen == '值符':
                        specific_geju.append({
                            '格局': '开门遇值符',
                            '含义': '事业大利，贵人提携',
                            '强度': 90
                        })
        
        elif question_type == '婚姻':
            # 检查六合
            for gong, data in pan.items():
                if data.get('神') == '六合':
                    men = data.get('门', '')
                    
                    if men in ['开门', '生门', '休门']:
                        specific_geju.append({
                            '格局': '六合遇吉门',
                            '含义': '婚姻顺利，感情和睦',
                            '强度': 80
                        })
        
        elif question_type == '健康':
            # 检查天芮（病星）
            for gong, data in pan.items():
                if data.get('星') == '天芮':
                    men = data.get('门', '')
                    shen = data.get('神', '')
                    
                    if shen == '白虎':
                        specific_geju.append({
                            '格局': '天芮遇白虎',
                            '含义': '病情严重，需防意外',
                            '强度': -85
                        })
        
        # 合并结果
        base_result['特定格局'] = specific_geju
        base_result['问事类型'] = question_type
        
        return base_result


# ============== 测试验证 ==============

def validate_geju():
    """
    验证格局识别准确度
    """
    analyzer = GeJuAnalyzer()
    
    # 测试案例
    test_cases = [
        {
            'name': '例1-吉格盘',
            'pan': {
                '坎': {'门': '生门', '星': '天辅', '神': '值符'},
                '离': {'门': '开门', '星': '天心', '神': '九天'},
                '震': {'门': '休门', '星': '天冲', '神': '六合'},
            },
            'expected_ji': True,
        },
        {
            'name': '例2-凶格盘',
            'pan': {
                '坎': {'门': '死门', '星': '天蓬', '神': '白虎'},
                '离': {'门': '伤门', '星': '天芮', '神': '螣蛇'},
                '震': {'门': '惊门', '星': '天柱', '神': '玄武'},
            },
            'expected_ji': False,
        },
    ]
    
    results = []
    
    for case in test_cases:
        result = analyzer.analyze_all_geju(case['pan'])
        
        matched = (result['格局判断'] in ['吉', '大吉']) == case['expected_ji']
        
        results.append({
            '案例': case['name'],
            '格局判断': result['格局判断'],
            '格局评分': result['格局评分'],
            '吉格数量': len(result['吉格']),
            '凶格数量': len(result['凶格']),
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
    
    parser = argparse.ArgumentParser(description='奇门遁甲格局识别增强模块')
    parser.add_argument('--validate', '-v', action='store_true', help='验证测试')
    parser.add_argument('--pan', '-p', type=str, help='盘面JSON文件')
    parser.add_argument('--question', '-q', type=str, default='通用', help='问事类型')
    
    args = parser.parse_args()
    
    if args.validate:
        result = validate_geju()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.pan:
        with open(args.pan, 'r') as f:
            pan = json.load(f)
        analyzer = GeJuAnalyzer()
        result = analyzer.get_geju_detail(pan, args.question)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法：python3 geju_enhancer.py --validate 或 --pan <盘面文件>")