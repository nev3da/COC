"""
作者：yuanl
日期：2025年7月24日
"""
import ctypes
# 设置进程为DPI敏感
ctypes.windll.shcore.SetProcessDpiAwareness(2)
import json
from threading import Thread
from collections import deque
import threading
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import cv2
from paddleocr import PaddleOCR
import time
import sys

from common.utils import *
from day_world import key_words as day_keywords
from day_world import script as day_script
from night_world import key_words as night_keywords
from night_world import script as night_script
import ui


class ScreenShotThread(Thread):
    def __init__(
        self,
        cap: WindowCapture,
        save_dir: str = "screenshots",
        interval: int = 0
    ):
        super().__init__()
        # self.daemon = True
        self.cap = cap
        self.interval = interval
        self.running = True
        self.save_dir = save_dir
        self.frames = deque()

        os.makedirs(self.save_dir, exist_ok=True)

    def run(self):
        while self.running:
            timestamp = time.time()
            frame = self.cap.grab()
            self.frames.append((timestamp, frame))

            # 删除一分钟之前的图片
            while self.frames and (timestamp - self.frames[0][0]) > 60:
                self.frames.popleft()
            if self.interval > 0:
                time.sleep(self.interval)

    def stop(self):
        self.running = False

    def imagesToVideo(self):
        frames = list(self.frames)
        height, width, _ = frames[0][1].shape
        timestamps = [t for t, _ in frames]
        total_time = timestamps[-1] - timestamps[0]
        fps = len(timestamps) / total_time if total_time > 0 else 1

        output_path = os.path.join(self.save_dir, f'{time.strftime("%Y-%m-%d_%H-%M-%S")}.mp4')
        writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        for _, frame in frames:
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            writer.write(bgr)
        writer.release()


class NightThread(QThread):
    finish_sig = pyqtSignal()

    def __init__(
        self,
        hwnd: int,
        ocr: PaddleOCR,
        cap: WindowCapture,
        event: threading.Event,
        collect_interval_1: int = 4,
        collect_interval_2: int = 0,
        execute_time: float = 3.0,
        unit: str = "女巫",
        number: int = 8,
    ):
        super(NightThread, self).__init__()
        self.hwnd = hwnd
        self.ocr = ocr
        self.cap = cap
        self.e = event
        self.collect_interval_1 = collect_interval_1
        self.collect_interval_2 = collect_interval_2
        self.execute_time = execute_time * 60 * 60
        self.unit = unit
        self.number = number

    def run(self):
        try:
            start_time = time.time()

            battle_num1 = self.collect_interval_1
            battle_num2 = self.collect_interval_2
            battle_total = battle_num1 + battle_num2
            while True:
                # 每打battle_total场战斗，就收集一次圣水
                for i in range(battle_total):
                    if self.e.is_set():
                        break
                    logger.info(f"距离收集圣水还有[{battle_total - i}/{battle_total}]场战斗")
                    # 缩小视野至最小
                    zoomOut(self.hwnd)
                    # 进攻
                    if i < battle_num1:
                        night_script.attack(self.hwnd, self.cap, self.ocr, self.unit, self.number, self.e)
                    else:
                        night_script.attackThenRetreat(self.hwnd, self.cap, self.ocr, self.unit)
                    if self.e.is_set():
                        break
                    time.sleep(4)
                    # 检查是否弹出胜利之星奖励
                    logger.info("检查胜利之星")
                    matchTemplateThenClick(self.hwnd, self.cap, night_keywords.TEMPLATES["victory_star"])
                if self.e.is_set():
                        break
                # 收集圣水
                night_script.collectElixir(self.hwnd, self.cap)
                # 判断是否到达执行时间
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
        hwnd: int,
        ocr: PaddleOCR,
        cap: WindowCapture,
        execute_time: float,
        number: int,
        gold: int,
        elixir: int,
        oil: int,
        event: threading.Event
    ):
        super(DayThread, self).__init__()
        self.hwnd = hwnd
        self.ocr = ocr
        self.cap = cap
        self.execute_time = execute_time * 60
        self.number = number // 20
        self.gold = gold
        self.elixir = elixir
        self.oil = oil
        self.e = event

    def run(self):
        try:
            start_time = time.time()
            battle_num = 1
            # 练兵
            day_script.buildArmy(self.hwnd, self.cap, self.number)
            while True:
                if self.e.is_set():
                    break
                logger.info(f'即将开始第{battle_num}场战斗')
                battle_num += 1
                # 进攻
                day_script.attack(self.hwnd, self.cap, self.ocr, self.number, (self.gold, self.elixir, self.oil), self.e)
                time.sleep(4)
                # 检查是否弹出宝箱（战场寻宝）
                day_script.receiveChest(self.hwnd, self.cap)
                # 检查是否弹出胜利之星奖励
                logger.info("检查胜利之星")
                matchTemplateThenClick(self.hwnd, self.cap, day_keywords.TEMPLATES["victory_star"])
                if self.e.is_set():
                    break
                # 判断是否到达执行时间
                if time.time() - start_time >= self.execute_time:
                    logger.success("已到达执行时间")
                    break
                else:
                    elapsed_time = time.time() - start_time
                    minutes, seconds = divmod(elapsed_time, 60)
                    logger.info(f"已执行时间：[{int(minutes)}min{int(seconds)}s/{int(self.execute_time / 60)}min]")
        except Exception as e:
            print(e)
        finally:
            self.finish_sig.emit()


class MainUi(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.script_thread: QThread = None
        self.screenshot_thread: ScreenShotThread = None
        self.setupUi(self)
        self.loadConfig()
        self.initResources()
        self.setLogics()

    def loadConfig(self):
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
            self.gold.setText(formatInt(config.get("gold", "")))
            self.elixir.setText(formatInt(config.get("elixir", "")))
            self.oil.setText(formatInt(config.get("oil", ""))),
        except FileNotFoundError:
            logger.warning("配置文件不存在，使用默认设置")
        except Exception as e:
            logger.error("加载配置出错:", e)

    def initResources(self):
        print("加载模型中...")
        self.ocr = PaddleOCR(
            use_textline_orientation=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
            text_detection_model_dir=resourcePath("common/paddlemodels/PP-OCRv5_mobile_det_infer"),
            text_recognition_model_dir=resourcePath("common/paddlemodels/PP-OCRv5_mobile_rec_infer"),
        )
        self.hwnd_prtsc = win32gui.FindWindow(None, self.window_name_label.text())
        self.hwnd_operate = win32gui.FindWindowEx(self.hwnd_prtsc, None, None, None)
        self.window_offset = getWindowSize(self.hwnd_prtsc)[1] - getWindowSize(self.hwnd_operate)[1]
        self.cap_script = WindowCapture(self.hwnd_prtsc, self.window_offset)
        self.cap_record = WindowCapture(self.hwnd_prtsc, self.window_offset)

    def setLogics(self):
        def nightScriptEvent():
            if self.night_btn.text() == "开始":
                event.clear()
                self.night_btn.setText("停止")
                self.tabWidget.tabBar().setEnabled(False)
                self.cap_script.initResources()
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
                self.cap_script.initResources()
                self.dayBegin()
                self.screenShotBegin()
            else:
                event.set()
                self.day_btn.setText("等待结束")
                self.day_btn.setEnabled(False)

        self.night_btn.clicked.connect(nightScriptEvent)
        self.day_btn.clicked.connect(dayScriptEvent)
        self.setWindowIcon(QIcon(resourcePath("avatar.ico")))

    def nightBegin(self):
        self.script_thread = NightThread(
            self.hwnd_operate,
            self.ocr,
            self.cap_script,
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
            self.hwnd_operate,
            self.ocr,
            self.cap_script,
            float(self.day_execute_time.text()),
            int(self.day_number.text()),
            int(self.gold.text().replace(' ', '')),
            int(self.elixir.text().replace(' ', '')),
            int(self.oil.text().replace(' ', '')),
            event
        )
        self.script_thread.finish_sig.connect(self.finished)
        self.script_thread.start()

    def screenShotBegin(self):
        # 启动截图线程
        self.cap_record.initResources()
        self.screenshot_thread = ScreenShotThread(self.cap_record, interval=0.05)
        self.screenshot_thread.start()

    def finished(self):
        self.cap_script.release()
        self.cap_record.release()
        # 停止脚本线程
        if self.script_thread:
            self.script_thread.quit()
            self.script_thread.wait()
            logger.success("线程已安全退出")

        # 停止截图线程
        if self.screenshot_thread:
            self.screenshot_thread.stop()
            self.screenshot_thread.join()
            logger.success("正在保存视频....")

            self.screenshot_thread.imagesToVideo()
            logger.success("已保存视频")

        self.night_btn.setText("开始")
        self.night_btn.setEnabled(True)
        self.day_btn.setText("开始")
        self.day_btn.setEnabled(True)
        self.tabWidget.tabBar().setEnabled(True)
        self.script_thread = None
        self.screenshot_thread = None
        self.saveConfig()

    def saveConfig(self):
        config = {
            "window_name_label": self.window_name_label.text(),
            "night_execute_time": self.night_execute_time.value(),
            "collect_interval_1": self.collect_interval_1.text(),
            "collect_interval_2": self.collect_interval_2.text(),
            "unit": self.unit.currentIndex(),  # 或 self.unit.currentText()
            "night_number": self.night_number.value(),
            "day_execute_time": self.day_execute_time.value(),
            "day_number": self.day_number.text(),
            "gold": self.gold.text().replace(' ', ''),
            "elixir": self.elixir.text().replace(' ', ''),
            "oil": self.oil.text().replace(' ', ''),
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    event = threading.Event()
    app = QApplication(sys.argv)
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("cocscript")
    except Exception as e:
        logger.error(e)
    with open(resourcePath("style.qss"), "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())
    window = MainUi()
    window.show()
    sys.exit(app.exec_())
