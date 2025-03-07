"""
作者：yuanl
日期：2024年12月24日
"""
import win32con
import win32gui
import win32print
import win32api
from win32api import GetSystemMetrics
import time
import cv2
import pynput
import numpy as np
from PIL import ImageGrab
from log import logger
import pyautogui


def saveScreen(img_name):
    scr_shot = ImageGrab.grab()
    scr_shot = np.array(scr_shot)
    cv2.imwrite(img_name, cv2.cvtColor(scr_shot, cv2.COLOR_RGB2BGR))


def getScaling():
    soft_width = GetSystemMetrics(0)
    screen_width = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
    scaling = round(screen_width / soft_width * 100) / 100
    return scaling


def getWindowLocation(title='MuMu模拟器12'):
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


def zoomOut(kb, ms, midPos, times=10):
    # press ctrl with kb
    ms.position = midPos
    time.sleep(0.1)
    kb.press(pynput.keyboard.Key.ctrl)
    time.sleep(0.1)
    for _ in range(times):
        ms.scroll(0, -1)
        time.sleep(0.1)
    pyautogui.scroll(-10000)
    time.sleep(0.1)
    kb.release(pynput.keyboard.Key.ctrl)


def moveThenClick(ms, pos, duration=0.1):
    ms.position = pos
    time.sleep(duration)
    ms.click(pynput.mouse.Button.left)


def getMidCoordinate(window_loc, template, scr_shot=None, threshold=0.95):
    if scr_shot is None:
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
    res = cv2.matchTemplate(scr_shot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    if max_val < threshold:
        return None
    else:
        x, y = max_loc
        return window_loc[0] + x + template.shape[1] // 2, window_loc[1] + y + template.shape[0] // 2

def getBottomCoordinate(window_loc, template, scr_shot=None, threshold=0.95):
    if scr_shot is None:
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
    res = cv2.matchTemplate(scr_shot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val < threshold:
        return None
    else:
        x, y = max_loc
        return window_loc[0] + x + template.shape[1] // 2, window_loc[1] + y + template.shape[0]

def getTopCoordinate(window_loc, template, scr_shot=None, threshold=0.95):
    if scr_shot is None:
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
    res = cv2.matchTemplate(scr_shot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val < threshold:
        return None
    else:
        x, y = max_loc
        return window_loc[0] + x + template.shape[1] // 2, window_loc[1] + y


def matchThenClick(ms, template, window_loc, mid=True):
    pos = getMidCoordinate(window_loc, template) if mid else getBottomCoordinate(window_loc, template)
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


if __name__ == '__main__':
    kb = pynput.keyboard.Controller()
    ms = pynput.mouse.Controller()
    kb.press(pynput.keyboard.Key.ctrl)
    time.sleep(2)
    for _ in range(10):
        ms.scroll(0, -1)
        time.sleep(0.1)
    time.sleep(1)
    kb.release(pynput.keyboard.Key.ctrl)
