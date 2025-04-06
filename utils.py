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
from PyQt5.QtCore import QThread


def saveScreen(img_name):
    scr_shot = ImageGrab.grab()
    scr_shot = np.array(scr_shot)
    cv2.imwrite(img_name, cv2.cvtColor(scr_shot, cv2.COLOR_RGB2BGR))


def getScaling():
    soft_width = GetSystemMetrics(0)
    screen_width = win32print.GetDeviceCaps(
        win32gui.GetDC(0), win32con.DESKTOPHORZRES)
    scaling = round(screen_width / soft_width * 100) / 100
    return scaling


def getWindowLocation(title="MuMu模拟器12"):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        logger.error("游戏没开，或窗口名称错误")
        raise RuntimeError("游戏没开，或窗口名称错误")
    else:
        try:
            # 发送还原最小化窗口的信息
            win32gui.SendMessage(
                hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            time.sleep(0.1)
            # 设为高亮
            win32gui.SetForegroundWindow(hwnd)
        finally:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            return hwnd, (left, top, right, bottom)


def zoomOut(
    kb: pynput.keyboard.Controller,
    ms: pynput.mouse.Controller,
    midPos: tuple[int, int],
    times: int = 10,
):
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


def shiftScreen(mid_pos: tuple[int, int], times: int = 4):
    for _ in range(abs(times)):
        # move cursor
        pyautogui.moveTo(mid_pos[0], mid_pos[1], duration=0.01)
        # 按下鼠标左键
        pyautogui.mouseDown()
        time.sleep(0.1)
        # 向上/下移
        pyautogui.moveTo(
            mid_pos[0], mid_pos[1] + (200 if times > 0 else -200), duration=0.2
        )
        time.sleep(0.1)
        pyautogui.mouseUp()


def moveThenClick(
    ms: pynput.mouse.Controller, pos: tuple[int, int], duration: float = 0.1
):
    ms.position = pos
    time.sleep(duration)
    ms.click(pynput.mouse.Button.left)


def getCoordinate(
    window_loc: tuple[int, int, int, int],
    template: np.ndarray,
    scr_shot: np.ndarray = None,
    threshold: float = 0.95,
    pos: str = "mid",
):
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
        if pos == "mid":
            return (
                window_loc[0] + x + template.shape[1] // 2,
                window_loc[1] + y + template.shape[0] // 2,
            )
        elif pos == "top":
            return window_loc[0] + x + template.shape[1] // 2, window_loc[1] + y
        elif pos == "bottom":
            return (
                window_loc[0] + x + template.shape[1] // 2,
                window_loc[1] + y + template.shape[0] + 30,
            )
        else:
            return None


def matchThenClick(
    ms: pynput.mouse.Controller,
    template: np.ndarray,
    window_loc: tuple[int, int, int, int],
    mid: bool = True,
):
    pos = (
        getCoordinate(window_loc, template)
        if mid
        else getCoordinate(window_loc, template, pos="bottom")
    )

    if pos:
        moveThenClick(ms, pos)
        time.sleep(1)
        return True
    return False


def waitUntilMatchThenClick(
    ms: pynput.mouse.Controller,
    template: np.ndarray,
    window_loc: tuple[int, int, int, int],
    interval: float = 0,
    timeout: float = 10.0,
):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return False
        if matchThenClick(ms, template, window_loc):
            return True
        time.sleep(interval)


def logThenExit(msg: str, img_name: str, quit: bool = True):
    saveScreen(img_name)
    if quit:
        logger.critical(msg)
        raise RuntimeError(msg)
    else:
        logger.warning(msg)


if __name__ == "__main__":
    print(type(abs(4)))
