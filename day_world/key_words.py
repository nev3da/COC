"""
作者：Yuanl
日期：2025年7月25日
"""
import cv2
import json
import os
from common.utils import resourcePath, loadImg

BATTLE_TIME = 300
DIR = 'day_world'
ARM_DIR = f'{DIR}/arm_imgs'
CONTROL_DIR = f'{DIR}/control_imgs'
CUSTOM_ARM_DIR = f'{DIR}/custom_arms'
CUSTOM_ARM_JSON = resourcePath(os.path.join(DIR, 'custom_arms.json'))


TEMPLATES = {
    'build_army': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'build_army.png'))),
    'delete_confirm': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'delete_confirm.png'))),
    'build_dragon': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'build_dragon.png'))),
    'build_bat': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'build_bat.png'))),
    'build_airship': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'build_airship.png'))),
    'build_end': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'build_end.png'))),
    'search': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'search.png'))),
    'next': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'next.png'))),
    'backhome': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'backhome.png'))),
    'end_fight': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'end_fight.png'))),
    'giveup': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'giveup.png'))),
    'end_fight_confirm': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'end_fight_confirm.png'))),
    'victory_back': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'victory_back.png'))),
    'victory_star': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'victory_star.png'))),
    'attack': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'attack.png'))),
    'receive_chest': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'receive_chest.png'))),
    'chest_hammer': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'chest_hammer.png'))),
    'continue_chest': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'continue_chest.png'))),
    'castle_cake': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'castle_cake.png'))),
    'castle_confirm': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'castle_confirm.png'))),
    'castle_cancel': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'castle_cancel.png'))),

    'archer_queen': loadImg(resourcePath(os.path.join(ARM_DIR, 'archer_queen.png'))),
    'bbrking': loadImg(resourcePath(os.path.join(ARM_DIR, 'bbrking.png'))),
    'grand_warden': loadImg(resourcePath(os.path.join(ARM_DIR, 'grand_warden.png'))),
    'royal_champion': loadImg(resourcePath(os.path.join(ARM_DIR, 'royal_champion.png'))),
    'minion_prince': loadImg(resourcePath(os.path.join(ARM_DIR, 'minion_prince.png'))),
    'dragon_duke': loadImg(resourcePath(os.path.join(ARM_DIR, 'dragon_duke.png'))),
    'dragon': loadImg(resourcePath(os.path.join(ARM_DIR, 'dragon.png'))),
    'bat': loadImg(resourcePath(os.path.join(ARM_DIR, 'bat.png'))),
    'airship': loadImg(resourcePath(os.path.join(ARM_DIR, 'airship.png'))),
    'switch': loadImg(resourcePath(os.path.join(ARM_DIR, 'switch.png'))),
    'switch_airship': loadImg(resourcePath(os.path.join(ARM_DIR, 'switch_airship.png'))),
}

# 动态加载用户自定义兵种图片
CUSTOM_TROOPS: list[tuple[str, int]] = []
if os.path.exists(CUSTOM_ARM_JSON):
    with open(CUSTOM_ARM_JSON, 'r', encoding='utf-8') as f:
        custom_cfg = json.load(f)
    for troop in custom_cfg.get('custom_troops', []):
        # 去掉 .png 作为键名
        key = os.path.splitext(troop['filename'])[0]
        img_path = resourcePath(os.path.join(CUSTOM_ARM_DIR, troop['filename']))
        if not os.path.exists(img_path):
            print(f"[custom_arms] 警告：自定义图片不存在，已跳过：{img_path}")
            continue
        TEMPLATES[key] = loadImg(img_path)
        CUSTOM_TROOPS.append((key, troop.get('count', 1)))


if __name__ == '__main__':
    pass
