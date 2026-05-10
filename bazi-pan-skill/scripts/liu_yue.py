#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命理 流月推算模块 v1.0.0
天工长老开发 - v4.0.0 核心新功能

功能：
- 计算指定年份12个月的流月干支
- 每月运势分析（事业/财运/感情/健康）
- 月令与日主关系判断
- 每月吉凶评分
"""

from typing import Dict, List, Optional, Tuple

# ============== 基础数据 ==============

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

GAN_YIN_YANG = {
    '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
    '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'
}

# 流月地支固定（以节气为界）
# 正月寅月（立春~惊蛰），二月卯月（惊蛰~清明）...
LIU_YUE_ZHI = {
    1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
    7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑',
}

# 月份名称
YUE_NAMES = {
    1: '正月（寅月）', 2: '二月（卯月）', 3: '三月（辰月）',
    4: '四月（巳月）', 5: '五月（午月）', 6: '六月（未月）',
    7: '七月（申月）', 8: '八月（酉月）', 9: '九月（戌月）',
    10: '十月（亥月）', 11: '十一月（子月）', 12: '十二月（丑月）',
}

# 月令五行旺衰表（以月令判断五行状态）
WUXING_WANG_SHUAI = {
    # 月令: 木 火 土 金 水
    '寅': {'木': '旺', '火': '相', '土': '死', '金': '囚', '水': '休'},
    '卯': {'木': '旺', '火': '相', '土': '死', '金': '囚', '水': '休'},
    '辰': {'木': '余', '火': '相', '土': '旺', '金': '相', '水': '囚'},
    '巳': {'木': '休', '火': '旺', '土': '相', '金': '死', '水': '囚'},
    '午': {'木': '休', '火': '旺', '土': '相', '金': '死', '水': '囚'},
    '未': {'木': '囚', '火': '余', '土': '旺', '金': '相', '水': '死'},
    '申': {'木': '死', '火': '囚', '土': '休', '金': '旺', '水': '相'},
    '酉': {'木': '死', '火': '囚', '土': '休', '金': '旺', '水': '相'},
    '戌': {'木': '囚', '火': '墓', '土': '旺', '金': '相', '水': '死'},
    '亥': {'木': '相', '火': '死', '土': '囚', '金': '休', '水': '旺'},
    '子': {'木': '相', '火': '死', '土': '囚', '金': '休', '水': '旺'},
    '丑': {'木': '囚', '火': '墓', '土': '旺', '金': '墓', '水': '余'},
}

# 十神判断
def get_shi_shen(day_gan: str, other_gan: str) -> str:
    """根据日干计算十神"""
    day_wuxing = GAN_WUXING[day_gan]
    day_yin_yang = GAN_YIN_YANG[day_gan]
    other_wuxing = GAN_WUXING[other_gan]
    other_yin_yang = GAN_YIN_YANG[other_gan]
    
    if day_wuxing == other_wuxing:
        return '比肩' if day_yin_yang == other_yin_yang else '劫财'
    
    wuxing_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    if wuxing_sheng.get(day_wuxing) == other_wuxing:
        return '食神' if day_yin_yang == other_yin_yang else '伤官'
    
    wuxing_ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
    if wuxing_ke.get(day_wuxing) == other_wuxing:
        return '偏财' if day_yin_yang == other_yin_yang else '正财'
    
    reverse_ke = {'土': '木', '金': '火', '水': '土', '木': '金', '火': '水'}
    if reverse_ke.get(day_wuxing) == other_wuxing:
        return '七杀' if day_yin_yang == other_yin_yang else '正官'
    
    reverse_sheng = {'火': '木', '土': '火', '金': '土', '水': '金', '木': '水'}
    if reverse_sheng.get(day_wuxing) == other_wuxing:
        return '偏印' if day_yin_yang == other_yin_yang else '正印'
    
    return '未知'


class LiuYueCalculator:
    """流月推算器"""

    @classmethod
    def get_liu_yue_gan_zhi(cls, year: int, month: int, year_gan: Optional[str] = None) -> Tuple[str, str]:
        """
        获取指定年月的流月干支
        
        Args:
            year: 公历年份
            month: 月份(1-12)
            year_gan: 流年天干（可选，如不传则自动计算）
        """
        if year_gan is None:
            year_gan = TIAN_GAN[(year - 4) % 10]
        
        # 流月地支
        month_zhi = LIU_YUE_ZHI[month]
        month_zhi_index = DI_ZHI.index(month_zhi)
        
        # 流月天干：五虎遁
        # 甲己之年丙作首，乙庚之年戊为头
        # 丙辛之岁寻庚上，丁壬壬寅顺水流
        # 若问戊癸何处起，甲寅之上好追求
        year_gan_index = TIAN_GAN.index(year_gan)
        start_map = {0: 2, 1: 2, 2: 4, 3: 4, 4: 6, 5: 6, 6: 8, 7: 8, 8: 0, 9: 0}
        start_gan_index = start_map.get(year_gan_index, 2)
        
        # 从寅月开始推算
        month_gan_index = (start_gan_index + month - 1) % 10
        month_gan = TIAN_GAN[month_gan_index]
        
        return month_gan, month_zhi

    @classmethod
    def calculate_monthly_fortune(cls, day_gan: str, si_zhu: Dict, yong_shen: Dict,
                                   year: int, liu_nian_gan: str, liu_nian_zhi: str) -> List[Dict]:
        """
        计算12个月流月运势
        
        Args:
            day_gan: 日主天干
            si_zhu: 四柱字典
            yong_shen: 用神信息
            year: 流年年份
            liu_nian_gan: 流年天干
            liu_nian_zhi: 流年地支
        """
        months = []
        
        for month_num in range(1, 13):
            month_gan, month_zhi = cls.get_liu_yue_gan_zhi(year, month_num, liu_nian_gan)
            month_ganzhi = month_gan + month_zhi
            
            # 月令十神（以月干对日干）
            month_shi_shen = get_shi_shen(day_gan, month_gan)
            
            # 月令地支对日主的十神（以藏干主气）
            zhu_cang_gan = ZHI_CANG_GAN.get(month_zhi, [''])[0]
            month_zhi_shi_shen = get_shi_shen(day_gan, zhu_cang_gan) if zhu_cang_gan else ''
            
            # 五行旺衰
            day_wuxing = GAN_WUXING[day_gan]
            wang_shuai = WUXING_WANG_SHUAI.get(month_zhi, {}).get(day_wuxing, '平')
            
            # 月令与喜用关系
            month_wuxing = ZHI_WUXING[month_zhi]
            xi_yong = yong_shen.get('喜用', [])
            is_xi_yong = month_wuxing in xi_yong
            
            # 月令与日主关系
            is_sheng_day = WUXING_SHENG.get(month_wuxing) == day_wuxing
            is_ke_day = WUXING_KE.get(day_wuxing) == month_wuxing
            is_day_ke = WUXING_KE.get(month_wuxing) == day_wuxing
            
            # 月令与流年关系
            is_chong_liu_nian = LIU_CHONG.get(month_zhi) == liu_nian_zhi
            is_he_liu_nian = LIU_HE.get(month_zhi) == liu_nian_zhi
            
            # 月令与日支关系
            ri_zhi = si_zhu.get('日柱', ('', ''))[1]
            is_chong_ri_zhi = LIU_CHONG.get(month_zhi) == ri_zhi
            is_he_ri_zhi = LIU_HE.get(month_zhi) == ri_zhi
            
            # 综合评分
            score = cls._calculate_month_score(
                day_gan, day_wuxing, month_gan, month_zhi, 
                wang_shuai, is_xi_yong, is_sheng_day, is_ke_day, is_day_ke,
                is_chong_liu_nian, is_he_liu_nian, is_chong_ri_zhi, is_he_ri_zhi,
                month_shi_shen
            )
            
            # 生成断语
            duan_yu = cls._generate_month_duan_yu(
                day_gan, day_wuxing, month_ganzhi, month_shi_shen, month_zhi_shi_shen,
                wang_shuai, is_xi_yong, score, is_chong_ri_zhi, is_he_ri_zhi,
                is_chong_liu_nian, is_he_liu_nian
            )
            
            # 分类运势
            career = cls._career_advice(month_shi_shen, wang_shuai, is_xi_yong)
            wealth = cls._wealth_advice(month_shi_shen, is_xi_yong, score)
            love = cls._love_advice(month_shi_shen, is_chong_ri_zhi, is_he_ri_zhi, is_xi_yong)
            health = cls._health_advice(month_zhi, wang_shuai, day_wuxing)
            
            months.append({
                '月份': month_num,
                '月名': YUE_NAMES[month_num],
                '流月干支': month_ganzhi,
                '月干十神': month_shi_shen,
                '月支十神': month_zhi_shi_shen,
                '日主旺衰': wang_shuai,
                '是否喜用': is_xi_yong,
                '吉凶评分': score,
                '综合断语': duan_yu,
                '事业': career,
                '财运': wealth,
                '感情': love,
                '健康': health,
            })
        
        return months

    @classmethod
    def _calculate_month_score(cls, day_gan: str, day_wuxing: str,
                                month_gan: str, month_zhi: str,
                                wang_shuai: str, is_xi_yong: bool,
                                is_sheng_day: bool, is_ke_day: bool, is_day_ke: bool,
                                is_chong_liu_nian: bool, is_he_liu_nian: bool,
                                is_chong_ri_zhi: bool, is_he_ri_zhi: bool,
                                month_shi_shen: str) -> int:
        """计算月份吉凶评分 (0-100)"""
        score = 50  # 基础分
        
        # 喜用月加分
        if is_xi_yong:
            score += 15
        
        # 生助日主加分
        if is_sheng_day:
            score += 10
        
        # 克泄日主减分
        if is_ke_day:
            score -= 10
        
        # 日主克月令（耗身）
        if is_day_ke:
            score -= 5
        
        # 旺衰调整
        wang_shuai_scores = {'旺': 5, '相': 10, '休': 0, '囚': -5, '死': -10, '余': 3, '墓': -5, '平': 0}
        score += wang_shuai_scores.get(wang_shuai, 0)
        
        # 与流年关系
        if is_he_liu_nian:
            score += 8
        if is_chong_liu_nian:
            score -= 8
        
        # 与日支关系
        if is_he_ri_zhi:
            score += 5
        if is_chong_ri_zhi:
            score -= 10
        
        # 吉神加分
        if month_shi_shen in ['正官', '正印', '食神', '正财']:
            score += 5
        if month_shi_shen in ['七杀', '伤官', '劫财']:
            score -= 5
        
        return max(0, min(100, score))

    @classmethod
    def _generate_month_duan_yu(cls, day_gan: str, day_wuxing: str, month_ganzhi: str,
                                 month_shi_shen: str, month_zhi_shi_shen: str,
                                 wang_shuai: str, is_xi_yong: bool, score: int,
                                 is_chong_ri_zhi: bool, is_he_ri_zhi: bool,
                                 is_chong_liu_nian: bool, is_he_liu_nian: bool) -> str:
        """生成月份综合断语"""
        parts = []
        
        # 十神基调
        shi_shen_duan = {
            '正官': '事业顺利，名利双收',
            '七杀': '压力较大，需防小人',
            '正印': '学业有利，贵人相助',
            '偏印': '思维活跃，宜研究学习',
            '正财': '财运稳定，收入可期',
            '偏财': '财运波动，投资需谨慎',
            '食神': '心情愉悦，才华展现',
            '伤官': '创意丰富，注意口舌',
            '比肩': '独立自主，合作有利',
            '劫财': '竞争加剧，谨防破财',
        }
        parts.append(shi_shen_duan.get(month_shi_shen, '运势平稳'))
        
        # 旺衰补充
        if wang_shuai in ['旺', '相']:
            parts.append('精气充沛')
        elif wang_shuai in ['死', '囚']:
            parts.append('精力稍弱，注意调养')
        
        # 喜用补充
        if is_xi_yong:
            parts.append('逢喜用之月，诸事较顺')
        
        # 特殊关系
        if is_chong_ri_zhi:
            parts.append('月冲日支，感情易有波折')
        if is_he_ri_zhi:
            parts.append('月合日支，感情和睦')
        if is_chong_liu_nian:
            parts.append('月冲流年，变动之象')
        
        if score >= 70:
            overall = '本月运势上佳'
        elif score >= 55:
            overall = '本月运势平稳'
        elif score >= 40:
            overall = '本月运势偏弱'
        else:
            overall = '本月运势低迷，宜静不宜动'
        
        return f'{overall}。{"；".join(parts)}。'

    @classmethod
    def _career_advice(cls, month_shi_shen: str, wang_shuai: str, is_xi_yong: bool) -> str:
        """事业建议"""
        if month_shi_shen in ['正官', '正印'] and is_xi_yong:
            return '事业大好，宜积极争取升职加薪'
        elif month_shi_shen == '食神':
            return '才华横溢，利创作、策划、展示'
        elif month_shi_shen == '伤官':
            return '创意丰富，但注意职场人际关系'
        elif month_shi_shen == '七杀':
            return '压力与机遇并存，宜迎难而上'
        elif month_shi_shen == '比肩':
            return '利合作共事，团队精神佳'
        elif wang_shuai in ['旺', '相']:
            return '状态良好，可推进重要项目'
        else:
            return '稳扎稳打，不宜冒进'

    @classmethod
    def _wealth_advice(cls, month_shi_shen: str, is_xi_yong: bool, score: int) -> str:
        """财运建议"""
        if month_shi_shen in ['正财', '偏财'] and is_xi_yong:
            return '财运亨通，正偏财皆有利'
        elif month_shi_shen == '正财':
            return '正财稳定，工资收入可期'
        elif month_shi_shen == '偏财':
            return '偏财有机会，但需理性投资'
        elif month_shi_shen == '劫财':
            return '谨防破财，不宜大额支出'
        elif score >= 65:
            return '财运尚可，适度消费'
        else:
            return '财运平淡，宜量入为出'

    @classmethod
    def _love_advice(cls, month_shi_shen: str, is_chong_ri_zhi: bool, 
                      is_he_ri_zhi: bool, is_xi_yong: bool) -> str:
        """感情建议"""
        if is_chong_ri_zhi:
            return '感情宫受冲，需多沟通包容'
        if is_he_ri_zhi:
            return '感情宫逢合，甜蜜和谐'
        
        if month_shi_shen in ['正财'] and is_xi_yong:
            return '男命利感情发展'
        if month_shi_shen in ['正官'] and is_xi_yong:
            return '女命利感情发展'
        if month_shi_shen in ['桃花', '红艳']:
            return '桃花旺盛，单身者有机会'
        
        return '感情平稳，用心经营即可'

    @classmethod
    def _health_advice(cls, month_zhi: str, wang_shuai: str, day_wuxing: str) -> str:
        """健康建议"""
        wuxing_organs = {
            '木': '肝胆、筋骨、眼睛',
            '火': '心脏、血液、小肠',
            '土': '脾胃、皮肤、肌肉',
            '金': '肺部、呼吸道、大肠',
            '水': '肾脏、泌尿系统、耳朵',
        }
        
        if wang_shuai in ['死', '囚']:
            organ = wuxing_organs.get(day_wuxing, '身体')
            return f'{day_wuxing}气偏弱，注意{organ}保养'
        
        month_organ = wuxing_organs.get(ZHI_WUXING[month_zhi], '')
        if month_organ:
            return f'月令{ZHI_WUXING[month_zhi]}旺，注意{month_organ}'
        
        return '注意作息规律，保持健康'

    @classmethod
    def format_output(cls, months: List[Dict], highlight_best: bool = True) -> str:
        """格式化输出流月运势"""
        lines = []
        lines.append('【流月运势】')
        lines.append('')
        
        # 找出最好和最差的月份
        if highlight_best:
            best = max(months, key=lambda m: m['吉凶评分'])
            worst = min(months, key=lambda m: m['吉凶评分'])
        
        for m in months:
            score = m['吉凶评分']
            indicator = '🟢' if score >= 65 else ('🟡' if score >= 45 else '🔴')
            
            # 标记最好最差
            tag = ''
            if highlight_best:
                if m['月份'] == best['月份']:
                    tag = ' ★最佳'
                elif m['月份'] == worst['月份']:
                    tag = ' ☆需注意'
            
            lines.append(f'  {indicator} {m["月名"]} — {m["流月干支"]}（{m["月干十神"]}） 评分:{score}{tag}')
            lines.append(f'     {m["综合断语"]}')
            lines.append(f'     事业：{m["事业"]} | 财运：{m["财运"]}')
            lines.append(f'     感情：{m["感情"]} | 健康：{m["健康"]}')
            lines.append('')
        
        return '\n'.join(lines)


# 五行生克
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
LIU_CHONG = {'子': '午', '午': '子', '丑': '未', '未': '丑', '寅': '申', '申': '寅',
             '卯': '酉', '酉': '卯', '辰': '戌', '戌': '辰', '巳': '亥', '亥': '巳'}
LIU_HE = {'子': '丑', '丑': '子', '寅': '亥', '亥': '寅', '卯': '戌', '戌': '卯',
          '辰': '酉', '酉': '辰', '巳': '申', '申': '巳', '午': '未', '未': '午'}

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


if __name__ == '__main__':
    import json
    
    # 测试案例
    test_si_zhu = {
        '年柱': ('庚', '午'),
        '月柱': ('壬', '午'),
        '日柱': ('庚', '戌'),
        '时柱': ('庚', '辰'),
    }
    
    test_yong_shen = {'喜用': ['水', '木'], '日主五行': '金', '旺衰': '旺'}
    
    months = LiuYueCalculator.calculate_monthly_fortune(
        day_gan='庚',
        si_zhu=test_si_zhu,
        yong_shen=test_yong_shen,
        year=2026,
        liu_nian_gan='丙',
        liu_nian_zhi='午',
    )
    
    print(LiuYueCalculator.format_output(months))
