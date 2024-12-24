"""
作者：yuanl
日期：2024年10月21日
"""
import ui
from script import attack, collect
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
    finished = pyqtSignal()
    def __init__(self, window_name, collect_interval=4, execute_time=3.0, unit='龙', number=4):
        super(ScriptThread, self).__init__()
        self.window_name = window_name
        self.collect_interval = collect_interval
        self.execute_time = execute_time * 60 * 60
        self.unit = unit
        self.number = number

    def run(self):
        ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        keyboard = pynput.keyboard.Controller()
        mouse = pynput.mouse.Controller()
        window_loc = getWindowLocation(self.window_name)[1]
        units = {
            '龙': 'dragon',
            '女巫': 'witch',
        }
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
        left, top, right, bottom = window_loc
        start_time = time.time()

        while True:
            for _ in range(self.collect_interval):  # 每打collect_interval场战斗，就收集一次圣水
                zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))  # 缩小视野至最小
                attack(keyboard, mouse, window_loc, ocr,
                       templates, (self.unit, units[self.unit]), self.number)  # 进攻
                if event.is_set():
                    break
                time.sleep(6)
                logger.info('检查胜利之星')
                matchThenClick(mouse, templates['victory_star'], window_loc)  # 检查是否弹出胜利之星奖励
            if event.is_set():
                logger.success('已手动停止')
                self.finished.emit()
                break
            collect(keyboard, mouse, window_loc, templates)  # 收集圣水
            if time.time() - start_time >= self.execute_time:  # 判断是否到达执行时间，
                logger.success('已到达执行时间')
                break


class MainUi(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.thread = None
        self.setupUi(self)
        self.setLogics()

    def setLogics(self):
        def scriptEvent():
            if self.btn.text() == '开始':
                event.clear()
                self.btn.setText('停止')
                self.begin()
            else:
                event.set()
                self.btn.setText('等待结束')
                self.btn.setEnabled(False)

        self.btn.clicked.connect(scriptEvent)
        self.setWindowIcon(QIcon("avatar.ico"))

    def begin(self):
        window_name = self.window_name_label.text()
        collect_interval = int(self.collect_interval.text())
        execute_time = float(self.execute_time.text())
        unit = self.unit.currentText()
        number = int(self.number.text())

        self.thread = ScriptThread(window_name, collect_interval, execute_time, unit, number)
        self.thread.finished.connect(self.finished)
        self.thread.start()
    
    def finished(self):
        self.btn.setText('开始')
        self.btn.setEnabled(True)


if __name__ == '__main__':
    if getScaling() != 1.0:
        print('请将系统缩放设置为100%')
        exit(0)
    event = threading.Event()
    app = QApplication(sys.argv)
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("cocscript")
    except Exception as e:
        logger.error(e)
    with open('style.qss', "r", encoding='utf-8') as file:
        app.setStyleSheet(file.read())
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
