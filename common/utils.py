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
from common.log import logger
import pyautogui
from PyQt5.QtCore import QThread
import os
import sys
from paddleocr import PaddleOCR


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
            win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
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
    ms: pynput.mouse.Controller,
    pos: tuple[int, int],
    duration: float = 0.1
):
    ms.position = pos
    time.sleep(duration)
    ms.click(pynput.mouse.Button.left)


def getTemplatePos(
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


def getOcrPos(
    window_loc: tuple[int, int, int, int],
    character: str,
    ocr: PaddleOCR,
    scr_shot: np.ndarray = None,
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0)
):
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    if scr_shot is None:
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)[round(h * crop[0]):round(h * crop[1]), round(w * crop[2]):round(w * crop[3]), :]
    result = ocr.predict(scr_shot)
    if not result[0]:
        return None
    for idx, line in enumerate(result[0]['rec_texts']):
        if character in line:
            four_corner = result[0]['rec_polys'][idx]
            mid_point = (
                round((four_corner[0][0] + four_corner[1][0]) / 2),
                round((four_corner[0][1] + four_corner[3][1]) / 2),
            )
            pos = (left + mid_point[0] + round(w * crop[2]), top + mid_point[1] + round(h * crop[0]))
            return pos
    return None


def matchTemplateThenClick(
    ms: pynput.mouse.Controller,
    template: np.ndarray,
    window_loc: tuple[int, int, int, int],
    mid: bool = True,
):
    pos = getTemplatePos(window_loc, template) if mid else getTemplatePos(window_loc, template, pos="bottom")
    if pos:
        moveThenClick(ms, pos)
        time.sleep(1)
        return True
    return False


def matchOcrThenClick(
    ms: pynput.mouse.Controller,
    character: str,
    ocr: PaddleOCR,
    window_loc: tuple[int, int, int, int],
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0)
):
    pos = getOcrPos(window_loc, character, ocr, crop=crop)
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
        if matchTemplateThenClick(ms, template, window_loc):
            return True
        time.sleep(interval)


def waitUntilOcrThenClick(
    ms: pynput.mouse.Controller,
    character: str,
    ocr: PaddleOCR,
    window_loc: tuple[int, int, int, int],
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
    interval: float = 0,
    timeout: float = 10.0,
):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return False
        if matchOcrThenClick(ms, character, ocr, window_loc, crop=crop):
            return True
        time.sleep(interval)


def logThenExit(msg: str, img_name: str, quit: bool = True):
    # saveScreen(img_name)
    if quit:
        logger.critical(msg)
        raise RuntimeError(msg)
    else:
        logger.warning(msg)


def resource_path(relative_path: str) -> str:
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_gaussian_points(x1, y1, x2, y2, x0, y0, num_points=11):
    # 向量方向和长度
    vec = np.array([x2 - x1, y2 - y1])
    length = np.linalg.norm(vec)
    if length == 0:
        return [(x0, y0)] * num_points

    unit_vec = vec / length  # 单位向量

    std = length / 4  # 2σ = 半个长度 → σ = length/4

    # 从正态分布采样一维偏移量
    t_values = np.random.normal(loc=0, scale=std, size=num_points)

    # 限制范围：如果超出 [-length/2, length/2]，则移到中点
    points = []
    for t in t_values:
        if abs(t) > length / 2:
            pt = np.array([x0, y0])
        else:
            pt = np.array([x0, y0]) + t * unit_vec
        points.append(tuple(np.round(pt).astype(int)))

    return points


if __name__ == "__main__":
    points = generate_gaussian_points(848, 744, 1367, 355, 1108, 550, num_points=11)
    from matplotlib import pyplot as plt
    plt.figure(figsize=(10, 10))
    for pt in points:
        plt.scatter(pt[0], pt[1], color='blue')
    plt.xlim(0, 1920)
    plt.ylim(0, 1080)
    plt.gca().invert_yaxis()  # 反转y轴
    plt.title("Gaussian Points")
    plt.show()
