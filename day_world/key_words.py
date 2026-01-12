"""
作者：Yuanl
日期：2025年7月25日
"""
import cv2
import os
from common.utils import resourcePath

BATTLE_TIME = 300
DIR = 'day_world'
ARM_DIR = f'{DIR}/arm_imgs'
CONTROL_DIR = f'{DIR}/control_imgs'


TEMPLATES = {
    'build_army': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_army.png'))), cv2.COLOR_BGR2RGB),
    'delete': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'delete.png'))), cv2.COLOR_BGR2RGB),
    'delete_confirm': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'delete_confirm.png'))), cv2.COLOR_BGR2RGB),
    'build_dragon': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_dragon.png'))), cv2.COLOR_BGR2RGB),
    'build_rage': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_rage.png'))), cv2.COLOR_BGR2RGB),
    'build_lightning': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_lightning.png'))), cv2.COLOR_BGR2RGB),
    'build_bat': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_bat.png'))), cv2.COLOR_BGR2RGB),
    'build_airship': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_airship.png'))), cv2.COLOR_BGR2RGB),
    'build_end': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'build_end.png'))), cv2.COLOR_BGR2RGB),
    'search': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'search.png'))), cv2.COLOR_BGR2RGB),
    'found': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'found.png'))), cv2.COLOR_BGR2RGB),
    'next': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'next.png'))), cv2.COLOR_BGR2RGB),
    'backhome': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'backhome.png'))), cv2.COLOR_BGR2RGB),
    'end_fight': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'end_fight.png'))), cv2.COLOR_BGR2RGB),
    'giveup': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'giveup.png'))), cv2.COLOR_BGR2RGB),
    'end_fight_confirm': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'end_fight_confirm.png'))), cv2.COLOR_BGR2RGB),
    'victory_back': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'victory_back.png'))), cv2.COLOR_BGR2RGB),
    'victory_star': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'victory_star.png'))), cv2.COLOR_BGR2RGB),
    'attack': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'attack.png'))), cv2.COLOR_BGR2RGB),
    'receive_chest': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'receive_chest.png'))), cv2.COLOR_BGR2RGB),
    'chest_hammer': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'chest_hammer.png'))), cv2.COLOR_BGR2RGB),
    'continue_chest': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'continue_chest.png'))), cv2.COLOR_BGR2RGB),
    'castle_cake': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'castle_cake.png'))), cv2.COLOR_BGR2RGB),
    'castle_confirm': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'castle_confirm.png'))), cv2.COLOR_BGR2RGB),
    'castle_cancel': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(CONTROL_DIR, 'castle_cancel.png'))), cv2.COLOR_BGR2RGB),

    'archer_queen': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'archer_queen.png'))), cv2.COLOR_BGR2RGB),
    'bbrking': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'bbrking.png'))), cv2.COLOR_BGR2RGB),
    'grand_warden': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'grand_warden.png'))), cv2.COLOR_BGR2RGB),
    'royal_champion': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'royal_champion.png'))), cv2.COLOR_BGR2RGB),
    'minion_prince': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'minion_prince.png'))), cv2.COLOR_BGR2RGB),
    'dragon': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'dragon.png'))), cv2.COLOR_BGR2RGB),
    'lightning': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'lightning.png'))), cv2.COLOR_BGR2RGB),
    'rage': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'rage.png'))), cv2.COLOR_BGR2RGB),
    'bat': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'bat.png'))), cv2.COLOR_BGR2RGB),
    'airship': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'airship.png'))), cv2.COLOR_BGR2RGB),
    'switch': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'switch.png'))), cv2.COLOR_BGR2RGB),
    'switch_airship': cv2.cvtColor(cv2.imread(resourcePath(os.path.join(ARM_DIR, 'switch_airship.png'))), cv2.COLOR_BGR2RGB),
}

if __name__ == '__main__':
    pass
