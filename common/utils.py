"""
作者：yuanl
日期：2024年12月24日
"""
import ctypes
import win32con
import win32gui
import win32api
import time
import cv2
import numpy as np
import os
import sys
from paddleocr import PaddleOCR
import win32ui

from common.log import logger


class WindowCapture:
    def __init__(self, hwnd: int, window_offset: int = 0):
        self.hwnd = hwnd
        self.window_offset = window_offset
        self.initResources()

    def initResources(self):
        self.w, self.h = getWindowSize(self.hwnd)
        # DC
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        # Bitmap
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
        self.saveDC.SelectObject(self.saveBitMap)

    def grab(self) -> np.ndarray:
        # 后台截图
        result = ctypes.windll.user32.PrintWindow(
            self.hwnd,
            self.saveDC.GetSafeHdc(),
            2
        )
        if not result:
            raise RuntimeError("PrintWindow failed")

        bmpstr = self.saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8)
        img.shape = (self.h, self.w, 4)
        return cv2.cvtColor(img[self.window_offset:, :, :3], cv2.COLOR_BGR2RGB)

    def release(self):
        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)


def getWindowSize(
    hwnd: int
):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top
    return w, h


def zoomOut(
    hwnd: int,
    times: int = 20,
):
    w, h = getWindowSize(hwnd)
    x, y = w // 2, h // 2
    # 转换为屏幕坐标
    screen_point = win32gui.ClientToScreen(hwnd, (x, y))
    lparam = win32api.MAKELONG(screen_point[0], screen_point[1])
    wparam = win32api.MAKELONG(0, -win32con.WHEEL_DELTA)
    for _ in range(times):
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEWHEEL, wparam, lparam)
        time.sleep(0.05)


def shiftScreen(
    hwnd: int,
    mid_pos: tuple[int, int],
    times: int = 4
):
    x, y1 = mid_pos
    y2 = y1
    interval = 0.01
    steps = 30
    pixel_per_time = 100 * (times // abs(times))
    for _ in range(abs(times)):
        # 移动到起点
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y1))
        time.sleep(interval)
        # 左键按下
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y1))
        time.sleep(interval)
        # 拖动
        for i in range(1, steps + 1):
            y2 = y1 + pixel_per_time * i // steps
            win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, win32api.MAKELONG(x, y2))
            time.sleep(interval)
        # 左键抬起
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(x, y2))
        time.sleep(0.5)


def click(
    hwnd: int,
    pos: tuple[int, int]
):
    lparam = win32api.MAKELONG(pos[0], pos[1])
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(0.01)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lparam)


def getTemplatePos(
    hwnd: int,
    cap: WindowCapture,
    template: np.ndarray,
    scr_shot: np.ndarray = None,
    threshold: float = 0.95,
    offset: str = "mid",
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
):
    w, h = getWindowSize(hwnd)
    if scr_shot is None:
        scr_shot = cap.grab()
        scr_shot = scr_shot[round(h * crop[0]):round(h * crop[1]), round(w * crop[2]):round(w * crop[3]), :]
    res = cv2.matchTemplate(scr_shot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val < threshold:
        return None
    else:
        x, y = max_loc
        if offset == "mid":
            return (
                round(w * crop[2]) + x + template.shape[1] // 2,
                round(h * crop[0]) + y + template.shape[0] // 2,
            )
        elif offset == "top":
            return (
                round(w * crop[2]) + x + template.shape[1] // 2,
                round(h * crop[0]) + y
            )
        elif offset == "bottom":
            return (
                round(w * crop[2]) + x + template.shape[1] // 2,
                round(h * crop[0]) + y + template.shape[0] + 30,
            )
        else:
            return None


def getOcrPos(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    character: str,
    scr_shot: np.ndarray = None,
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0)
):
    w, h = getWindowSize(hwnd)
    if scr_shot is None:
        scr_shot = cap.grab()
        scr_shot = scr_shot[round(h * crop[0]):round(h * crop[1]), round(w * crop[2]):round(w * crop[3]), :]
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
            pos = (round(w * crop[2]) + mid_point[0], round(h * crop[0]) + mid_point[1])
            return pos
    return None


def matchTemplateThenClick(
    hwnd: int,
    cap: WindowCapture,
    template: np.ndarray,
    offset: str = 'mid',
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
):
    pos = getTemplatePos(hwnd, cap, template, offset=offset, crop=crop)
    if pos:
        click(hwnd, pos)
        time.sleep(1)
        return True
    return False


def matchOcrThenClick(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    character: str,
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0)
):
    pos = getOcrPos(hwnd, cap, ocr, character, crop=crop)
    if pos:
        click(hwnd, pos)
        time.sleep(1)
        return True
    return False


def waitUntilMatchThenClick(
    hwnd: int,
    cap: WindowCapture,
    template: np.ndarray,
    interval: float = 0,
    timeout: float = 10.0,
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return False
        if matchTemplateThenClick(hwnd, cap, template, crop=crop):
            return True
        time.sleep(interval)


def waitUntilOcrThenClick(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    character: str,
    interval: float = 0,
    timeout: float = 10.0,
    crop: tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return False
        if matchOcrThenClick(hwnd, cap, ocr, character, crop=crop):
            return True
        time.sleep(interval)


def logThenExit(
    msg: str,
    img_name: str,
    quit: bool = True
):
    # saveScreen(img_name)
    if quit:
        logger.critical(msg)
        raise RuntimeError(msg)
    else:
        logger.warning(msg)


def resourcePath(relative_path: str) -> str:
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generateGaussianPoints(
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    num_points: int = 11
):
    x_mid, y_mid = (x1 + x2) // 2, (y1 + y2) // 2
    # 向量方向和长度
    vec = np.array([x2 - x1, y2 - y1])
    length = np.linalg.norm(vec)
    if length == 0:
        return [(x_mid, y_mid)] * num_points

    # 单位向量
    unit_vec = vec / length
    # 2σ = length/2，从正态分布采样
    t_values = np.random.normal(loc=0, scale=length / 4, size=num_points)

    # 如果超出 [-length/2, length/2]，则移到中点
    points = []
    for t in t_values:
        if abs(t) > length / 2:
            pt = np.array([x_mid, y_mid])
        else:
            pt = np.array([x_mid, y_mid]) + t * unit_vec
        points.append(tuple(np.round(pt).astype(int)))

    return points


def formatInt(n: int) -> str:
    s = str(n)
    parts = []
    while s:
        parts.insert(0, s[-3:])
        s = s[:-3]
    return ' '.join(parts)


if __name__ == "__main__":
    points = generateGaussianPoints(848, 744, 1367, 355, 1108, 550, num_points=11)
    from matplotlib import pyplot as plt
    plt.figure(figsize=(10, 10))
    for pt in points:
        plt.scatter(pt[0], pt[1], color='blue')
    plt.xlim(0, 1920)
    plt.ylim(0, 1080)
    plt.gca().invert_yaxis()  # 反转y轴
    plt.title("Gaussian Points")
    plt.show()
