#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风水堪舆工具 v3.3.0
天工长老开发

功能：
- 八宅风水排盘（东四宅/西四宅）
- 命卦计算
- 游年九星排布
- 方位吉凶分析
- 流年飞星排布（v3.3.0 新增）
- 煞气识别增强（v3.3.0 新增）
- 布局建议
"""

import argparse
import json
from typing import Dict, List, Optional

# ============== 基础数据 ==============

# 八卦
BA_GUA = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']

# 八宅游年九星
JIU_XING = {
    '生气': {'五行': '木', '吉凶': '大吉', '含义': '事业兴旺，贵人相助'},
    '天医': {'五行': '土', '吉凶': '大吉', '含义': '健康长寿，疾病可愈'},
    '延年': {'五行': '金', '吉凶': '大吉', '含义': '婚姻和睦，家庭幸福'},
    '伏位': {'五行': '木', '吉凶': '吉', '含义': '平稳安定，宜守不宜动'},
    '绝命': {'五行': '金', '吉凶': '大凶', '含义': '破财伤身，需化解'},
    '五鬼': {'五行': '火', '吉凶': '凶', '含义': '口舌是非，小人暗害'},
    '六煞': {'五行': '水', '吉凶': '凶', '含义': '桃花纠纷，感情不顺'},
    '祸害': {'五行': '土', '吉凶': '凶', '含义': '意外灾祸，健康受损'}
}

# 九星方位（洛书九宫）
JIU_GONG = {
    1: {'卦': '坎', '方位': '正北', '五行': '水'},
    2: {'卦': '坤', '方位': '西南', '五行': '土'},
    3: {'卦': '震', '方位': '正东', '五行': '木'},
    4: {'卦': '巽', '方位': '东南', '五行': '木'},
    5: {'卦': '中', '方位': '中央', '五行': '土'},
    6: {'卦': '乾', '方位': '西北', '五行': '金'},
    7: {'卦': '兑', '方位': '正西', '五行': '金'},
    8: {'卦': '艮', '方位': '东北', '五行': '土'},
    9: {'卦': '离', '方位': '正南', '五行': '火'}
}

# 东四命/西四命
DONG_SI_MING = ['坎', '离', '震', '巽']  # 东四命
XI_SI_MING = ['乾', '坤', '艮', '兑']     # 西四命

# 东四宅/西四宅
DONG_SI_ZHAI = ['坎宅', '离宅', '震宅', '巽宅']
XI_SI_ZHAI = ['乾宅', '坤宅', '艮宅', '兑宅']

# 游年歌诀（八宅翻卦）
YOU_NIAN = {
    '乾': {'生气': '兑', '天医': '艮', '延年': '坤', '伏位': '乾', '绝命': '离', '五鬼': '震', '六煞': '坎', '祸害': '巽'},
    '坤': {'生气': '艮', '天医': '兑', '延年': '乾', '伏位': '坤', '绝命': '坎', '五鬼': '巽', '六煞': '离', '祸害': '震'},
    '震': {'生气': '离', '天医': '坎', '延年': '巽', '伏位': '震', '绝命': '兑', '五鬼': '艮', '六煞': '艮', '祸害': '坤'},
    '巽': {'生气': '坎', '天医': '离', '延年': '震', '伏位': '巽', '绝命': '兑', '五鬼': '坤', '六煞': '艮', '祸害': '坎'},
    '坎': {'生气': '巽', '天医': '震', '延年': '离', '伏位': '坎', '绝命': '坤', '五鬼': '艮', '六煞': '乾', '祸害': '兑'},
    '离': {'生气': '震', '天医': '巽', '延年': '坎', '伏位': '离', '绝命': '乾', '五鬼': '兑', '六煞': '坤', '祸害': '艮'},
    '艮': {'生气': '坤', '天医': '乾', '延年': '兑', '伏位': '艮', '绝命': '巽', '五鬼': '坎', '六煞': '震', '祸害': '离'},
    '兑': {'生气': '乾', '天医': '坤', '延年': '艮', '伏位': '兑', '绝命': '震', '五鬼': '离', '六煞': '巽', '祸害': '坎'}
}

# 流年飞星（2024-2043）
LIU_NIAN_FEI_XING = {
    2024: 3, 2025: 2, 2026: 1, 2027: 9, 2028: 8,
    2029: 7, 2030: 6, 2031: 5, 2032: 4, 2033: 3,
    2034: 2, 2035: 1, 2036: 9, 2037: 8, 2038: 7,
    2039: 6, 2040: 5, 2041: 4, 2042: 3, 2043: 2
}

# 流年飞星含义
FEI_XING_MEANING = {
    1: {'name': '一白贪狼星', '五行': '水', '吉凶': '吉', '含义': '事业、桃花、人缘'},
    2: {'name': '二黑巨门星', '五行': '土', '吉凶': '凶', '含义': '疾病、伤痛'},
    3: {'name': '三碧禄存星', '五行': '木', '吉凶': '凶', '含义': '是非、官非、争斗'},
    4: {'name': '四绿文曲星', '五行': '木', '吉凶': '吉', '含义': '学业、文昌、考试'},
    5: {'name': '五黄廉贞星', '五行': '土', '吉凶': '大凶', '含义': '灾祸、意外、大病'},
    6: {'name': '六白武曲星', '五行': '金', '吉凶': '吉', '含义': '偏财、贵人、权势'},
    7: {'name': '七赤破军星', '五行': '金', '吉凶': '凶', '含义': '破财、口舌、盗贼'},
    8: {'name': '八白左辅星', '五行': '土', '吉凶': '大吉', '含义': '正财、置业、升职'},
    9: {'name': '九紫右弼星', '五行': '火', '吉凶': '大吉', '含义': '喜庆、姻缘、添丁'}
}

# 化解方法
HUA_JIE = {
    '二黑': '铜葫芦、六帝钱、白色/金色物品',
    '三碧': '红色物品、灯光',
    '五黄': '铜铃、六帝钱、金属物品，忌动土',
    '七赤': '安忍水、黑色/蓝色物品'
}

# ============== 命卦计算 ==============

def get_ming_gua(year: int, gender: str = '男') -> str:
    """
    根据出生年份和性别计算命卦
    男命：(100 - 出生年后两位) ÷ 9 取余
    女命：(出生年后两位 - 4) ÷ 9 取余
    """
    year_last2 = year % 100

    if gender == '男':
        remainder = (100 - year_last2) % 9
    else:
        remainder = (year_last2 - 4) % 9

    if remainder == 0:
        remainder = 9

    gua_map = {1: '坎', 2: '坤', 3: '震', 4: '巽', 6: '乾', 7: '兑', 8: '艮', 9: '离'}
    return gua_map.get(remainder, '坤')


# ============== 八宅分类 ==============

def get_zhai_type(direction: str) -> str:
    """根据坐向判断宅型"""
    zhai_map = {
        '坐北朝南': '坎宅', '坐南朝北': '离宅',
        '坐东朝西': '震宅', '坐西朝东': '兑宅',
        '坐东南朝西北': '巽宅', '坐西北朝东南': '乾宅',
        '坐东北朝西南': '艮宅', '坐西南朝东北': '坤宅'
    }
    return zhai_map.get(direction, '')


def get_dong_xi(zhai: str) -> str:
    """判断东四宅/西四宅"""
    if zhai in DONG_SI_ZHAI:
        return '东四宅'
    elif zhai in XI_SI_ZHAI:
        return '西四宅'
    return '未知'


# ============== 游年九星排布 ==============

def get_you_nian(zhai: str) -> Dict[str, str]:
    """获取游年九星方位"""
    return YOU_NIAN.get(zhai, {})


def get_fang_wei_ji_xiong(zhai: str) -> Dict[str, Dict]:
    """获取各方位吉凶"""
    you_nian = get_you_nian(zhai)
    result = {}

    for xing_name, fang_wei in you_nian.items():
        if xing_name in JIU_XING:
            result[fang_wei] = {
                '九星': xing_name,
                '吉凶': JIU_XING[xing_name]['吉凶'],
                '含义': JIU_XING[xing_name]['含义'],
                '五行': JIU_XING[xing_name]['五行']
            }

    return result


# ============== 流年飞星 ==============

def get_liu_nian_fei_xing(year: int) -> Dict:
    """
    计算流年九宫飞星
    规则：中宫飞星按年递减，逢5入中后递减
    """
    if year < 2024 or year > 2043:
        # 通用算法
        zhong_gong = (11 - (year - 2000) % 9) % 9
        if zhong_gong == 0:
            zhong_gong = 9
    else:
        zhong_gong = LIU_NIAN_FEI_XING.get(year, 1)

    # 洛书轨迹飞布
    fei_xing_path = [5, 6, 7, 8, 9, 1, 2, 3, 4]  # 洛书顺序

    # 找到中宫飞星在路径中的位置
    start_idx = fei_xing_path.index(zhong_gong)

    # 九宫位置顺序（洛书轨迹）
    palace_order = [5, 6, 7, 8, 9, 1, 2, 3, 4]  # 中→乾→兑→艮→离→坎→坤→震→巽

    result = {}
    for i, palace in enumerate(palace_order):
        star_idx = (start_idx + i) % 9
        star = fei_xing_path[star_idx]
        result[palace] = {
            '飞星': star,
            '名称': FEI_XING_MEANING[star]['name'],
            '五行': FEI_XING_MEANING[star]['五行'],
            '吉凶': FEI_XING_MEANING[star]['吉凶'],
            '含义': FEI_XING_MEANING[star]['含义'],
            '方位': JIU_GONG[palace]['方位'],
            '卦': JIU_GONG[palace]['卦']
        }

    return result


def get_liu_nian_fang_wei(year: int) -> Dict:
    """获取流年吉凶方位"""
    fei_xing = get_liu_nian_fei_xing(year)

    ji_fang = []
    xiong_fang = []
    wu_huang_fang = ''
    er_hei_fang = ''

    for palace, info in fei_xing.items():
        if info['吉凶'] in ['大吉', '吉']:
            ji_fang.append(f"{info['方位']}（{info['名称']}）")
        elif info['吉凶'] in ['大凶', '凶']:
            xiong_fang.append(f"{info['方位']}（{info['名称']}）")

        if info['飞星'] == 5:
            wu_huang_fang = info['方位']
        elif info['飞星'] == 2:
            er_hei_fang = info['方位']

    return {
        '吉方': ji_fang,
        '凶方': xiong_fang,
        '五黄方': wu_huang_fang,
        '二黑方': er_hei_fang
    }


# ============== 煞气识别 ==============

def get_sha_qi(direction: str, year: int) -> Dict:
    """煞气识别"""
    result = {'形煞': [], '理煞': [], '化解': []}

    # 流年三煞
    san_sha_map = {
        '申子辰': '南方', '寅午戌': '北方',
        '亥卯未': '西方', '巳酉丑': '东方'
    }

    year_zhi_idx = (year - 4) % 12
    year_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][year_zhi_idx]

    if year_zhi in ['申', '子', '辰']:
        san_sha = '南方'
    elif year_zhi in ['寅', '午', '戌']:
        san_sha = '北方'
    elif year_zhi in ['亥', '卯', '未']:
        san_sha = '西方'
    else:
        san_sha = '东方'

    result['理煞'].append(f'今年三煞方：{san_sha}')

    # 岁破方
    sui_po_idx = (year_zhi_idx + 6) % 12
    sui_po = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'][sui_po_idx]
    result['理煞'].append(f'今年岁破方：{sui_po}')

    # 流年飞星煞气
    fei_xing = get_liu_nian_fei_xing(year)
    for palace, info in fei_xing.items():
        if info['飞星'] == 5:
            result['理煞'].append(f'五黄煞在{info["方位"]}，宜静不宜动')
            result['化解'].append(f'{info["方位"]}：挂铜铃或六帝钱化解五黄')
        elif info['飞星'] == 2:
            result['理煞'].append(f'二黑病符在{info["方位"]}，注意健康')
            result['化解'].append(f'{info["方位"]}：放铜葫芦化解二黑')

    # 形煞检查（需要用户提供）
    result['形煞说明'] = '形煞需实地勘察：路冲、反弓、天斩、壁刀等'
    result['形煞类型'] = {
        '路冲煞': '道路直冲大门或窗户',
        '反弓煞': '道路反弓对宅',
        '天斩煞': '两高楼之间狭窄缝隙',
        '壁刀煞': '邻屋墙角对宅',
        '穿心煞': '大门正对后门或阳台'
    }

    return result


# ============== 布局建议 ==============

def get_bu_ju(zhai: str, ming_gua: str, year: int) -> Dict:
    """布局建议"""
    fang_wei = get_fang_wei_ji_xiong(zhai)
    liu_nian = get_liu_nian_fang_wei(year)

    bu_ju = {
        '大门': '宜开在生气/天医/延年方',
        '主卧': '宜在生气/延年方，利健康婚姻',
        '书房': '宜在文昌位（四绿方），利学业',
        '厨房': '宜在祸害/五鬼方（压凶），灶口向吉方',
        '客厅': '宜在生气/延年方，利家运',
        '卫生间': '宜在绝命/五鬼方（压凶），忌在吉方'
    }

    # 结合流年
    ji_fang = liu_nian['吉方']
    xiong_fang = liu_nian['凶方']

    return {
        '房间布局': bu_ju,
        '今年吉方': ji_fang,
        '今年凶方': xiong_fang,
        '注意事项': [
            f'五黄方（{liu_nian["五黄方"]}）不宜动土、装修',
            f'二黑方（{liu_nian["二黑方"]}）注意家人健康',
            f'三煞方不宜动土、钻墙'
        ]
    }


# ============== 综合排盘 ==============

def fengshui_pan(year: int, direction: str = None, gender: str = '男') -> Dict:
    """风水综合排盘"""
    result = {}

    # 命卦
    result['命卦'] = get_ming_gua(year, gender)
    result['东西命'] = '东四命' if result['命卦'] in DONG_SI_MING else '西四命'

    # 宅型
    if direction:
        result['坐向'] = direction
        result['宅型'] = get_zhai_type(direction)
        result['东西宅'] = get_dong_xi(result['宅型'])
        result['宅命相配'] = '相配' if (
            (result['东西命'] == '东四命' and result['东西宅'] == '东四宅') or
            (result['东西命'] == '西四命' and result['东西宅'] == '西四宅')
        ) else '不配'

    # 游年九星
    zhai = result.get('宅型', result['命卦'])
    # 去掉"宅"后缀，如"坎宅"→"坎"
    zhai_base = zhai.replace('宅', '')
    result['游年九星'] = get_fang_wei_ji_xiong(zhai_base)

    # 流年飞星
    current_year = 2026  # 默认当前年
    result['流年飞星'] = get_liu_nian_fei_xing(current_year)
    result['流年方位'] = get_liu_nian_fang_wei(current_year)

    # 煞气
    result['煞气'] = get_sha_qi(zhai, current_year)

    # 布局建议
    result['布局建议'] = get_bu_ju(zhai, result['命卦'], current_year)

    return result


# ============== 输出格式化 ==============

def format_output(result: Dict) -> str:
    """格式化输出"""
    lines = []

    lines.append('【风水堪舆排盘】v3.3.0')
    lines.append(f'• 命卦：{result["命卦"]}（{result["东西命"]}）')

    if result.get('宅型'):
        lines.append(f'• 坐向：{result["坐向"]}')
        lines.append(f'• 宅型：{result["宅型"]}（{result["东西宅"]}）')
        lines.append(f'• 宅命：{result["宅命相配"]}')

    lines.append('')
    lines.append('【游年九星】')
    gua_to_fang = {'坎': '正北', '坤': '西南', '震': '正东', '巽': '东南', '离': '正南', '乾': '西北', '艮': '东北', '兑': '正西'}
    for gua, info in result.get('游年九星', {}).items():
        fang = gua_to_fang.get(gua, gua)
        icon = '🟢' if '大吉' in info['吉凶'] else '🔵' if '吉' in info['吉凶'] else '🔴' if '凶' in info['吉凶'] else '⚪'
        lines.append(f'  {icon} {fang}（{gua}宫）：{info["九星"]}（{info["吉凶"]}）— {info["含义"]}')

    lines.append('')
    lines.append(f'【流年飞星 2026】')
    for palace, info in result.get('流年飞星', {}).items():
        icon = '🟢' if '大吉' in info['吉凶'] else '🔵' if '吉' in info['吉凶'] else '🔴' if '凶' in info['吉凶'] else '⚪'
        lines.append(f'  {icon} {info["方位"]}（{info["卦"]}宫）：{info["名称"]}（{info["吉凶"]}）— {info["含义"]}')

    lines.append('')
    lines.append('【流年方位】')
    lines.append(f'  吉方：{", ".join(result.get("流年方位", {}).get("吉方", []))}')
    lines.append(f'  凶方：{", ".join(result.get("流年方位", {}).get("凶方", []))}')
    lines.append(f'  五黄方：{result.get("流年方位", {}).get("五黄方", "无")}')
    lines.append(f'  二黑方：{result.get("流年方位", {}).get("二黑方", "无")}')

    lines.append('')
    lines.append('【煞气识别】')
    for sha in result.get('煞气', {}).get('理煞', []):
        lines.append(f'  ⚠️ {sha}')
    for hua in result.get('煞气', {}).get('化解', []):
        lines.append(f'  💊 {hua}')

    lines.append('')
    lines.append('【布局建议】')
    for room, advice in result.get('布局建议', {}).get('房间布局', {}).items():
        lines.append(f'  {room}：{advice}')

    return '\n'.join(lines)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description='风水堪舆工具 v3.3.0')
    parser.add_argument('--year', '-y', type=int, default=1990, help='出生年份')
    parser.add_argument('--direction', '-d', type=str, help='房屋坐向（如"坐北朝南"）')
    parser.add_argument('--gender', '-g', type=str, default='男', choices=['男', '女'], help='性别')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')

    args = parser.parse_args()

    result = fengshui_pan(args.year, args.direction, args.gender)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
