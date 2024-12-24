"""
作者：yuanl
日期：2024年12月22日
"""
import os.path
import time

import cv2
import win32con
import win32gui
import win32print
import win32api
from win32api import GetSystemMetrics
import pynput
import key_words
import pyautogui
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageGrab
from matplotlib import pyplot as plt
from key_words import *
from log import logger

def saveScreen(img_name):
    scr_shot = ImageGrab.grab()
    scr_shot = np.array(scr_shot)
    cv2.imwrite(img_name, cv2.cvtColor(scr_shot, cv2.COLOR_RGB2BGR))

def getScaling():
    soft_width = GetSystemMetrics(0)
    screen_width = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
    scaling = round(screen_width / soft_width * 100) / 100
    return scaling

def getWindowLocation(title='MuMU模拟器12'):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        logger.error('游戏没开，或窗口名称错误')
        exit(0)
    else:
        try:
            # 发送还原最小化窗口的信息
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            time.sleep(0.1)
            # 设为高亮
            win32gui.SetForegroundWindow(hwnd)
        finally:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            return hwnd, (left, top, right, bottom)

def zoomOut(kb, ms, midPos, times=10000):
    # press ctrl with kb
    kb.press(pynput.keyboard.Key.ctrl)
    time.sleep(0.01)
    ms.position = midPos
    time.sleep(0.01)
    for _ in range(times):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
    time.sleep(0.01)
    kb.release(pynput.keyboard.Key.ctrl)

def moveThenClick(ms, pos, duration=0.1):
    ms.position = pos
    time.sleep(duration)
    ms.click(pynput.mouse.Button.left)

def getMidCoordinate(window_loc, template, screenshot=None, threshold=0.95):
    if screenshot is None:
        screenshot = ImageGrab.grab(window_loc)
        screenshot = np.array(screenshot)
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val < threshold:
        return None
    else:
        x, y = max_loc
        return window_loc[0] + x + template.shape[1] // 2, window_loc[1] + y + template.shape[0] // 2

def collect(kb, ms, window_loc, templates):
    left, top, right, bottom = window_loc
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    zoomOut(kb, ms, mid_pos, times=2000)
    for _ in range(4):
        ms.position = mid_pos
        pyautogui.mouseDown()   # 按下鼠标左键
        time.sleep(0.1)
        pyautogui.moveTo(mid_pos[0], mid_pos[1] + 200, duration=0.2)    # 向上移
        time.sleep(0.1)
        pyautogui.mouseUp()
    time.sleep(1)
    logger.info('识别圣水车')
    wheelbarrow_pos = getMidCoordinate(window_loc, templates['elixir1'], threshold=0.8)
    if not wheelbarrow_pos:
        wheelbarrow_pos = getMidCoordinate(window_loc, templates['elixir2'], threshold=0.8)
        if not wheelbarrow_pos:
            logThenExit('未找到圣水车', 'no_wheelbarrow.png', quit=False)
            return
    moveThenClick(ms, wheelbarrow_pos)
    time.sleep(1)
    logger.info('识别收集和关闭按钮')
    collect_pos = getMidCoordinate(window_loc, templates['collect'])
    close_pos = getMidCoordinate(window_loc, templates['close'])
    if not close_pos:
        logThenExit('未找到关闭按钮', 'no_close.png')
    if collect_pos:     # 如果找到收集按钮就点一下，没找到可能是因为圣水满了，收集按钮变灰，识别不到，所以直接点关闭
        logger.info('收集')
        moveThenClick(ms, collect_pos)
        time.sleep(1)
    logger.info('关闭')
    moveThenClick(ms, close_pos)

def getAttackPos(window_loc, ocr):
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    scr_shot = ImageGrab.grab(window_loc)
    scr_shot = np.array(scr_shot)
    result = ocr.ocr(scr_shot[round(1 / 2 * h):, : round(1 / 2 * w), :])
    if not result[0]:
        return None
    for line in result[0]:
        if '进攻' in line[1][0]:
            four_corner = line[0]
            mid_point = (round((four_corner[0][0] + four_corner[1][0]) / 2), round((four_corner[0][1] + four_corner[2][1]) / 2))
            attack_pos = (left + mid_point[0], top + mid_point[1] + round(1 / 2 * h))
            return attack_pos
    return None

def waitUntilMatch(ocr, window_loc, time_limit=10.0):
    time.sleep(1)
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    start_time = time.time()
    while True:
        if time.time() - start_time >= time_limit:
            return False
        logger.info(f'正在匹配对手：[{time.time() - start_time:.2f}/{time_limit:.2f}]')
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        result = ocr.ocr(scr_shot[: round(1 / 3 * h), round(1 / 3 * w): , :])
        if not result[0]:
            time.sleep(1)
            continue
        for line in result[0]:
            if '进攻' in line[1][0]:
                return True

def matchThenClick(ms, template, window_loc):
    pos = getMidCoordinate(window_loc, template)
    if pos:
        moveThenClick(ms, pos)
        time.sleep(1)
        return True
    return False

def logThenExit(msg, img_name, quit=True):
    if quit:
        logger.critical(msg)
    else:
        logger.warning(msg)
    saveScreen(img_name)
    if quit:
        exit(0)


def attack(kb, ms, window_loc, ocr, templates):
    left, top, right, bottom = window_loc
    search_times = 5
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getAttackPos(window_loc, ocr)
            if not attack_pos:
                logThenExit('未找到进攻按钮', 'no_attack.png')
            moveThenClick(ms, attack_pos)
            time.sleep(1)
            if not matchThenClick(ms, templates['search'], window_loc):
                logThenExit('未找到搜索按钮', 'no_search.png')
            if waitUntilMatch(ocr, window_loc):     # 找到对手
                find = True
                break
            else:   # 规定时间内未找到对手
                logger.info(f'规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]')
                if not matchThenClick(ms, templates['cancel'], window_loc):
                    logThenExit('未找到取消按钮', 'no_cancel.png')
            time.sleep(3)
        if find:
            logger.info('开始进攻')
            break
        else:
            logger.warning(f'连续{search_times}次未找到对手，等半分钟再搜')
            time.sleep(30)
    # 开打
    start_time = time.time()
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    place_arms_pos = (mid_pos[0], top + 755)
    zoomOut(kb, ms, mid_pos)
    scr_shot = ImageGrab.grab(window_loc)
    scr_shot = np.array(scr_shot)
    for _ in range(4):  # 屏幕下移
        ms.position = mid_pos
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.moveTo(mid_pos[0], mid_pos[1] - 200, duration=0.2)
        time.sleep(0.1)
        pyautogui.mouseUp()
    war_machine_pos = getMidCoordinate(window_loc, templates['war_machine'], scr_shot)
    if war_machine_pos:
        logger.info('放战争机器')
        moveThenClick(ms, war_machine_pos)
        time.sleep(0.2)
        moveThenClick(ms, place_arms_pos)
        time.sleep(0.2)
    dragon_pos = getMidCoordinate(window_loc, templates['dragon'], scr_shot)
    if dragon_pos:
        logger.info('放龙')
        moveThenClick(ms, dragon_pos)
        time.sleep(0.2)
        ms.position = place_arms_pos
        time.sleep(0.2)
        for _ in range(4):
            ms.click(pynput.mouse.Button.left)
            time.sleep(0.2)
    ms.position = mid_pos   # 鼠标移动到中心
    while True: # 等待战斗结束
        logger.info(f'等待战斗结束：[{time.time() - start_time:.2f}/{TIME_LIMIT:.2f}]')
        if time.time() - start_time >= TIME_LIMIT:
            logger.info('进入二阶段了，但是不打二阶段')
            if matchThenClick(ms, templates['endfight'], window_loc):
                logger.info('结束战斗')
                time.sleep(1)
                if matchThenClick(ms, templates['confirm'], window_loc):
                    logger.info('确认')
                    time.sleep(1)
                    if matchThenClick(ms, templates['backhome'], window_loc):
                        logger.info('回营')
                        break
                    else:
                        logThenExit('未找到回营按钮', 'no_backhome.png')
                else:
                    logThenExit('未找到确认按钮', 'no_confirm.png')
            else:
                logThenExit('未找到结束战斗按钮', 'no_endfight.png')
        if matchThenClick(ms, templates['backhome'], window_loc):
            logger.info('回营') 
            break
        time.sleep(5)

def main(collect_interval=4, execute_time=3):
    """
    :param collect_interval: 收集间隔（场）
    :param execute_time: 执行时间（小时）
    """
    if getScaling() != 1.0:
        logger.error('请将显示设置为100%')
        exit(0)
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title='MuMu模拟器12')[1]
    left, top, right, bottom = window_loc
    templates = {
        'search': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'search.png')), cv2.COLOR_BGR2RGB),
        'endfight': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'endfight.png')), cv2.COLOR_BGR2RGB),
        'confirm': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'confirm.png')), cv2.COLOR_BGR2RGB),
        'backhome': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'backhome.png')), cv2.COLOR_BGR2RGB),
        'victory_star': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'victory_star.png')), cv2.COLOR_BGR2RGB),
        'cancel': cv2.cvtColor(cv2.imread(os.path.join(CONTROL_DIR, 'cancel.png')), cv2.COLOR_BGR2RGB),
        'war_machine': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'warmachine.png')), cv2.COLOR_BGR2RGB),
        'dragon': cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'dragon.png')), cv2.COLOR_BGR2RGB),
        'elixir1': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'elixir1.png')), cv2.COLOR_BGR2RGB),
        'elixir2': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'elixir2.png')), cv2.COLOR_BGR2RGB),
        'collect': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'collect.png')), cv2.COLOR_BGR2RGB),
        'close': cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'close.png')), cv2.COLOR_BGR2RGB),
    }
    execute_time *= (60 * 60)
    start_time = time.time()
    
    while True:
        for _ in range(collect_interval):   # 每打collect_interval场战斗，就收集一次圣水
            zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))    # 缩小视野至最小
            attack(keyboard, mouse, window_loc, ocr, templates)     # 进攻
            time.sleep(6)
            logger.info('检查胜利之星')
            matchThenClick(mouse, templates['victory_star'], window_loc)    # 检查是否弹出胜利之星奖励
        collect(keyboard, mouse, window_loc, templates)     # 收集圣水
        if time.time() - start_time >= execute_time:        # 判断是否到达执行时间，
            break
    


if __name__ == '__main__':
    main()
    # keyboard = pynput.keyboard.Controller()
    # mouse = pynput.mouse.Controller()
    # left, top, right, bottom = getWindowLocation(title='MuMu模拟器12')[1]
    # time.sleep(1)
    # template = cv2.cvtColor(cv2.imread(os.path.join(RESOURCE_DIR, 'elixir2.png')), cv2.COLOR_BGR2RGB)
    # src = ImageGrab.grab((left, top, right, bottom))
    # src = np.array(src)
    # pos = getMidCoordinate((left, top, right, bottom), template, src)
    # if pos:
    #     mouse.position = pos
    # else:
    #     print('未找到')