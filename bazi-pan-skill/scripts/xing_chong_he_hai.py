#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命理 刑冲合害分析模块 v1.0.0
天工长老开发 - v4.0.0 核心新功能

功能：
- 地支六合分析
- 地支六冲分析
- 地支三合/半三合分析
- 地支三刑分析
- 地支六害分析
- 地支相破分析
- 综合关系判断与断语
"""

from typing import Dict, List, Optional, Tuple, Set

# ============== 地支关系数据 ==============

# 天干五行
GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支五行
ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 地支藏干
ZHI_CANG_GAN = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲'],
}

# 地支六合（阴阳相合）
LIU_HE = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午',
}

# 六合含义
LIU_HE_MEANING = {
    ('子', '丑'): '子丑合土：智慧与包容相结合，利合作、婚姻',
    ('寅', '亥'): '寅亥合木：生机与滋养相合，利学业、发展',
    ('卯', '戌'): '卯戌合火：温柔与热情相合，利感情、社交',
    ('辰', '酉'): '辰酉合金：稳重与精明相合，利财运、事业',
    ('巳', '申'): '巳申合水：变化与灵活相合，利变动、创新',
    ('午', '未'): '午未合土/火：光明与包容相合，利名利、稳定',
}

# 地支六冲（对冲，相距六位）
LIU_CHONG = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳',
}

# 六冲含义
LIU_CHONG_MEANING = {
    ('子', '午'): '子午冲：水火相冲，主变动、冲突、情绪波动',
    ('丑', '未'): '丑未冲：土土相冲，主内部矛盾、家庭纠纷',
    ('寅', '申'): '寅申冲：金木相冲，主出行变动、事业转折',
    ('卯', '酉'): '卯酉冲：金木相冲，主感情波折、口舌是非',
    ('辰', '戌'): '辰戌冲：土土相冲，主地产变动、居所迁移',
    ('巳', '亥'): '巳亥冲：水火相冲，主思想冲突、远行之象',
}

# 地支三合（三支合局）
SAN_HE = {
    '申子辰': {'局': '水局', '五行': '水', '含义': '智慧流通，人脉广泛'},
    '亥卯未': {'局': '木局', '五行': '木', '含义': '生机旺盛，利成长发展'},
    '寅午戌': {'局': '火局', '五行': '火', '含义': '热情高涨，利名声事业'},
    '巳酉丑': {'局': '金局', '五行': '金', '含义': '刚毅果断，利财富积累'},
}

# 半三合（两字合）
BAN_SAN_HE = {
    # 拱合（缺中间）
    '申辰': {'局': '水局（拱）', '五行': '水', '含义': '水气暗聚，待机而发'},
    '亥未': {'局': '木局（拱）', '五行': '木', '含义': '木气暗聚，蓄势待发'},
    '寅戌': {'局': '火局（拱）', '五行': '火', '含义': '火气暗聚，伺机而动'},
    '巳丑': {'局': '金局（拱）', '五行': '金', '含义': '金气暗聚，隐忍待发'},
    # 半合（生方+中方）
    '申子': {'局': '水局（半合）', '五行': '水', '含义': '水气渐旺，智慧增长'},
    '亥卯': {'局': '木局（半合）', '五行': '木', '含义': '木气渐旺，生机勃发'},
    '寅午': {'局': '火局（半合）', '五行': '火', '含义': '火气渐旺，热情上升'},
    '巳酉': {'局': '金局（半合）', '五行': '金', '含义': '金气渐旺，锐气渐增'},
    # 半合（中方+墓方）
    '子辰': {'局': '水局（半合）', '五行': '水', '含义': '水气收敛，蓄势内敛'},
    '卯未': {'局': '木局（半合）', '五行': '木', '含义': '木气收敛，根深蒂固'},
    '午戌': {'局': '火局（半合）', '五行': '火', '含义': '火气收敛，内敛含蓄'},
    '酉丑': {'局': '金局（半合）', '五行': '金', '含义': '金气收敛，精打细算'},
}

# 地支三刑
SAN_XING = {
    # 无恩之刑
    '寅巳申': {'类型': '无恩之刑', '含义': '忘恩负义，恩将仇报，人际关系复杂'},
    # 恃势之刑
    '丑戌未': {'类型': '恃势之刑', '含义': '仗势欺人，自以为是，易招是非'},
    # 无礼之刑
    '子卯': {'类型': '无礼之刑', '含义': '无礼粗鲁，缺乏修养，感情不顺'},
    # 自刑
    '辰辰': {'类型': '自刑', '含义': '自我纠结，内心矛盾，自作自受'},
    '午午': {'类型': '自刑', '含义': '自我纠结，急躁冲动，自寻烦恼'},
    '酉酉': {'类型': '自刑', '含义': '自我纠结，过于挑剔，自困自缚'},
    '亥亥': {'类型': '自刑', '含义': '自我纠结，消极悲观，自我封闭'},
}

# 地支六害（六穿）
LIU_HAI = {
    '子': '未', '未': '子',
    '丑': '午', '午': '丑',
    '寅': '巳', '巳': '寅',
    '卯': '辰', '辰': '卯',
    '申': '亥', '亥': '申',
    '酉': '戌', '戌': '酉',
}

# 六害含义
LIU_HAI_MEANING = {
    ('子', '未'): '子未害：骨肉相害，亲情不和',
    ('丑', '午'): '丑午害：暗中相害，小人作祟',
    ('寅', '巳'): '寅巳害：口舌是非，意见不合',
    ('卯', '辰'): '卯辰害：暗藏危机，防小人暗算',
    ('申', '亥'): '申亥害：谋事难成，多劳少获',
    ('酉', '戌'): '酉戌害：嫉妒猜疑，感情不和',
}

# 地支相破
XIANG_PO = {
    '子': '酉', '酉': '子',
    '丑': '辰', '辰': '丑',
    '寅': '亥', '亥': '寅',
    '卯': '午', '午': '卯',
    '巳': '申', '申': '巳',
    '未': '戌', '戌': '未',
}

# 相破含义
XIANG_PO_MEANING = {
    ('子', '酉'): '子酉破：破财之象，谨防损失',
    ('丑', '辰'): '丑辰破：内部不和，合作破裂',
    ('寅', '亥'): '寅亥破：先合后破，事与愿违',
    ('卯', '午'): '卯午破：感情波动，情绪不稳',
    ('巳', '申'): '巳申破：合中带破，好事多磨',
    ('未', '戌'): '未戌破：土破之象，根基动摇',
}


class XingChongHeHai:
    """刑冲合害分析器"""

    @classmethod
    def analyze(cls, si_zhu_zhi: List[str], da_yun_zhi: Optional[List[str]] = None,
                liu_nian_zhi: Optional[str] = None) -> Dict:
        """
        综合分析四柱地支之间的刑冲合害关系
        
        Args:
            si_zhu_zhi: 四柱地支 [年支, 月支, 日支, 时支]
            da_yun_zhi: 大运地支列表（可选）
            liu_nian_zhi: 流年地支（可选）
        
        Returns:
            分析结果字典
        """
        result = {
            '六合': [],
            '六冲': [],
            '三合': [],
            '半三合': [],
            '三刑': [],
            '六害': [],
            '相破': [],
            '综合判断': '',
            '建议': [],
        }

        # 收集所有地支（四柱 + 大运 + 流年）
        all_zhi = list(si_zhu_zhi)
        zhu_names = ['年支', '月支', '日支', '时支']
        
        if da_yun_zhi:
            for dz in da_yun_zhi[:2]:  # 只看前两步大运
                all_zhi.append(dz)
                zhu_names.append(f'大运')
        
        if liu_nian_zhi:
            all_zhi.append(liu_nian_zhi)
            zhu_names.append('流年')

        # ===== 1. 检查六合 =====
        result['六合'] = cls._check_liu_he(si_zhu_zhi)
        if liu_nian_zhi:
            ln_he = cls._check_liu_he_with_target(si_zhu_zhi, liu_nian_zhi)
            result['六合'].extend(ln_he)

        # ===== 2. 检查六冲 =====
        result['六冲'] = cls._check_liu_chong(si_zhu_zhi)
        if liu_nian_zhi:
            ln_chong = cls._check_liu_chong_with_target(si_zhu_zhi, liu_nian_zhi)
            result['六冲'].extend(ln_chong)

        # ===== 3. 检查三合 =====
        result['三合'] = cls._check_san_he(si_zhu_zhi)

        # ===== 4. 检查半三合 =====
        result['半三合'] = cls._check_ban_san_he(si_zhu_zhi)

        # ===== 5. 检查三刑 =====
        result['三刑'] = cls._check_san_xing(si_zhu_zhi)

        # ===== 6. 检查六害 =====
        result['六害'] = cls._check_liu_hai(si_zhu_zhi)
        if liu_nian_zhi:
            ln_hai = cls._check_liu_hai_with_target(si_zhu_zhi, liu_nian_zhi)
            result['六害'].extend(ln_hai)

        # ===== 7. 检查相破 =====
        result['相破'] = cls._check_xiang_po(si_zhu_zhi)
        if liu_nian_zhi:
            ln_po = cls._check_xiang_po_with_target(si_zhu_zhi, liu_nian_zhi)
            result['相破'].extend(ln_po)

        # ===== 综合判断 =====
        result['综合判断'] = cls._comprehensive_judgment(result)
        result['建议'] = cls._generate_advice(result)

        return result

    # ============ 内部检查方法 ============

    @classmethod
    def _check_liu_he(cls, zhi_list: List[str]) -> List[Dict]:
        """检查四柱内部的六合关系"""
        results = []
        checked = set()
        
        for i in range(len(zhi_list)):
            for j in range(i + 1, len(zhi_list)):
                zhi1, zhi2 = zhi_list[i], zhi_list[j]
                pair = tuple(sorted([zhi1, zhi2]))
                if pair in checked:
                    continue
                
                if LIU_HE.get(zhi1) == zhi2:
                    checked.add(pair)
                    meaning_key = tuple(sorted([zhi1, zhi2]))
                    results.append({
                        '关系': f'{zhi1}{zhi2}六合',
                        '位置': cls._get_position_name(i, j),
                        '含义': LIU_HE_MEANING.get(meaning_key, f'{zhi1}{zhi2}相合，主和谐'),
                        '吉凶': '吉',
                    })
        
        return results

    @classmethod
    def _check_liu_he_with_target(cls, zhi_list: List[str], target: str) -> List[Dict]:
        """检查流年与四柱的六合"""
        results = []
        positions = ['年', '月', '日', '时']
        
        for i, zhi in enumerate(zhi_list):
            if LIU_HE.get(zhi) == target:
                meaning_key = tuple(sorted([zhi, target]))
                results.append({
                    '关系': f'流年{target}与{positions[i]}支{zhi}六合',
                    '位置': f'流年+{positions[i]}支',
                    '含义': LIU_HE_MEANING.get(meaning_key, f'流年与{positions[i]}柱相合'),
                    '吉凶': '吉',
                })
        
        return results

    @classmethod
    def _check_liu_chong(cls, zhi_list: List[str]) -> List[Dict]:
        """检查四柱内部的六冲关系"""
        results = []
        checked = set()
        
        for i in range(len(zhi_list)):
            for j in range(i + 1, len(zhi_list)):
                zhi1, zhi2 = zhi_list[i], zhi_list[j]
                pair = tuple(sorted([zhi1, zhi2]))
                if pair in checked:
                    continue
                
                if LIU_CHONG.get(zhi1) == zhi2:
                    checked.add(pair)
                    meaning_key = tuple(sorted([zhi1, zhi2]))
                    results.append({
                        '关系': f'{zhi1}{zhi2}相冲',
                        '位置': cls._get_position_name(i, j),
                        '含义': LIU_CHONG_MEANING.get(meaning_key, f'{zhi1}{zhi2}相冲，主变动'),
                        '吉凶': '凶',
                    })
        
        return results

    @classmethod
    def _check_liu_chong_with_target(cls, zhi_list: List[str], target: str) -> List[Dict]:
        """检查流年与四柱的六冲"""
        results = []
        positions = ['年', '月', '日', '时']
        
        for i, zhi in enumerate(zhi_list):
            if LIU_CHONG.get(zhi) == target:
                meaning_key = tuple(sorted([zhi, target]))
                results.append({
                    '关系': f'流年{target}冲{positions[i]}支{zhi}',
                    '位置': f'流年+{positions[i]}支',
                    '含义': LIU_CHONG_MEANING.get(meaning_key, f'流年冲{positions[i]}柱，主变动'),
                    '吉凶': '凶',
                    '注意': '流年冲柱，该柱对应领域需特别注意',
                })
        
        return results

    @classmethod
    def _check_san_he(cls, zhi_list: List[str]) -> List[Dict]:
        """检查三合局"""
        results = []
        zhi_set = set(zhi_list)
        
        for combo, info in SAN_HE.items():
            combo_zhi = list(combo)
            if all(z in zhi_set for z in combo_zhi):
                # 找出位置
                positions = []
                for z in combo_zhi:
                    idx = zhi_list.index(z)
                    positions.append(['年', '月', '日', '时'][idx])
                
                results.append({
                    '关系': f'{combo}三合{info["局"]}',
                    '位置': '/'.join(positions),
                    '五行': info['五行'],
                    '含义': info['含义'],
                    '吉凶': '吉',
                    '说明': f'三合{info["局"]}全，{info["五行"]}气旺盛',
                })
        
        return results

    @classmethod
    def _check_ban_san_he(cls, zhi_list: List[str]) -> List[Dict]:
        """检查半三合"""
        results = []
        zhi_set = set(zhi_list)
        
        for combo, info in BAN_SAN_HE.items():
            combo_zhi = list(combo)
            if len(combo_zhi) == 2 and all(z in zhi_set for z in combo_zhi):
                results.append({
                    '关系': f'{combo}{info["局"]}',
                    '位置': '四柱中',
                    '五行': info['五行'],
                    '含义': info['含义'],
                    '吉凶': '半吉',
                })
        
        return results

    @classmethod
    def _check_san_xing(cls, zhi_list: List[str]) -> List[Dict]:
        """检查三刑"""
        results = []
        zhi_set = set(zhi_list)
        
        # 检查寅巳申（无恩之刑）
        if all(z in zhi_set for z in ['寅', '巳', '申']):
            results.append({
                '关系': '寅巳申三刑',
                '类型': '无恩之刑',
                '含义': '忘恩负义，恩将仇报，人际关系复杂',
                '吉凶': '凶',
                '注意': '需注意人际关系，防小人陷害',
            })
        elif sum(1 for z in ['寅', '巳', '申'] if z in zhi_set) == 2:
            results.append({
                '关系': '寅巳申二刑（不全）',
                '类型': '无恩之刑（缺位）',
                '含义': '潜在刑伤，流年逢之则发',
                '吉凶': '半凶',
            })
        
        # 检查丑戌未（恃势之刑）
        if all(z in zhi_set for z in ['丑', '戌', '未']):
            results.append({
                '关系': '丑戌未三刑',
                '类型': '恃势之刑',
                '含义': '仗势欺人，自以为是，易招是非',
                '吉凶': '凶',
                '注意': '不可恃强凌弱，需谦虚谨慎',
            })
        elif sum(1 for z in ['丑', '戌', '未'] if z in zhi_set) == 2:
            results.append({
                '关系': '丑戌未二刑（不全）',
                '类型': '恃势之刑（缺位）',
                '含义': '潜在是非，流年逢之则发',
                '吉凶': '半凶',
            })
        
        # 检查子卯（无礼之刑）
        if '子' in zhi_set and '卯' in zhi_set:
            results.append({
                '关系': '子卯相刑',
                '类型': '无礼之刑',
                '含义': '无礼粗鲁，缺乏修养，感情不顺',
                '吉凶': '凶',
                '注意': '需注意言行举止，修身养性',
            })
        
        # 检查自刑（辰辰、午午、酉酉、亥亥）
        from collections import Counter
        zhi_count = Counter(zhi_list)
        for self_xing in ['辰', '午', '酉', '亥']:
            if zhi_count[self_xing] >= 2:
                results.append({
                    '关系': f'{self_xing}{self_xing}自刑',
                    '类型': '自刑',
                    '含义': SAN_XING.get(f'{self_xing}{self_xing}', {}).get('含义', '自我纠结'),
                    '吉凶': '凶',
                    '注意': '需注意自我调节，避免自我内耗',
                })
        
        return results

    @classmethod
    def _check_liu_hai(cls, zhi_list: List[str]) -> List[Dict]:
        """检查六害"""
        results = []
        checked = set()
        
        for i in range(len(zhi_list)):
            for j in range(i + 1, len(zhi_list)):
                zhi1, zhi2 = zhi_list[i], zhi_list[j]
                pair = tuple(sorted([zhi1, zhi2]))
                if pair in checked:
                    continue
                
                if LIU_HAI.get(zhi1) == zhi2:
                    checked.add(pair)
                    meaning_key = tuple(sorted([zhi1, zhi2]))
                    results.append({
                        '关系': f'{zhi1}{zhi2}相害',
                        '位置': cls._get_position_name(i, j),
                        '含义': LIU_HAI_MEANING.get(meaning_key, f'{zhi1}{zhi2}相害，主不和'),
                        '吉凶': '凶',
                    })
        
        return results

    @classmethod
    def _check_liu_hai_with_target(cls, zhi_list: List[str], target: str) -> List[Dict]:
        """检查流年与四柱的六害"""
        results = []
        positions = ['年', '月', '日', '时']
        
        for i, zhi in enumerate(zhi_list):
            if LIU_HAI.get(zhi) == target:
                meaning_key = tuple(sorted([zhi, target]))
                results.append({
                    '关系': f'流年{target}害{positions[i]}支{zhi}',
                    '位置': f'流年+{positions[i]}支',
                    '含义': LIU_HAI_MEANING.get(meaning_key, f'流年与{positions[i]}柱相害'),
                    '吉凶': '凶',
                })
        
        return results

    @classmethod
    def _check_xiang_po(cls, zhi_list: List[str]) -> List[Dict]:
        """检查相破"""
        results = []
        checked = set()
        
        for i in range(len(zhi_list)):
            for j in range(i + 1, len(zhi_list)):
                zhi1, zhi2 = zhi_list[i], zhi_list[j]
                pair = tuple(sorted([zhi1, zhi2]))
                if pair in checked:
                    continue
                
                if XIANG_PO.get(zhi1) == zhi2:
                    checked.add(pair)
                    meaning_key = tuple(sorted([zhi1, zhi2]))
                    results.append({
                        '关系': f'{zhi1}{zhi2}相破',
                        '位置': cls._get_position_name(i, j),
                        '含义': XIANG_PO_MEANING.get(meaning_key, f'{zhi1}{zhi2}相破，主破损'),
                        '吉凶': '凶',
                    })
        
        return results

    @classmethod
    def _check_xiang_po_with_target(cls, zhi_list: List[str], target: str) -> List[Dict]:
        """检查流年与四柱的相破"""
        results = []
        positions = ['年', '月', '日', '时']
        
        for i, zhi in enumerate(zhi_list):
            if XIANG_PO.get(zhi) == target:
                meaning_key = tuple(sorted([zhi, target]))
                results.append({
                    '关系': f'流年{target}破{positions[i]}支{zhi}',
                    '位置': f'流年+{positions[i]}支',
                    '含义': XIANG_PO_MEANING.get(meaning_key, f'流年与{positions[i]}柱相破'),
                    '吉凶': '凶',
                })
        
        return results

    # ============ 工具方法 ============

    @classmethod
    def _get_position_name(cls, i: int, j: int) -> str:
        """获取位置名称"""
        positions = ['年', '月', '日', '时']
        return f'{positions[i]}-{positions[j]}'

    @classmethod
    def _comprehensive_judgment(cls, result: Dict) -> str:
        """综合判断"""
        judgments = []
        
        # 统计吉凶数量
        ji_count = len(result['六合']) + len(result['三合'])
        xiong_count = len(result['六冲']) + len(result['三刑']) + len(result['六害']) + len(result['相破'])
        
        # 日支特殊判断
        ri_zhi_chong = any('日' in item.get('位置', '') for item in result['六冲'])
        ri_zhi_he = any('日' in item.get('位置', '') for item in result['六合'])
        ri_zhi_xing = any('日' in item.get('位置', '') or '日' in item.get('类型', '')
                         for item in result['三刑'])
        
        if ri_zhi_chong:
            judgments.append('日支逢冲，婚姻感情需特别注意，易有变动')
        if ri_zhi_he:
            judgments.append('日支逢合，感情和睦，人际和谐')
        if ri_zhi_xing:
            judgments.append('日支逢刑，内心纠结，自我消耗较重')
        
        if result['三合']:
            san_he_types = [item['五行'] for item in result['三合']]
            judgments.append(f'三合局成（{",".join(san_he_types)}），气势强旺')
        
        if result['六合']:
            n_he = len(result['六合'])
            judgments.append(f'命中有合（{n_he}组），人缘佳，贵人多')
        
        if result['六冲']:
            n_chong = len(result['六冲'])
            judgments.append(f'命中有冲（{n_chong}组），一生变动较多')
        
        if result['三刑']:
            n_xing = len(result['三刑'])
            judgments.append(f'命中带刑（{n_xing}组），需谨慎处事')
        
        if not judgments:
            judgments.append('命局平和，无明显刑冲合害，一生较为平稳')
        
        return '；'.join(judgments) + '。'

    @classmethod
    def _generate_advice(cls, result: Dict) -> List[str]:
        """根据刑冲合害生成建议"""
        advice = []
        
        # 日支逢冲
        if any('日' in item.get('位置', '') for item in result['六冲']):
            advice.append('婚姻宫逢冲，宜晚婚，择偶需谨慎')
            advice.append('感情中多包容理解，避免冲动行事')
        
        # 三合局
        if result['三合']:
            advice.append('三合局成，可借势而为，发挥所长')
        
        # 六冲多
        if len(result['六冲']) >= 2:
            advice.append('命局冲多，一生多变动，宜顺应时势')
        
        # 三刑
        if result['三刑']:
            advice.append('命局带刑，处事需谨慎，防小人暗算')
        
        # 六害
        if result['六害']:
            advice.append('命局带害，人际关系需用心经营')
        
        if not advice:
            advice.append('命局和谐，顺势而为即可')
        
        return advice

    @classmethod
    def format_output(cls, result: Dict) -> str:
        """格式化输出"""
        lines = []
        lines.append('【刑冲合害分析】')
        
        if result['六合']:
            lines.append('  ◈ 六合（和谐之象）：')
            for item in result['六合']:
                lines.append(f'    {item["关系"]}（{item["位置"]}）— {item["含义"]}')
        
        if result['六冲']:
            lines.append('  ◆ 六冲（变动之象）：')
            for item in result['六冲']:
                lines.append(f'    {item["关系"]}（{item["位置"]}）— {item["含义"]}')
        
        if result['三合']:
            lines.append('  ◈ 三合（气势之象）：')
            for item in result['三合']:
                lines.append(f'    {item["关系"]}（{item["位置"]}）— {item["含义"]}')
        
        if result['半三合']:
            lines.append('  ◇ 半三合：')
            for item in result['半三合']:
                lines.append(f'    {item["关系"]} — {item["含义"]}')
        
        if result['三刑']:
            lines.append('  ⚡ 三刑（刑伤之象）：')
            for item in result['三刑']:
                lines.append(f'    {item["关系"]}（{item["类型"]}）— {item["含义"]}')
        
        if result['六害']:
            lines.append('  ⚠ 六害（不和之象）：')
            for item in result['六害']:
                lines.append(f'    {item["关系"]}（{item["位置"]}）— {item["含义"]}')
        
        if result['相破']:
            lines.append('  ⚠ 相破（破损之象）：')
            for item in result['相破']:
                lines.append(f'    {item["关系"]}（{item["位置"]}）— {item["含义"]}')
        
        if not any([result['六合'], result['六冲'], result['三合'], 
                    result['半三合'], result['三刑'], result['六害'], result['相破']]):
            lines.append('  四柱地支无明显刑冲合害关系，命局平和。')
        
        lines.append('')
        lines.append(f'【综合判断】{result["综合判断"]}')
        
        if result['建议']:
            lines.append('【建议】')
            for a in result['建议']:
                lines.append(f'  • {a}')
        
        return '\n'.join(lines)


# ============ 便捷函数 ============

def analyze_xing_chong_he_hai(si_zhu_zhi: List[str], liu_nian_zhi: Optional[str] = None) -> Dict:
    """便捷函数：分析刑冲合害"""
    return XingChongHeHai.analyze(si_zhu_zhi, liu_nian_zhi=liu_nian_zhi)


if __name__ == '__main__':
    # 测试
    import json
    
    # 测试案例：庚午 壬午 庚戌 庚辰
    test_zhi = ['午', '午', '戌', '辰']
    
    result = analyze_xing_chong_he_hai(test_zhi)
    print(XingChongHeHai.format_output(result))
    
    print('\n' + '=' * 50 + '\n')
    
    # 测试案例：带三合
    test_zhi2 = ['申', '子', '辰', '酉']
    result2 = analyze_xing_chong_he_hai(test_zhi2)
    print(XingChongHeHai.format_output(result2))
