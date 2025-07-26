"""
作者：yuanl
日期：2025年7月24日
"""

import ui
from night_world import script as night_script
from night_world import key_words as night_keywords
from day_world import script as day_script
from day_world import key_words as day_keywords
from common.utils import *

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
from collections import deque
from PIL import ImageGrab
from threading import Thread
import pyautogui
import json

COMMON_DIR = 'common'


class ScreenshotThread(Thread):
    def __init__(self, window_name, save_dir="screenshots", interval=0):
        super().__init__()
        # self.daemon = True
        self.window_name = window_name
        self.interval = interval
        self.running = True
        self.save_dir = save_dir
        self.frames = deque()

        os.makedirs(self.save_dir, exist_ok=True)
        self.window_loc = getWindowLocation(self.window_name)[1]

    def run(self):
        while self.running:
            timestamp = time.time()
            img = ImageGrab.grab(self.window_loc)
            frame = np.array(img)
            x, y = pyautogui.position()
            self.frames.append((timestamp, frame, (x, y)))

            # 删除一分钟之前的图片
            while self.frames and (timestamp - self.frames[0][0]) > 60:
                self.frames.popleft()
            if self.interval > 0:
                time.sleep(self.interval)

    def stop(self):
        self.running = False

    def images_to_video(self):
        frames_with_mouse = list(self.frames)
        height, width, _ = frames_with_mouse[0][1].shape
        timestamps = [t for t, _, _ in frames_with_mouse]
        total_time = timestamps[-1] - timestamps[0]
        fps = len(timestamps) / total_time if total_time > 0 else 1

        output_path = os.path.join(self.save_dir, f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.mp4')
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        for _, frame, (x, y) in frames_with_mouse:
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            x -= self.window_loc[0]
            y -= self.window_loc[1]
            if 0 <= x < width and 0 <= y < height:
                # 在鼠标位置画一个红色圆点
                cv2.circle(bgr, (x, y), radius=12, color=(0, 0, 255), thickness=-1)  # 红点
            out.write(bgr)
        out.release()


class NightThread(QThread):
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
        super(NightThread, self).__init__()
        self.window_name = window_name
        self.collect_interval_1 = collect_interval_1
        self.collect_interval_2 = collect_interval_2
        self.execute_time = execute_time * 60 * 60
        self.unit = unit
        self.number = number

    def run(self):
        try:
            ocr = PaddleOCR(use_textline_orientation=False,
                            use_doc_orientation_classify=False,
                            use_doc_unwarping=False,
                            text_detection_model_name="PP-OCRv5_mobile_det",
                            text_recognition_model_name="PP-OCRv5_mobile_rec",
                            text_detection_model_dir=resource_path(f"{COMMON_DIR}/paddlemodels/PP-OCRv5_mobile_det_infer"),
                            text_recognition_model_dir=resource_path(f"{COMMON_DIR}/paddlemodels/PP-OCRv5_mobile_rec_infer"),
                            )
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
                    logger.info(f"距离收集圣水还有[{battle_total - i}/{battle_total}]场战斗")
                    # 缩小视野至最小
                    zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
                    # 进攻
                    if i < battle_num1:
                        night_script.attack(keyboard, mouse, window_loc, ocr, night_keywords.TEMPLATES, (self.unit, night_keywords.UNITS[self.unit]), self.number)
                    else:
                        night_script.attackThenRetreat(keyboard, mouse, window_loc, ocr, night_keywords.TEMPLATES, self.unit)
                    if event.is_set():
                        break
                    time.sleep(4)
                    # 检查是否弹出胜利之星奖励
                    logger.info("检查胜利之星")
                    matchTemplateThenClick(mouse, night_keywords.TEMPLATES["victory_star"], window_loc)
                if event.is_set():
                    logger.success("已手动停止")
                    break
                # 收集圣水
                night_script.collect(keyboard, mouse, window_loc, night_keywords.TEMPLATES)
                # 判断是否到达执行时间，
                if time.time() - start_time >= self.execute_time:
                    logger.success("已到达执行时间")
                    break
                else:
                    elapsed_time = time.time() - start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    logger.info(f"已执行时间：[{int(hours)}h{int(minutes)}min{int(seconds)}s/{int(self.execute_time / 3600)}h]")
        except Exception as e:
            print(e)
        finally:
            self.finish_sig.emit()


class DayThread(QThread):
    finish_sig = pyqtSignal()

    def __init__(
        self,
        window_name,
        execute_time=2.0,
        number=280,
    ):
        super(DayThread, self).__init__()
        self.window_name = window_name
        self.execute_time = execute_time * 60 * 60
        self.number = number // 20

    def run(self):
        try:
            ocr = PaddleOCR(use_textline_orientation=False,
                            use_doc_orientation_classify=False,
                            use_doc_unwarping=False,
                            text_detection_model_name="PP-OCRv5_mobile_det",
                            text_recognition_model_name="PP-OCRv5_mobile_rec",
                            text_detection_model_dir=resource_path(f"{COMMON_DIR}/paddlemodels/PP-OCRv5_mobile_det_infer"),
                            text_recognition_model_dir=resource_path(f"{COMMON_DIR}/paddlemodels/PP-OCRv5_mobile_rec_infer"),
                            )
            keyboard = pynput.keyboard.Controller()
            mouse = pynput.mouse.Controller()
            window_loc = getWindowLocation(self.window_name)[1]
            left, top, right, bottom = window_loc
            start_time = time.time()
            battle_num = 1
            # 练兵
            day_script.buildArmy(mouse, window_loc, day_keywords.TEMPLATES, self.number)
            while True:
                logger.info(f'即将开始第{battle_num}场战斗')
                battle_num += 1
                # 缩小视野至最小
                zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
                # 进攻
                day_script.attack(keyboard, mouse, window_loc, ocr, day_keywords.TEMPLATES, self.number)
                if event.is_set():
                    break
                time.sleep(5)
                # 检查是否弹出胜利之星奖励
                logger.info("检查胜利之星")
                matchTemplateThenClick(mouse, day_keywords.TEMPLATES["victory_star"], window_loc)
                if event.is_set():
                    logger.success("已手动停止")
                    break
                # 判断是否到达执行时间，
                if time.time() - start_time >= self.execute_time:
                    logger.success("已到达执行时间")
                    break
                else:
                    elapsed_time = time.time() - start_time
                    hours, remainder = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    logger.info(f"已执行时间：[{int(hours)}h{int(minutes)}min{int(seconds)}s/{int(self.execute_time / 3600)}h]")
        except Exception as e:
            print(e)
        finally:
            self.finish_sig.emit()


class MainUi(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.script_thread: QThread = None
        self.screenshot_thread: ScreenshotThread = None
        self.setupUi(self)
        self.load_config()
        self.setLogics()

    def setLogics(self):
        def nightScriptEvent():
            if self.night_btn.text() == "开始":
                event.clear()
                self.night_btn.setText("停止")
                self.tabWidget.tabBar().setEnabled(False)
                self.nightBegin()
                self.screenShotBegin()
            else:
                event.set()
                self.night_btn.setText("等待结束")
                self.night_btn.setEnabled(False)

        def dayScriptEvent():
            if self.day_btn.text() == "开始":
                event.clear()
                self.day_btn.setText("停止")
                self.tabWidget.tabBar().setEnabled(False)
                self.dayBegin()
                self.screenShotBegin()
            else:
                event.set()
                self.day_btn.setText("等待结束")
                self.day_btn.setEnabled(False)

        self.night_btn.clicked.connect(nightScriptEvent)
        self.day_btn.clicked.connect(dayScriptEvent)
        self.setWindowIcon(QIcon(resource_path("avatar.ico")))

    def load_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            self.window_name_label.setText(config.get("window_name_label", ""))
            self.night_execute_time.setValue(config.get("night_execute_time", 3))
            self.collect_interval_1.setText(config.get("collect_interval_1", ""))
            self.collect_interval_2.setText(config.get("collect_interval_2", ""))
            self.unit.setCurrentIndex(config.get("unit", 0))
            self.night_number.setValue(config.get("night_number", 8))
            self.day_execute_time.setValue(config.get("day_execute_time", 2))
            self.day_number.setText(config.get("day_number", ""))
        except FileNotFoundError:
            logger.warning("配置文件不存在，使用默认设置")
        except Exception as e:
            logger.error("加载配置出错:", e)

    def nightBegin(self):
        self.script_thread = NightThread(
            self.window_name_label.text(),
            int(self.collect_interval_1.text()),
            int(self.collect_interval_2.text()),
            float(self.night_execute_time.text()),
            self.unit.currentText(),
            int(self.night_number.text()),
        )
        self.script_thread.finish_sig.connect(self.finished)
        self.script_thread.start()

    def dayBegin(self):
        self.script_thread = DayThread(
            self.window_name_label.text(),
            float(self.day_execute_time.text()),
            int(self.day_number.text()),
        )
        self.script_thread.finish_sig.connect(self.finished)
        self.script_thread.start()

    def screenShotBegin(self):
        # 启动截图线程
        self.screenshot_thread = ScreenshotThread(self.window_name_label.text())
        self.screenshot_thread.start()

    def finished(self):
        self.script_thread.quit()
        self.script_thread.wait()
        logger.success("线程已安全退出")

        # 停止截图线程
        if self.screenshot_thread:
            self.screenshot_thread.stop()
            self.screenshot_thread.join()
            logger.success("正在保存视频....")

            self.screenshot_thread.images_to_video()
            logger.success("已保存视频")

        self.night_btn.setText("开始")
        self.night_btn.setEnabled(True)
        self.day_btn.setText("开始")
        self.day_btn.setEnabled(True)
        self.tabWidget.tabBar().setEnabled(True)
        self.script_thread = None
        self.screenshot_thread = None
        self.save_config()

    def save_config(self):
        config = {
            "window_name_label": self.window_name_label.text(),
            "night_execute_time": self.night_execute_time.value(),
            "collect_interval_1": self.collect_interval_1.text(),
            "collect_interval_2": self.collect_interval_2.text(),
            "unit": self.unit.currentIndex(),  # 或 self.unit.currentText()
            "night_number": self.night_number.value(),
            "day_execute_time": self.day_execute_time.value(),
            "day_number": self.day_number.text()
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


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
    with open(resource_path("style.qss"), "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
