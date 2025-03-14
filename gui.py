"""
作者：yuanl
日期：2024年10月21日
"""

import ui
from script import attack, collect, attackWithNoArms
from key_words import *
from utils import *
import ctypes

import sys
import time
from paddleocr import PaddleOCR
import cv2
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import threading
import pynput


class StandardThread(QThread):
    finished = pyqtSignal()

    def __init__(
        self, window_name, collect_interval=4, execute_time=3.0, unit="龙", number=4
    ):
        super(StandardThread, self).__init__()
        self.window_name = window_name
        self.collect_interval = collect_interval
        self.execute_time = execute_time * 60 * 60
        self.unit = unit
        self.number = number

    def run(self):
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        keyboard = pynput.keyboard.Controller()
        mouse = pynput.mouse.Controller()
        window_loc = getWindowLocation(self.window_name)[1]
        left, top, right, bottom = window_loc
        start_time = time.time()

        try:
            while True:
                # 每打collect_interval场战斗，就收集一次圣水
                for i in range(self.collect_interval):
                    logger.info(
                        f"距离收集圣水还有[{self.collect_interval - i}/{self.collect_interval}]场战斗"
                    )
                    # 缩小视野至最小
                    zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
                    # 进攻
                    attack(
                        keyboard,
                        mouse,
                        window_loc,
                        ocr,
                        TEMPLATES,
                        (self.unit, UNITS[self.unit]),
                        self.number,
                    )
                    if event.is_set():
                        break
                    time.sleep(6)
                    # 检查是否弹出胜利之星奖励
                    logger.info("检查胜利之星")
                    matchThenClick(mouse, TEMPLATES["victory_star"], window_loc)
                if event.is_set():
                    logger.success("已手动停止")
                    break
                # 收集圣水
                collect(keyboard, mouse, window_loc, TEMPLATES)
                # 判断是否到达执行时间，
                if time.time() - start_time >= self.execute_time:
                    logger.success("已到达执行时间")
                    break
                else:
                    elapsed_time = time.time() - start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    logger.info(
                        f"已执行时间：[{int(hours)}h{int(minutes)}min{int(seconds)}s/{int(self.execute_time / 3600)}h]"
                    )
        finally:
            self.finished.emit()


class DropThread(QThread):
    finished = pyqtSignal()

    def __init__(
        self, window_name, collect_interval=10, execute_time=3.0, unit="witch"
    ):
        super(DropThread, self).__init__()
        self.window_name = window_name
        self.collect_interval = collect_interval
        self.execute_time = execute_time * 60 * 60
        self.unit = unit

    def run(self):
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        keyboard = pynput.keyboard.Controller()
        mouse = pynput.mouse.Controller()
        window_loc = getWindowLocation(self.window_name)[1]
        left, top, right, bottom = window_loc
        start_time = time.time()

        try:
            while True:
                # 每打collect_interval场战斗，就收集一次圣水
                for i in range(self.collect_interval):
                    logger.info(
                        f"距离收集圣水还有[{self.collect_interval - i}/{self.collect_interval}]场战斗"
                    )
                    # 缩小视野至最小
                    zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
                    # 进攻
                    attackWithNoArms(
                        keyboard, mouse, window_loc, ocr, TEMPLATES, self.unit
                    )
                    if event.is_set():
                        break
                    time.sleep(4)
                if event.is_set():
                    logger.success("已手动停止")
                    break
                # 收集圣水
                collect(keyboard, mouse, window_loc, TEMPLATES)
                # 判断是否到达执行时间，
                if time.time() - start_time >= self.execute_time:
                    logger.success("已到达执行时间")
                    break
                else:
                    elapsed_time = time.time() - start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    logger.info(
                        f"已执行时间：[{int(hours)}h{int(minutes)}min{int(seconds)}s/{int(self.execute_time / 3600)}h]"
                    )
        finally:
            self.finished.emit()


class MainUi(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.thread: QThread = None
        self.setupUi(self)
        self.setLogics()

    def setLogics(self):
        def standardEvent():
            if self.btn_1.text() == "开始":
                self.btn_2.setEnabled(False)
                event.clear()
                self.btn_1.setText("停止")
                self.standard()
            else:
                event.set()
                self.btn_1.setText("等待结束")
                self.btn_1.setEnabled(False)

        def dropEvent():
            if self.btn_2.text() == "开始":
                self.btn_1.setEnabled(False)
                event.clear()
                self.btn_2.setText("停止")
                self.drop()
            else:
                event.set()
                self.btn_2.setText("等待结束")
                self.btn_2.setEnabled(False)

        self.btn_1.clicked.connect(standardEvent)
        self.btn_2.clicked.connect(dropEvent)
        self.setWindowIcon(QIcon("avatar.ico"))

    def standard(self):
        window_name = self.window_name_label.text()
        collect_interval = int(self.collect_interval.text())
        execute_time = float(self.execute_time_1.text())
        unit = self.unit_1.currentText()
        number = int(self.number.text())

        self.thread = StandardThread(
            window_name, collect_interval, execute_time, unit, number
        )
        self.thread.finished.connect(self.finished)
        self.thread.start()

    def drop(self):
        window_name = self.window_name_label.text()
        execute_time = float(self.execute_time_2.text())
        unit = self.unit_2.currentText()

        self.thread = DropThread(window_name, 10, execute_time, unit)
        self.thread.finished.connect(self.finished)
        self.thread.start()

    def finished(self):
        self.btn_1.setText("开始")
        self.btn_2.setText("开始")
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)
        self.thread.quit()


if __name__ == "__main__":
    if getScaling() != 1.0:
        print("请将系统缩放设置为100%")
        exit(0)
    event = threading.Event()
    app = QApplication(sys.argv)
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("cocscript")
    except Exception as e:
        logger.error(e)
    with open("style.qss", "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
