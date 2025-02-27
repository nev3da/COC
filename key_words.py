"""
作者：Yuanl
日期：2024年12月22日
"""
import cv2
import os

ARM_DIR = 'arm_imgs'
CONTROL_DIR = 'control_imgs'
RESOURCE_DIR = 'resource_imgs'

UNITS = {
    '龙': 'dragon',
    '女巫': 'witch',
    '变异亡灵': 'fly',
}
TEMPLATES = {
    'search': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'search.png')), cv2.COLOR_BGR2RGB),
    'endfight': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'endfight.png')), cv2.COLOR_BGR2RGB),
    'confirm': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'confirm.png')), cv2.COLOR_BGR2RGB),
    'backhome': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'backhome.png')), cv2.COLOR_BGR2RGB),
    'victory_star': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'victory_star.png')), cv2.COLOR_BGR2RGB),
    'cancel': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'cancel.png')), cv2.COLOR_BGR2RGB),
    'war_machine': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'warmachine.png')), cv2.COLOR_BGR2RGB),
    'helicopter': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'helicopter.png')), cv2.COLOR_BGR2RGB),
    'dragon': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'dragon.png')), cv2.COLOR_BGR2RGB),
    'witch': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'witch.png')), cv2.COLOR_BGR2RGB),
    'fly': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'fly.png')), cv2.COLOR_BGR2RGB),
    'skill': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'skill.png')), cv2.COLOR_BGR2RGB),
    'elixir1': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'elixir1.png')), cv2.COLOR_BGR2RGB),
    'elixir2': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'elixir2.png')), cv2.COLOR_BGR2RGB),
    'collect': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'collect.png')), cv2.COLOR_BGR2RGB),
    'close': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'close.png')), cv2.COLOR_BGR2RGB),
}