"""
作者：yuanl
日期：2024年10月21日
"""

import ui
from script import attack, collect, attackThenRetreat
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


class ScriptThread(QThread):
    finish_sig = pyqtSignal()

    def __init__(
        self,
        window_name,
        collect_interval_1=4,
        collect_interval_2=0,
        execute_time=3.0,
        unit="龙",
        number=4,
    ):
        super(ScriptThread, self).__init__()
        self.window_name = window_name
        self.collect_interval_1 = collect_interval_1
        self.collect_interval_2 = collect_interval_2
        self.execute_time = execute_time * 60 * 60
        self.unit = unit
        self.number = number

    def run(self):
        try:
            ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
            keyboard = pynput.keyboard.Controller()
            mouse = pynput.mouse.Controller()
            window_loc = getWindowLocation(self.window_name)[1]
            left, top, right, bottom = window_loc
            start_time = time.time()

            battle_num1 = self.collect_interval_1
            battle_num2 = self.collect_interval_2
            battle_total = battle_num1 + battle_num2
            while True:
                # 每打battle_total场战斗，就收集一次圣水
                for i in range(battle_total):
                    logger.info(
                        f"距离收集圣水还有[{battle_total - i}/{battle_total}]场战斗"
                    )
                    # 缩小视野至最小
                    zoomOut(keyboard, mouse,
                            ((left + right) // 2, (top + bottom) // 2))
                    # 进攻
                    attack(keyboard, mouse, window_loc, ocr, TEMPLATES, (self.unit, UNITS[self.unit]), self.number) if i < battle_num1 else attackThenRetreat(
                        keyboard, mouse, window_loc, ocr, TEMPLATES, self.unit)
                    if event.is_set():
                        break
                    time.sleep(4) if i < battle_num1 else time.sleep(2)
                    # 检查是否弹出胜利之星奖励
                    logger.info("检查胜利之星")
                    matchThenClick(
                        mouse, TEMPLATES["victory_star"], window_loc)
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
        except Exception as e:
            pass
        finally:
            self.finish_sig.emit()


class MainUi(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.thread: QThread
        self.setupUi(self)
        self.setLogics()

    def setLogics(self):
        def scriptEvent():
            if self.btn.text() == "开始":
                event.clear()
                self.btn.setText("停止")
                self.begin()
            else:
                event.set()
                self.btn.setText("等待结束")
                self.btn.setEnabled(False)

        self.btn.clicked.connect(scriptEvent)
        self.setWindowIcon(QIcon("avatar.ico"))

    def begin(self):
        window_name = self.window_name_label.text()
        collect_interval_1 = int(self.collect_interval_1.text())
        collect_interval_2 = int(self.collect_interval_2.text())
        execute_time = float(self.execute_time.text())
        unit = self.unit.currentText()
        number = int(self.number.text())

        self.thread = ScriptThread(
            window_name,
            collect_interval_1,
            collect_interval_2,
            execute_time,
            unit,
            number,
        )
        self.thread.finish_sig.connect(self.finished)
        self.thread.start()

    def finished(self):
        self.btn.setText("开始")
        self.btn.setEnabled(True)
        self.thread.quit()
        self.thread.wait()
        logger.success("线程已安全退出")


if __name__ == "__main__":
    if getScaling() != 1.0:
        print("请将系统缩放设置为100%")
        exit(0)
    event = threading.Event()
    app = QApplication(sys.argv)
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "cocscript")
    except Exception as e:
        logger.error(e)
    with open("style.qss", "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
