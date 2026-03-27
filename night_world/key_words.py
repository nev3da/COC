"""
作者：Yuanl
日期：2024年12月22日
"""
import os
from common.utils import resourcePath, loadImg

BATTLE_TIME = 120   # 战斗时间
DIR = 'night_world'
ARM_DIR = f'{DIR}/arm_imgs'
CONTROL_DIR = f'{DIR}/control_imgs'
RESOURCE_DIR = f'{DIR}/resource_imgs'

UNITS = {
    '龙': 'dragon',
    '女巫': 'witch',
    '变异亡灵': 'fly',
}
TEMPLATES = {
    'search': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'search.png'))),
    'endfight': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'endfight.png'))),
    'confirm': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'confirm.png'))),
    'backhome': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'backhome.png'))),
    'victory_star': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'victory_star.png'))),
    'cancel': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'cancel.png'))),
    'giveup': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'giveup.png'))),
    'giveup_confirm': loadImg(resourcePath(os.path.join(CONTROL_DIR, 'giveup_confirm.png'))),

    'war_machine': loadImg(resourcePath(os.path.join(ARM_DIR, 'warmachine.png'))),
    'helicopter': loadImg(resourcePath(os.path.join(ARM_DIR, 'helicopter.png'))),
    'dragon': loadImg(resourcePath(os.path.join(ARM_DIR, 'dragon.png'))),
    'witch': loadImg(resourcePath(os.path.join(ARM_DIR, 'witch.png'))),
    'fly': loadImg(resourcePath(os.path.join(ARM_DIR, 'fly.png'))),
    'skill': loadImg(resourcePath(os.path.join(ARM_DIR, 'skill.png'))),
    'machine_skill': loadImg(resourcePath(os.path.join(ARM_DIR, 'machine_skill.png'))),

    'elixir1': loadImg(resourcePath(os.path.join(RESOURCE_DIR, 'elixir1.png'))),
    'elixir2': loadImg(resourcePath(os.path.join(RESOURCE_DIR, 'elixir2.png'))),
    'collect': loadImg(resourcePath(os.path.join(RESOURCE_DIR, 'collect.png'))),
    'close': loadImg(resourcePath(os.path.join(RESOURCE_DIR, 'close.png'))),
    'axe': resourcePath(os.path.join(RESOURCE_DIR, 'axe'))
}

if __name__ == '__main__':
    for name in os.listdir(TEMPLATES['axe']):
        print(os.path.join(TEMPLATES['axe'], name))
