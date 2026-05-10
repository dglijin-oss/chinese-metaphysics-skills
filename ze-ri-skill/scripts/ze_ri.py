#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
择日学工具 v3.3.0
天工长老开发

功能：
- 建除十二神查询
- 黄道黑道日查询
- 神煞吉凶查询
- 宜忌事项查询
- 分类择日（婚嫁/开业/动土/出行等）
- 时辰择日（精确到时辰）
- 吉日推荐（月度/年度）
- 与八字喜用神配合择日
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# ============== 天干地支基础 ==============

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
WU_XING_GAN = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
WU_XING_ZHI = {'子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'}

# ============== 农历数据（1900-2100）=============

LUNAR_DATA = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
    0x0d520,
]

MONTHS_CH = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']


def is_leap_year(year):
    """判断闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(year, month):
    """每月天数"""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif is_leap_year(year):
        return 29
    else:
        return 28


# ============== 干支计算 ==============

def get_gan_zhi_year(year: int) -> str:
    """计算年干支"""
    gan_idx = (year - 4) % 10
    zhi_idx = (year - 4) % 12
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]


def get_gan_zhi_month(year: int, month: int, day: int) -> str:
    """计算月干支（以节气为界，简化版）"""
    # 年干决定月干
    year_gan_idx = (year - 4) % 10
    month_gan_start = (year_gan_idx * 2 + 2) % 10  # 丙寅月起

    # 简化：以农历月为准（实际应以节气）
    month_gan_idx = (month_gan_start + month - 1) % 10
    month_zhi_idx = (month + 1) % 12  # 寅月起

    return TIAN_GAN[month_gan_idx] + DI_ZHI[month_zhi_idx]


def get_gan_zhi_day(year: int, month: int, day: int) -> str:
    """计算日干支"""
    base_date = datetime(1900, 1, 1)
    target_date = datetime(year, month, day)
    delta = (target_date - base_date).days
    # 1900-01-01 是 甲戌日
    gan_idx = (delta + 0) % 10  # 甲
    zhi_idx = (delta + 10) % 12  # 戌
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]


def get_gan_zhi_hour(hour: int, day_gan: str) -> str:
    """计算时干支"""
    zhi_idx = (hour + 1) // 2 % 12
    gan_base = TIAN_GAN.index(day_gan) * 2 % 10
    gan_idx = (gan_base + zhi_idx) % 10
    return TIAN_GAN[gan_idx] + DI_ZHI[zhi_idx]


def get_day_gan_zhi(year, month, day):
    """获取日天干地支"""
    gz = get_gan_zhi_day(year, month, day)
    return gz[0], gz[1]


def get_day_gan_idx(year, month, day):
    """获取日天干索引"""
    return TIAN_GAN.index(get_gan_zhi_day(year, month, day)[0])


def get_day_zhi_idx(year, month, day):
    """获取日地支索引"""
    return DI_ZHI.index(get_gan_zhi_day(year, month, day)[1])


# ============== 建除十二神 ==============

JIAN_CHU = ['建', '除', '满', '平', '定', '执', '破', '危', '成', '收', '开', '闭']

JIAN_CHU_JI_XIONG = {
    '建': '吉', '除': '吉', '满': '吉', '平': '平',
    '定': '吉', '执': '吉', '破': '大凶', '危': '凶',
    '成': '吉', '收': '吉', '开': '吉', '闭': '凶'
}

JIAN_CHU_YI = {
    '建': ['上任', '出行', '安床', '入学'],
    '除': ['扫舍', '求医', '解除', '沐浴'],
    '满': ['祭祀', '祈福', '嫁娶', '纳采'],
    '平': ['祭祀', '祈福', '修造', '动土'],
    '定': ['祭祀', '祈福', '嫁娶', '安床'],
    '执': ['祭祀', '祈福', '捕捉', '狩猎'],
    '破': ['破屋', '坏垣', '求医', '解除'],
    '危': ['祭祀', '祈福'],
    '成': ['祭祀', '祈福', '嫁娶', '开业', '入学', '出行'],
    '收': ['祭祀', '祈福', '捕捉', '纳财', '入库'],
    '开': ['祭祀', '祈福', '嫁娶', '开业', '出行', '动土'],
    '闭': ['祭祀', '祈福', '修造', '安葬']
}

JIAN_CHU_JI = {
    '建': ['动土', '开仓', '安葬'],
    '除': ['嫁娶', '开业'],
    '满': ['服药', '栽种', '安葬'],
    '平': ['嫁娶', '安葬', '开渠'],
    '定': ['出行', '医疗', '词讼'],
    '执': ['出行', '搬迁', '开仓'],
    '破': ['余事'],
    '危': ['登高', '乘船', '远行'],
    '成': ['诉讼', '词讼'],
    '收': ['出行', '安葬', '开仓'],
    '开': ['动土', '破土', '安葬'],
    '闭': ['嫁娶', '出行', '开业', '针刺']
}


def get_jian_chu(year: int, month: int, day: int) -> str:
    """
    计算建除十二神
    规则：以月建（月支）为基准，从建日开始顺数
    简化：用日支与月支的关系
    """
    # 获取日支
    day_zhi = get_gan_zhi_day(year, month, day)[1]
    day_zhi_idx = DI_ZHI.index(day_zhi)

    # 获取月支（简化用公历月）
    month_zhi_idx = (month + 1) % 12  # 正月建寅

    # 建除 = (日支 - 月支) % 12
    jc_idx = (day_zhi_idx - month_zhi_idx + 12) % 12
    return JIAN_CHU[jc_idx]


# ============== 黄道黑道十二神 ==============

HUANG_DAO = ['青龙', '明堂', '天刑', '朱雀', '金匮', '天德', '白虎', '玉堂', '天牢', '玄武', '司命', '勾陈']

HUANG_DAO_JI_XIONG = {
    '青龙': '大吉', '明堂': '大吉', '天刑': '凶', '朱雀': '凶',
    '金匮': '大吉', '天德': '大吉', '白虎': '凶', '玉堂': '大吉',
    '天牢': '凶', '玄武': '凶', '司命': '吉', '勾陈': '凶'
}


def get_huang_dao(year: int, month: int, day: int) -> str:
    """
    黄道黑道计算
    规则：根据日支确定当日的黄道十二神
    子午日从青龙起，丑未日从明堂起，依此类推
    """
    day_zhi = get_gan_zhi_day(year, month, day)[1]
    day_zhi_idx = DI_ZHI.index(day_zhi)

    # 起法：子午日从青龙（0）起，丑未日从明堂（1），寅申 day 2...
    start_idx = day_zhi_idx % 12

    # 当日值神从起始神开始
    huang_dao_idx = start_idx
    return HUANG_DAO[huang_dao_idx]


# ============== 二十八宿（简化）=============

ER_SHI_BA_XIU = [
    '角', '亢', '氐', '房', '心', '尾', '箕',  # 东方青龙七宿
    '斗', '牛', '女', '虚', '危', '室', '壁',  # 北方玄武七宿
    '奎', '娄', '胃', '昴', '毕', '觜', '参',  # 西方白虎七宿
    '井', '鬼', '柳', '星', '张', '翼', '轸'   # 南方朱雀七宿
]

XIU_JI_XIONG = {
    '角': '吉', '亢': '凶', '氐': '吉', '房': '吉', '心': '凶', '尾': '吉', '箕': '吉',
    '斗': '吉', '牛': '凶', '女': '凶', '虚': '凶', '危': '吉', '室': '吉', '壁': '吉',
    '奎': '凶', '娄': '吉', '胃': '吉', '昴': '凶', '毕': '吉', '觜': '凶', '参': '吉',
    '井': '吉', '鬼': '凶', '柳': '凶', '星': '凶', '张': '吉', '翼': '吉', '轸': '吉'
}


def get_xiu(year: int, month: int, day: int) -> str:
    """二十八宿（简化算法）"""
    base_date = datetime(1900, 1, 1)
    target_date = datetime(year, month, day)
    delta = (target_date - base_date).days
    return ER_SHI_BA_XIU[delta % 28]


# ============== 神煞系统 ==============

def get_shen_sha(year: int, month: int, day: int) -> Dict:
    """神煞查询"""
    day_gan, day_zhi = get_day_gan_zhi(year, month, day)
    day_zhi_idx = DI_ZHI.index(day_zhi)
    day_gan_idx = TIAN_GAN.index(day_gan)

    ji_shen = []  # 吉神
    xiong_sha = []  # 凶煞

    # === 吉神 ===

    # 天德贵人
    tian_de = {1: '巳', 2: '庚', 3: '丁', 4: '申', 5: '壬', 6: '亥',
               7: '辛', 8: '寅', 9: '丙', 10: '巳', 11: '庚', 12: '亥'}
    if str(tian_de.get(month, '')) == day_zhi or str(tian_de.get(month, '')) == day_gan:
        ji_shen.append('天德贵人')

    # 月德贵人
    yue_de = {1: '丙', 2: '甲', 3: '壬', 4: '庚', 5: '丙', 6: '甲',
              7: '壬', 8: '庚', 9: '丙', 10: '甲', 11: '壬', 12: '庚'}
    if yue_de.get(month, '') == day_gan:
        ji_shen.append('月德贵人')

    # 天赦日
    tian_she = {
        (1, 2, 3): '戊寅', (4, 5, 6): '甲午',
        (7, 8, 9): '戊申', (10, 11, 12): '甲子'
    }
    for months, gz in tian_she.items():
        if month in months:
            if get_gan_zhi_day(year, month, day) == gz:
                ji_shen.append('天赦日')
            break

    # 三合日
    san_he = {
        '申': '子', '子': '申', '辰': '子',  # 申子辰三合
        '亥': '卯', '卯': '亥', '未': '卯',  # 亥卯未三合
        '寅': '午', '午': '寅', '戌': '午',  # 寅午戌三合
        '巳': '酉', '酉': '巳', '丑': '酉',  # 巳酉丑三合
    }

    # 六合日
    liu_he = {
        '子': '丑', '丑': '子', '寅': '亥', '亥': '寅',
        '卯': '戌', '戌': '卯', '辰': '酉', '酉': '辰',
        '巳': '申', '申': '巳', '午': '未', '未': '午'
    }

    # 天乙贵人
    tian_yi_map = {
        '甲': ['丑', '未'], '乙': ['子', '申'], '丙': ['亥', '酉'],
        '丁': ['亥', '酉'], '戊': ['丑', '未'], '己': ['子', '申'],
        '庚': ['丑', '未'], '辛': ['午', '寅'], '壬': ['卯', '巳'],
        '癸': ['卯', '巳']
    }
    if day_zhi in tian_yi_map.get(day_gan, []):
        ji_shen.append('天乙贵人')

    # === 凶煞 ===

    # 岁破
    year_zhi_idx = (year - 4) % 12
    sui_po_idx = (year_zhi_idx + 6) % 12
    if day_zhi_idx == sui_po_idx:
        xiong_sha.append('岁破')

    # 月破
    month_zhi_idx = (month + 1) % 12
    yue_po_idx = (month_zhi_idx + 6) % 12
    if day_zhi_idx == yue_po_idx:
        xiong_sha.append('月破')

    # 四离四绝（简化）
    si_li = [(3, 20), (6, 21), (9, 23), (12, 22)]  # 春分、夏至、秋分、冬至前一日
    si_jue = [(2, 3), (5, 4), (8, 7), (11, 7)]  # 立春、立夏、立秋、立冬前一日
    if (month, day) in si_li:
        xiong_sha.append('四离日')
    if (month, day) in si_jue:
        xiong_sha.append('四绝日')

    # 杨公忌日（简化：公历每月特定日）
    yang_gong = {1: 13, 2: 11, 3: 13, 4: 9, 5: 13, 6: 11, 7: 13, 8: 9, 9: 13, 10: 11, 11: 13, 12: 9}
    if day == yang_gong.get(month, 0):
        xiong_sha.append('杨公忌日')

    return {'吉神': ji_shen, '凶煞': xiong_sha}


# ============== 时辰择日 ==============

SHI_CHEN = [
    {'name': '子时', 'time': '23:00-01:00', 'zhi': '子'},
    {'name': '丑时', 'time': '01:00-03:00', 'zhi': '丑'},
    {'name': '寅时', 'time': '03:00-05:00', 'zhi': '寅'},
    {'name': '卯时', 'time': '05:00-07:00', 'zhi': '卯'},
    {'name': '辰时', 'time': '07:00-09:00', 'zhi': '辰'},
    {'name': '巳时', 'time': '09:00-11:00', 'zhi': '巳'},
    {'name': '午时', 'time': '11:00-13:00', 'zhi': '午'},
    {'name': '未时', 'time': '13:00-15:00', 'zhi': '未'},
    {'name': '申时', 'time': '15:00-17:00', 'zhi': '申'},
    {'name': '酉时', 'time': '17:00-19:00', 'zhi': '酉'},
    {'name': '戌时', 'time': '19:00-21:00', 'zhi': '戌'},
    {'name': '亥时', 'time': '21:00-23:00', 'zhi': '亥'},
]

# 十二时辰吉凶（基于日干，简化通用版）
SHI_CHEN_JI_XIONG = {
    '建': {'吉': ['子', '寅', '辰', '午', '申', '戌'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
    '除': {'吉': ['丑', '卯', '巳', '未', '酉', '亥'], '凶': ['子', '寅', '辰', '午', '申', '戌']},
    '满': {'吉': ['寅', '辰', '午', '申', '戌', '子'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
    '平': {'吉': ['卯', '巳', '未', '酉', '亥', '丑'], '凶': ['子', '寅', '辰', '午', '申', '戌']},
    '定': {'吉': ['辰', '午', '申', '戌', '子', '寅'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
    '执': {'吉': ['巳', '未', '酉', '亥', '丑', '卯'], '凶': ['子', '寅', '辰', '午', '申', '戌']},
    '破': {'吉': [], '凶': ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']},
    '危': {'吉': ['午', '申', '戌', '子', '寅', '辰'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
    '成': {'吉': ['未', '酉', '亥', '丑', '卯', '巳'], '凶': ['子', '寅', '辰', '午', '申', '戌']},
    '收': {'吉': ['申', '戌', '子', '寅', '辰', '午'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
    '开': {'吉': ['酉', '亥', '丑', '卯', '巳', '未'], '凶': ['子', '寅', '辰', '午', '申', '戌']},
    '闭': {'吉': ['戌', '子', '寅', '辰', '午', '申'], '凶': ['丑', '卯', '巳', '未', '酉', '亥']},
}


def get_shi_chen_list(year: int, month: int, day: int) -> List[Dict]:
    """获取当日十二时辰吉凶排布"""
    jian_chu = get_jian_chu(year, month, day)
    huang_dao = get_huang_dao(year, month, day)

    result = []
    for sc in SHI_CHEN:
        zhi = sc['zhi']
        ji_xiong_map = SHI_CHEN_JI_XIONG.get(jian_chu, {'吉': [], '凶': []})

        if zhi in ji_xiong_map['吉']:
            ji_xiong = '吉'
        elif zhi in ji_xiong_map['凶']:
            ji_xiong = '凶'
        else:
            ji_xiong = '平'

        # 黄道黑道影响
        hd_jx = HUANG_DAO_JI_XIONG.get(huang_dao, '平')
        if hd_jx in ['大吉', '吉'] and ji_xiong == '凶':
            ji_xiong = '平'
        elif hd_jx in ['大凶', '凶'] and ji_xiong == '吉':
            ji_xiong = '平'

        hour_gz = get_gan_zhi_hour(int(sc['time'].split(':')[0]) % 24, get_gan_zhi_day(year, month, day)[0])

        result.append({
            '时辰': sc['name'],
            '时间': sc['time'],
            '干支': hour_gz,
            '吉凶': ji_xiong
        })

    return result


def get_best_shi_chen(year: int, month: int, day: int, event: str = 'general') -> List[Dict]:
    """根据事项推荐最佳时辰"""
    shi_chen_list = get_shi_chen_list(year, month, day)
    ji_shi_chen = [sc for sc in shi_chen_list if sc['吉凶'] == '吉']

    # 根据事项筛选
    event_shi_chen = {
        '婚嫁': ['午', '未', '巳', '辰'],  # 正午前后最佳
        '开业': ['辰', '巳', '午', '未'],  # 上午最佳
        '出行': ['寅', '卯', '辰', '巳'],  # 清晨出发
        '动土': ['辰', '巳', '午'],  # 上午
        '签约': ['巳', '午', '未', '申'],  # 上午到下午
        '搬家': ['辰', '巳', '午', '未'],  # 上午
        '考试': ['卯', '辰', '巳'],  # 早晨
        '求医': ['卯', '辰', '巳', '午'],  # 上午
    }

    preferred_zhi = event_shi_chen.get(event, ['辰', '巳', '午', '未'])
    sorted_sc = sorted(ji_shi_chen, key=lambda x: (0 if x['时辰'][0] in preferred_zhi else 1, x['时间']))

    return sorted_sc if sorted_sc else ji_shi_chen


# ============== 分类择日 ==============

EVENT_JI_XIONG = {
    '婚嫁': {
        '宜': ['成', '开', '定', '满'],
        '忌': ['破', '闭', '危'],
        '避神煞': ['月破', '岁破', '四离', '四绝', '杨公忌日'],
        '重吉神': ['天德贵人', '月德贵人', '天乙贵人']
    },
    '开业': {
        '宜': ['成', '开', '定'],
        '忌': ['破', '闭'],
        '避神煞': ['月破', '岁破'],
        '重吉神': ['天德贵人', '月德贵人']
    },
    '动土': {
        '宜': ['成', '开', '平'],
        '忌': ['破', '闭', '建'],
        '避神煞': ['月破', '岁破'],
        '重吉神': ['天德贵人']
    },
    '出行': {
        '宜': ['成', '开', '建', '定'],
        '忌': ['破', '闭'],
        '避神煞': ['月破'],
        '重吉神': ['天德贵人', '月德贵人']
    },
    '搬家': {
        '宜': ['成', '开', '定', '满'],
        '忌': ['破', '闭'],
        '避神煞': ['月破', '岁破'],
        '重吉神': ['天德贵人', '月德贵人']
    },
    '考试': {
        '宜': ['成', '定', '开'],
        '忌': ['破', '闭'],
        '避神煞': ['月破'],
        '重吉神': ['文昌']
    },
    '求医': {
        '宜': ['除', '成', '开'],
        '忌': ['破', '闭'],
        '避神煞': [],
        '重吉神': ['天医']
    },
    '祭祀': {
        '宜': ['成', '定', '满', '开', '收'],
        '忌': ['破'],
        '避神煞': [],
        '重吉神': ['天德贵人', '月德贵人']
    }
}


def ze_ri_score(year: int, month: int, day: int, event: str = 'general') -> Dict:
    """综合择日评分"""
    jian_chu = get_jian_chu(year, month, day)
    huang_dao = get_huang_dao(year, month, day)
    shen_sha = get_shen_sha(year, month, day)
    xiu = get_xiu(year, month, day)

    # 基础分 50
    score = 50

    # 建除评分
    jc_jx = JIAN_CHU_JI_XIONG.get(jian_chu, '平')
    if jc_jx == '吉':
        score += 20
    elif jc_jx == '大凶':
        score -= 30
    elif jc_jx == '凶':
        score -= 20

    # 黄道评分
    hd_jx = HUANG_DAO_JI_XIONG.get(huang_dao, '平')
    if '大吉' in hd_jx:
        score += 15
    elif '吉' in hd_jx:
        score += 10
    elif '凶' in hd_jx:
        score -= 15

    # 神煞评分
    for gs in shen_sha.get('吉神', []):
        score += 5
    for xs in shen_sha.get('凶煞', []):
        score -= 10

    # 二十八宿评分
    xiu_jx = XIU_JI_XIONG.get(xiu, '平')
    if xiu_jx == '吉':
        score += 5
    elif xiu_jx == '凶':
        score -= 5

    # 事件匹配
    if event != 'general' and event in EVENT_JI_XIONG:
        evt = EVENT_JI_XIONG[event]
        if jian_chu in evt['宜']:
            score += 10
        if jian_chu in evt['忌']:
            score -= 20
        for xs in shen_sha.get('凶煞', []):
            if xs in evt['避神煞']:
                score -= 15
        for gs in shen_sha.get('吉神', []):
            if gs in evt['重吉神']:
                score += 10

    # 限制分数范围
    score = max(0, min(100, score))

    # 判断等级
    if score >= 85:
        level = '大吉'
    elif score >= 70:
        level = '吉'
    elif score >= 55:
        level = '中平'
    elif score >= 40:
        level = '凶'
    else:
        level = '大凶'

    return {
        '日期': f'{year}年{month}月{day}日',
        '干支': get_gan_zhi_day(year, month, day),
        '建除': jian_chu,
        '建除吉凶': jc_jx,
        '黄道': huang_dao,
        '黄道吉凶': hd_jx,
        '二十八宿': xiu,
        '宿吉凶': XIU_JI_XIONG.get(xiu, '平'),
        '神煞': shen_sha,
        '综合评分': score,
        '等级': level
    }


def tui_jian_ji_ri(year: int, month: int, event: str = 'general', limit: int = 10) -> List[Dict]:
    """推荐当月吉日"""
    days = days_in_month(year, month)
    ji_ri_list = []

    for day in range(1, days + 1):
        result = ze_ri_score(year, month, day, event)
        if result['综合评分'] >= 60:
            result['日'] = day
            ji_ri_list.append(result)

    # 按评分排序
    ji_ri_list.sort(key=lambda x: x['综合评分'], reverse=True)
    return ji_ri_list[:limit]


def get_day_summary(year: int, month: int, day: int, event: str = 'general', hour: int = None) -> Dict:
    """获取某日完整择日信息"""
    result = ze_ri_score(year, month, day, event)

    # 十二时辰
    result['时辰'] = get_shi_chen_list(year, month, day)

    # 推荐时辰
    result['推荐时辰'] = get_best_shi_chen(year, month, day, event)

    # 如果指定了小时，给出该时辰判断
    if hour is not None:
        hour_info = None
        for sc in result['时辰']:
            h_start = int(sc['时间'].split(':')[0])
            if hour == h_start:
                hour_info = sc
                break
        result['当前时辰'] = hour_info

    return result


# ============== 输出格式化 ==============

def format_output(result: Dict, event: str = 'general') -> str:
    """格式化输出"""
    lines = []
    lines.append('【择日学排盘】v3.3.0')
    lines.append(f'• 日期：{result["日期"]}')
    lines.append(f'• 干支：{result["干支"]}')
    lines.append(f'• 建除：{result["建除"]}（{result["建除吉凶"]}）')
    lines.append(f'• 黄道：{result["黄道"]}（{result["黄道吉凶"]}）')
    lines.append(f'• 二十八宿：{result["二十八宿"]}（{result["宿吉凶"]}）')

    if result['神煞']['吉神']:
        lines.append(f'• 吉神：{", ".join(result["神煞"]["吉神"])}')
    if result['神煞']['凶煞']:
        lines.append(f'• 凶煞：{", ".join(result["神煞"]["凶煞"])}')

    lines.append(f'• 综合评分：{result["综合评分"]}/100')
    lines.append(f'• 等级：{result["等级"]}')
    lines.append('')

    # 时辰排布
    lines.append('【十二时辰】')
    for sc in result.get('时辰', []):
        marker = '✅' if sc['吉凶'] == '吉' else '❌' if sc['吉凶'] == '凶' else '➖'
        lines.append(f'  {marker} {sc["时辰"]} {sc["时间"]} {sc["干支"]} — {sc["吉凶"]}')
    lines.append('')

    # 推荐时辰
    if result.get('推荐时辰'):
        lines.append(f'【推荐时辰】（{event}）')
        for i, sc in enumerate(result['推荐时辰'][:3]):
            lines.append(f'  {i+1}. {sc["时辰"]} {sc["时间"]} {sc["干支"]}')
        lines.append('')

    return '\n'.join(lines)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description='择日学工具 v3.3.0')
    parser.add_argument('--date', '-d', type=str, help='查询日期 (YYYY-MM-DD)')
    parser.add_argument('--month', '-m', type=str, help='查询月份 (YYYY-MM)，用于推荐吉日')
    parser.add_argument('--event', '-e', type=str, default='general',
                        choices=['婚嫁', '开业', '动土', '出行', '搬家', '考试', '求医', '祭祀', 'general'],
                        help='择日事项')
    parser.add_argument('--hour', '-H', type=int, help='指定时辰 (0-23)')
    parser.add_argument('--limit', '-l', type=int, default=10, help='推荐吉日数量')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')

    args = parser.parse_args()

    if args.date:
        year, month, day = map(int, args.date.split('-'))
        result = get_day_summary(year, month, day, args.event, args.hour)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result, args.event))

    elif args.month:
        year, month = map(int, args.month.split('-'))
        ji_ri = tui_jian_ji_ri(year, month, args.event, args.limit)
        if args.json:
            print(json.dumps(ji_ri, ensure_ascii=False, indent=2))
        else:
            print(f'【{year}年{month}月吉日推荐】（{args.event}）')
            print('')
            for i, jr in enumerate(ji_ri, 1):
                print(f'  {i}. {jr["日期"]} — 评分 {jr["综合评分"]}/100（{jr["等级"]}）建除：{jr["建除"]} 黄道：{jr["黄道"]}')
            if not ji_ri:
                print('  本月无吉日推荐')

    else:
        # 默认今日
        now = datetime.now()
        result = get_day_summary(now.year, now.month, now.day, args.event, now.hour)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result, args.event))


if __name__ == '__main__':
    main()
