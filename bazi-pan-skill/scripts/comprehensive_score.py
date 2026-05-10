#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命理 综合评分与趋吉避凶模块 v1.0.0
天工长老开发 - v4.0.0 核心新功能

功能：
- 多维度综合评分（0-100分）
- 趋吉避凶建议（吉利方位/颜色/行业/数字/吉祥物）
- 五行补救建议
- 人生大运走势分析
"""

from typing import Dict, List, Optional, Tuple

# ============== 基础数据 ==============

GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 五行对应的吉利方位
WUXING_DIRECTIONS = {
    '木': {'方位': '东方、东南方', '详细': ['正东', '东南']},
    '火': {'方位': '南方', '详细': ['正南']},
    '土': {'方位': '中央、东北方、西南方', '详细': ['中央', '东北', '西南']},
    '金': {'方位': '西方、西北方', '详细': ['正西', '西北']},
    '水': {'方位': '北方', '详细': ['正北']},
}

# 五行对应的吉利颜色
WUXING_COLORS = {
    '木': ['绿色', '青色', '翠色'],
    '火': ['红色', '紫色', '粉色', '橙色'],
    '土': ['黄色', '棕色', '米色', '咖啡色'],
    '金': ['白色', '金色', '银色'],
    '水': ['黑色', '蓝色', '灰色'],
}

# 五行对应的行业
WUXING_INDUSTRIES = {
    '木': ['教育', '文化出版', '园林绿化', '服装纺织', '医药', '家具'],
    '火': ['能源化工', '餐饮', '娱乐传媒', '电子科技', '美容美发', '照明'],
    '土': ['房地产', '建筑工程', '农业', '陶瓷石材', '仓储物流', '矿产'],
    '金': ['金融保险', '机械制造', '珠宝首饰', '金属加工', '法律', '军警'],
    '水': ['贸易', '物流运输', '旅游', '餐饮酒水', '清洁', '水产'],
}

# 五行对应的吉利数字
WUXING_NUMBERS = {
    '木': ['3', '8', '13', '18', '23', '28', '33', '38'],
    '火': ['2', '7', '12', '17', '22', '27', '32', '37'],
    '土': ['5', '0', '10', '15', '20', '25', '30', '35'],
    '金': ['4', '9', '14', '19', '24', '29', '34', '39'],
    '水': ['1', '6', '11', '16', '21', '26', '31', '36'],
}

# 五行对应的吉祥物
WUXING_LUCKY_ITEMS = {
    '木': ['绿植', '木质手串', '翡翠', '绿幽灵水晶', '竹制品'],
    '火': ['红玛瑙', '紫水晶', '太阳石', '红色饰品', '蜡烛'],
    '土': ['黄水晶', '琥珀', '陶瓷饰品', '玉石', '玛瑙'],
    '金': ['金银饰品', '白水晶', '珍珠', '金属饰品', '钻石'],
    '水': ['黑曜石', '蓝宝石', '海蓝宝', '鱼缸', '流水摆件'],
}

# 五行对应的食物
WUXING_FOODS = {
    '木': ['绿色蔬菜', '水果', '坚果', '豆芽', '绿茶'],
    '火': ['红豆', '红枣', '西红柿', '辣椒', '羊肉'],
    '土': ['小米', '南瓜', '山药', '土豆', '黄豆'],
    '金': ['白萝卜', '百合', '银耳', '梨', '鸡肉'],
    '水': ['黑豆', '黑芝麻', '海带', '鱼类', '黑木耳'],
}

# 格局加分
GE_JU_SCORES = {
    '正官格': 18,
    '正印格': 16,
    '食神格': 14,
    '正财格': 14,
    '偏财格': 10,
    '七杀格': 8,
    '偏印格': 8,
    '伤官格': 6,
    '建禄格': 10,
    '羊刃格': 5,
}


class ComprehensiveScorer:
    """综合评分计算器"""

    @classmethod
    def calculate_score(cls, si_zhu: Dict, wuxing_count: Dict, ge_ju: Optional[str],
                        yong_shen: Dict, shen_sha_result: Optional[Dict] = None,
                        xing_chong_result: Optional[Dict] = None) -> Dict:
        """
        计算八字综合评分（多维度）
        
        Returns:
            {
                '总分': int,
                '等级': str,
                '分项评分': {
                    '五行平衡': int,
                    '格局优劣': int,
                    '用神有力': int,
                    '神煞吉凶': int,
                    '刑冲合害': int,
                    '日主强弱': int,
                },
                '等级说明': str,
            }
        """
        # 1. 五行平衡评分 (0-20)
        wuxing_balance = cls._score_wuxing_balance(wuxing_count)
        
        # 2. 格局评分 (0-18)
        ge_ju_score = cls._score_ge_ju(ge_ju)
        
        # 3. 用神有力评分 (0-18)
        yong_shen_score = cls._score_yong_shen(yong_shen, si_zhu)
        
        # 4. 神煞吉凶评分 (0-16)
        shen_sha_score = cls._score_shen_sha(shen_sha_result)
        
        # 5. 刑冲合害评分 (0-14)
        xing_chong_score = cls._score_xing_chong(xing_chong_result)
        
        # 6. 日主强弱评分 (0-14)
        day_strength_score = cls._score_day_strength(yong_shen, wuxing_count)
        
        total = wuxing_balance + ge_ju_score + yong_shen_score + shen_sha_score + xing_chong_score + day_strength_score
        
        # 确定等级
        grade, grade_desc = cls._get_grade(total)
        
        return {
            '总分': total,
            '等级': grade,
            '分项评分': {
                '五行平衡': wuxing_balance,
                '格局优劣': ge_ju_score,
                '用神有力': yong_shen_score,
                '神煞吉凶': shen_sha_score,
                '刑冲合害': xing_chong_score,
                '日主强弱': day_strength_score,
            },
            '等级说明': grade_desc,
        }

    @classmethod
    def _score_wuxing_balance(cls, wuxing_count: Dict) -> int:
        """五行平衡评分"""
        counts = list(wuxing_count.values())
        if not any(counts):
            return 10
        
        avg = sum(counts) / 5
        max_diff = max(abs(c - avg) for c in counts)
        
        if max_diff <= 0.5:
            return 20  # 完美平衡
        elif max_diff <= 1:
            return 16  # 基本平衡
        elif max_diff <= 1.5:
            return 12  # 略有偏差
        elif max_diff <= 2:
            return 8   # 偏差较大
        else:
            return 4   # 严重失衡

    @classmethod
    def _score_ge_ju(cls, ge_ju: Optional[str]) -> int:
        """格局评分"""
        if not ge_ju:
            return 8  # 无明确格局
        
        return GE_JU_SCORES.get(ge_ju, 10)

    @classmethod
    def _score_yong_shen(cls, yong_shen: Dict, si_zhu: Dict) -> int:
        """用神有力评分"""
        if not yong_shen:
            return 8
        
        wang_shuai = yong_shen.get('旺衰', '')
        xi_yong = yong_shen.get('喜用', [])
        
        score = 10
        
        # 用神是否在四柱中出现
        si_zhu_zhi = [si_zhu['年柱'][1], si_zhu['月柱'][1], 
                      si_zhu['日柱'][1], si_zhu['时柱'][1]]
        si_zhu_gan = [si_zhu['年柱'][0], si_zhu['月柱'][0], 
                      si_zhu['日柱'][0], si_zhu['时柱'][0]]
        
        for wx in xi_yong:
            # 检查天干
            for gan in si_zhu_gan:
                if GAN_WUXING[gan] == wx:
                    score += 3
                    break
            # 检查地支
            for zhi in si_zhu_zhi:
                if ZHI_WUXING[zhi] == wx:
                    score += 2
                    break
        
        return min(18, score)

    @classmethod
    def _score_shen_sha(cls, shen_sha_result: Optional[Dict]) -> int:
        """神煞吉凶评分"""
        if not shen_sha_result:
            return 8  # 默认分
        
        ji_count = shen_sha_result.get('吉神数', 0)
        xiong_count = shen_sha_result.get('凶煞数', 0)
        
        score = 8 + ji_count * 2 - xiong_count
        
        return max(0, min(16, score))

    @classmethod
    def _score_xing_chong(cls, xing_chong_result: Optional[Dict]) -> int:
        """刑冲合害评分"""
        if not xing_chong_result:
            return 10  # 默认分
        
        score = 14
        
        # 合多加分
        he_count = len(xing_chong_result.get('六合', [])) + len(xing_chong_result.get('三合', []))
        score += he_count * 1
        
        # 冲减分
        chong_count = len(xing_chong_result.get('六冲', []))
        score -= chong_count * 2
        
        # 刑减分
        xing_count = len(xing_chong_result.get('三刑', []))
        score -= xing_count * 2
        
        # 害减分
        hai_count = len(xing_chong_result.get('六害', []))
        score -= hai_count * 1
        
        # 破减分
        po_count = len(xing_chong_result.get('相破', []))
        score -= po_count * 1
        
        return max(0, min(14, score))

    @classmethod
    def _score_day_strength(cls, yong_shen: Dict, wuxing_count: Dict) -> int:
        """日主强弱评分"""
        if not yong_shen:
            return 7
        
        wang_shuai = yong_shen.get('旺衰', '')
        
        if wang_shuai == '旺':
            return 12  # 日主有力
        elif wang_shuai == '相':
            return 10
        elif wang_shuai == '弱':
            return 8   # 日主偏弱，但有发挥空间
        else:
            return 7

    @classmethod
    def _get_grade(cls, total: int) -> Tuple[str, str]:
        """根据总分确定等级"""
        if total >= 85:
            return '上上', '命格极佳，一生顺遂，贵人相助，事业有成'
        elif total >= 75:
            return '上吉', '命格优良，运势良好，努力必有回报'
        elif total >= 65:
            return '中上', '命格中上，运势较好，把握机遇可获成功'
        elif total >= 55:
            return '中平', '命格中等，运势平稳，需自身努力方有成就'
        elif total >= 45:
            return '中下', '命格偏弱，多遇波折，需加倍努力'
        elif total >= 35:
            return '下平', '命格较差，困难较多，当修身养性，积善改运'
        else:
            return '下下', '命格不佳，逆境较多，宜保守处世，积德修善'


class TrendAdvisor:
    """趋吉避凶建议生成器"""

    @classmethod
    def generate_advice(cls, yong_shen: Dict, wuxing_count: Dict,
                        si_zhu: Dict, day_gan: str, 
                        xing_chong_result: Optional[Dict] = None) -> Dict:
        """
        生成趋吉避凶建议
        """
        xi_yong = yong_shen.get('喜用', ['木', '火', '土', '金', '水'])
        ji_shen = yong_shen.get('忌神', [])
        day_wuxing = GAN_WUXING[day_gan]
        
        # 吉利方位
        lucky_directions = []
        for wx in xi_yong:
            if wx in WUXING_DIRECTIONS:
                lucky_directions.extend(WUXING_DIRECTIONS[wx]['详细'])
        
        # 吉利颜色
        lucky_colors = []
        for wx in xi_yong:
            if wx in WUXING_COLORS:
                lucky_colors.extend(WUXING_COLORS[wx])
        
        # 吉利行业
        lucky_industries = []
        for wx in xi_yong:
            if wx in WUXING_INDUSTRIES:
                lucky_industries.extend(WUXING_INDUSTRIES[wx])
        
        # 吉利数字
        lucky_numbers = []
        for wx in xi_yong:
            if wx in WUXING_NUMBERS:
                lucky_numbers.extend(WUXING_NUMBERS[wx][:4])  # 取4个
        
        # 吉祥物
        lucky_items = []
        for wx in xi_yong:
            if wx in WUXING_LUCKY_ITEMS:
                lucky_items.extend(WUXING_LUCKY_ITEMS[wx][:2])
        
        # 吉利食物
        lucky_foods = []
        for wx in xi_yong:
            if wx in WUXING_FOODS:
                lucky_foods.extend(WUXING_FOODS[wx][:3])
        
        # 五行补救建议
        bujiu = cls._generate_bujiu(wuxing_count, xi_yong)
        
        # 注意事项
        warnings = cls._generate_warnings(xing_chong_result, wuxing_count, xi_yong)
        
        return {
            '喜用五行': xi_yong,
            '忌神五行': ji_shen,
            '吉利方位': list(set(lucky_directions))[:4],
            '吉利颜色': list(set(lucky_colors))[:5],
            '吉利行业': list(set(lucky_industries))[:6],
            '吉利数字': list(set(lucky_numbers))[:6],
            '吉祥物': list(set(lucky_items))[:4],
            '吉利食物': list(set(lucky_foods))[:5],
            '五行补救': bujiu,
            '注意事项': warnings,
        }

    @classmethod
    def _generate_bujiu(cls, wuxing_count: Dict, xi_yong: List[str]) -> List[str]:
        """生成五行补救建议"""
        bujiu = []
        
        missing = [wx for wx, count in wuxing_count.items() if count == 0]
        weak = [wx for wx, count in wuxing_count.items() if count == 1]
        
        for wx in missing:
            advice = cls._get_wuxing_bujiu(wx)
            bujiu.append(f'【缺{wx}】{advice}')
        
        for wx in weak:
            advice = cls._get_wuxing_bujiu(wx)
            bujiu.append(f'【{wx}弱】{advice}')
        
        return bujiu

    @classmethod
    def _get_wuxing_bujiu(cls, wuxing: str) -> str:
        """获取五行补救建议"""
        bujiu_advice = {
            '木': '多接触绿色植物，常去公园散步，佩戴木质饰品，宜穿绿色衣物',
            '火': '多晒太阳，保持乐观，常穿红色衣物，可佩戴红玛瑙',
            '土': '亲近大地，多去户外，佩戴黄水晶，多食黄色食物',
            '金': '佩戴金属饰品，多穿白色衣物，保持居室整洁明亮',
            '水': '近水而居，多游泳，佩戴黑曜石，多喝水，常穿黑色衣物',
        }
        return bujiu_advice.get(wuxing, '')

    @classmethod
    def _generate_warnings(cls, xing_chong_result: Optional[Dict],
                           wuxing_count: Dict, xi_yong: List[str]) -> List[str]:
        """生成注意事项"""
        warnings = []
        
        if xing_chong_result:
            # 日支逢冲
            for chong in xing_chong_result.get('六冲', []):
                if '日' in chong.get('位置', ''):
                    warnings.append('婚姻宫逢冲，感情需多用心经营')
                    break
            
            # 三刑
            if xing_chong_result.get('三刑'):
                warnings.append('命带刑伤，行事需谨慎，防口舌是非')
        
        # 五行过旺提醒
        for wx, count in wuxing_count.items():
            if count >= 3 and wx not in xi_yong:
                warnings.append(f'{wx}气过旺，宜适当泄耗')
        
        if not warnings:
            warnings.append('命局和谐，顺势而为，积善行德')
        
        return warnings

    @classmethod
    def format_output(cls, advice: Dict) -> str:
        """格式化输出建议"""
        lines = []
        lines.append('【趋吉避凶建议】')
        lines.append('')
        
        lines.append(f'  喜用五行：{", ".join(advice["喜用五行"])}')
        lines.append(f'  忌神五行：{", ".join(advice["忌神五行"])}')
        lines.append('')
        
        if advice['吉利方位']:
            lines.append(f'  🧭 吉利方位：{", ".join(advice["吉利方位"])}')
        
        if advice['吉利颜色']:
            lines.append(f'  🎨 吉利颜色：{", ".join(advice["吉利颜色"])}')
        
        if advice['吉利行业']:
            lines.append(f'  💼 吉利行业：{", ".join(advice["吉利行业"])}')
        
        if advice['吉利数字']:
            lines.append(f'  🔢 吉利数字：{", ".join(advice["吉利数字"])}')
        
        if advice['吉祥物']:
            lines.append(f'  🎁 吉祥物：{", ".join(advice["吉祥物"])}')
        
        if advice['吉利食物']:
            lines.append(f'  🍵 吉利食物：{", ".join(advice["吉利食物"])}')
        
        if advice['五行补救']:
            lines.append('')
            lines.append('  【五行补救】')
            for b in advice['五行补救']:
                lines.append(f'    {b}')
        
        if advice['注意事项']:
            lines.append('')
            lines.append('  【注意事项】')
            for w in advice['注意事项']:
                lines.append(f'    • {w}')
        
        return '\n'.join(lines)


if __name__ == '__main__':
    import json
    
    # 测试
    test_si_zhu = {
        '年柱': ('庚', '午'),
        '月柱': ('壬', '午'),
        '日柱': ('庚', '戌'),
        '时柱': ('庚', '辰'),
    }
    
    test_wuxing = {'木': 0, '火': 2, '土': 2, '金': 3, '水': 1}
    test_yong_shen = {'喜用': ['水', '木'], '忌神': ['火', '土'], '日主五行': '金', '旺衰': '旺'}
    
    # 评分
    score = ComprehensiveScorer.calculate_score(test_si_zhu, test_wuxing, '食神格', test_yong_shen)
    print("【综合评分】")
    print(f"总分: {score['总分']}/100")
    print(f"等级: {score['等级']} — {score['等级说明']}")
    for k, v in score['分项评分'].items():
        print(f"  {k}: {v}")
    
    print()
    
    # 建议
    advice = TrendAdvisor.generate_advice(test_yong_shen, test_wuxing, test_si_zhu, '庚')
    print(TrendAdvisor.format_output(advice))
