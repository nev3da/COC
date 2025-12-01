"""
作者：yuanl
日期：2024年12月22日
"""

import os.path
import pyautogui
from paddleocr import PaddleOCR
from tqdm import tqdm
import time
import pickle
from PyQt5.QtCore import QThread

from night_world.key_words import *
from common.utils import *


def collect(
    kb: pynput.keyboard.Controller,
    ms: pynput.mouse.Controller,
    window_loc: tuple[int, int, int, int],
    templates: dict[str, np.ndarray]
):
    left, top, right, bottom = window_loc
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    zoomOut(kb, ms, mid_pos)
    shiftScreen(mid_pos, 4)
    time.sleep(1)
    logger.info("识别圣水车")
    while True:
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        # 识别白色背景圣水
        wheelbarrow_pos = getTemplatePos(window_loc, templates["elixir1"], scr_shot, threshold=0.8)
        if not wheelbarrow_pos:
            # 识别红色背景圣水
            wheelbarrow_pos = getTemplatePos(window_loc, templates["elixir2"], scr_shot, threshold=0.8)
            if not wheelbarrow_pos:
                find_wheelbarrow = False
                # 识别斧子
                for filename in os.listdir(templates["axe"]):
                    t = None
                    with open(os.path.join(templates["axe"], filename), "rb") as f:
                        t = pickle.load(f)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                    wheelbarrow_pos = getTemplatePos(window_loc, t, scr_shot, threshold=0.75)
                    if wheelbarrow_pos:
                        find_wheelbarrow = True
                        break
                if not find_wheelbarrow:
                    logger.warning("未找到圣水车")
                    return
        moveThenClick(ms, wheelbarrow_pos)
        time.sleep(1)
        logger.info("识别收集和关闭按钮")
        close_pos = getTemplatePos(window_loc, templates["close"])
        if not close_pos:
            logger.info("识别到了圣水瓶，重新识别圣水车")
        else:
            break
    collect_pos = getTemplatePos(window_loc, templates["collect"])
    # 如果找到收集按钮就点一下，没找到可能是因为圣水满了，收集按钮变灰，识别不到，所以直接点关闭
    if collect_pos:
        logger.info("收集")
        moveThenClick(ms, collect_pos)
        time.sleep(1)
    logger.info("关闭")
    moveThenClick(ms, close_pos)


# 进攻按钮是半透明的，所以没用模板匹配，而是用OCR识别
def getAttackPos(
    window_loc: tuple[int, int, int, int],
    ocr: PaddleOCR
):
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    scr_shot = ImageGrab.grab(window_loc)
    scr_shot = np.array(scr_shot)
    result = ocr.predict(scr_shot[round(1 / 2 * h):, : round(1 / 2 * w), :])
    if not result[0]:
        return None
    for idx, line in enumerate(result[0]['rec_texts']):
        if "进攻" in line:
            four_corner = result[0]['rec_polys'][idx]
            mid_point = (
                round((four_corner[0][0] + four_corner[1][0]) / 2),
                round((four_corner[0][1] + four_corner[3][1]) / 2),
            )
            attack_pos = (left + mid_point[0], top + mid_point[1] + round(h * 1/2))
            return attack_pos
    return None


def matchOpponent(
    ocr: PaddleOCR,
    window_loc: tuple[int, int, int, int],
    time_limit: float = 20.0
):
    time.sleep(1)
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    start_time = time.time()
    while True:
        if time.time() - start_time >= time_limit:
            return False
        logger.info(f"正在匹配对手：[{time.time() - start_time:.2f}/{time_limit:.2f}]")
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        result = ocr.predict(scr_shot[: round(1 / 3 * h), round(1 / 3 * w): round(2 / 3 * w), :])
        if not result[0]:
            time.sleep(1)
            continue
        for line in result[0]['rec_texts']:
            if "开战倒计时" in line:
                return True


def attack(
    kb: pynput.keyboard.Controller,
    ms: pynput.mouse.Controller,
    window_loc: tuple[int, int, int, int],
    ocr: PaddleOCR,
    templates: dict[str, np.ndarray],
    unit: tuple[str, str],
    number: int,
):
    left, top, right, bottom = window_loc
    h, w = bottom - top, right - left
    search_times = 5
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getAttackPos(window_loc, ocr)
            if not attack_pos:
                logThenExit("未找到进攻按钮", "no_attack.png")
            moveThenClick(ms, attack_pos)
            if not waitUntilMatchThenClick(ms, templates["search"], window_loc, timeout=2):
                logThenExit("未找到搜索按钮", "no_search.png")
            if matchOpponent(ocr, window_loc):  # 找到对手
                find = True
                break
            else:  # 规定时间内未找到对手
                logger.warning(f"规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]")
                if not matchTemplateThenClick(ms, templates["cancel"], window_loc):
                    logThenExit("未找到取消按钮", "no_cancel.png")
            time.sleep(3)
        if find:
            logger.info("开始进攻")
            break
        else:
            logger.warning(f"连续{search_times}次未找到对手，等半分钟再搜")
            time.sleep(30)
    # 开打
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    place_arms_pos = (mid_pos[0], top + 755)
    zoomOut(kb, ms, mid_pos)

    def placeArms(arm_num):
        shiftScreen(mid_pos, -3)
        # 如果第一阶段战争机器挂了，第二阶段直升机图像会自动高亮。因此先点一下
        time.sleep(0.5)
        ms.position = place_arms_pos
        time.sleep(0.2)
        ms.click(pynput.mouse.Button.left)
        time.sleep(0.5)

        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        war_machine_pos = getTemplatePos(window_loc, templates["war_machine"], scr_shot)
        if war_machine_pos:
            logger.info("放战争机器")
            moveThenClick(ms, war_machine_pos)
            time.sleep(0.2)
            moveThenClick(ms, place_arms_pos)
            time.sleep(0.2)
        else:
            helicopter_pos = getTemplatePos(window_loc, templates["helicopter"], scr_shot)
            if helicopter_pos:
                logger.info("放直升机")
                moveThenClick(ms, helicopter_pos)
                time.sleep(0.2)
                moveThenClick(ms, place_arms_pos)
                time.sleep(0.2)

        arm_pos = getTemplatePos(window_loc, templates[unit[1]], scr_shot, pos="top")
        if arm_pos:
            logger.info(f"放{unit[0]}")
            moveThenClick(ms, arm_pos)
            time.sleep(0.2)
            ms.position = place_arms_pos
            time.sleep(0.2)
            for _ in range(arm_num):
                ms.click(pynput.mouse.Button.left)
                time.sleep(0.2)
        if unit[0] == "女巫":
            logger.info("女巫放技能")
            for _ in range(number):
                matchTemplateThenClick(ms, templates["skill"], window_loc, mid=False)
        ms.position = mid_pos  # 鼠标移动到中心

    placeArms(number)
    second_phase = False
    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        while True:  # 等待战斗结束
            if matchTemplateThenClick(ms, templates["backhome"], window_loc):
                pbar.close()
                logger.info(f"第1阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
                logger.info("回营")
                return
            scr_shot = ImageGrab.grab(window_loc)
            scr_shot = np.array(scr_shot)
            result = ocr.predict(scr_shot[: round(1 / 3 * h), round(1 / 3 * w): round(2 / 3 * w), :])
            if result[0]:
                for line in result[0]['rec_texts']:
                    if "开战倒计时" in line:
                        second_phase = True
                        break
            if second_phase:
                break
            matchTemplateThenClick(ms, templates["machine_skill"], window_loc, mid=False)
            time.sleep(2)
            pbar.update(round(time.time() - last_time, 1))
            last_time = time.time()
            pbar.set_description(f"第1阶段进攻中：{(time.time() - start_time):.1f}/{BATTLE_TIME}秒")

    logger.info(f"第1阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
    logger.info("进入二阶段")
    time.sleep(2)
    placeArms(number)
    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        while True:  # 等待战斗结束
            if matchTemplateThenClick(ms, templates["backhome"], window_loc):
                pbar.close()
                logger.info(f"第2阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
                logger.info("回营")
                return
            matchTemplateThenClick(ms, templates["machine_skill"], window_loc, mid=False)
            time.sleep(2)
            pbar.update(round(time.time() - last_time, 1))
            last_time = time.time()
            pbar.set_description(f"第2阶段进攻中：{(time.time() - start_time):.1f}/{BATTLE_TIME}秒")


def attackThenRetreat(
    kb: pynput.keyboard.Controller,
    ms: pynput.mouse.Controller,
    window_loc: tuple[int, int, int, int],
    ocr: PaddleOCR,
    templates: dict[str, np.ndarray],
    unit: str,
):
    left, top, right, bottom = window_loc
    search_times = 5
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getAttackPos(window_loc, ocr)
            if not attack_pos:
                logThenExit("未找到进攻按钮", "no_attack.png")
            moveThenClick(ms, attack_pos)
            if not waitUntilMatchThenClick(ms, templates["search"], window_loc, timeout=2):
                logThenExit("未找到搜索按钮", "no_search.png")
            if matchOpponent(ocr, window_loc):  # 找到对手
                find = True
                break
            else:  # 规定时间内未找到对手
                logger.warning(f"规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]")
                if not matchTemplateThenClick(ms, templates["cancel"], window_loc):
                    logThenExit("未找到取消按钮", "no_cancel.png")
            time.sleep(3)
        if find:
            logger.info("开始进攻")
            break
        else:
            logger.warning(f"连续{search_times}次未找到对手，等半分钟再搜")
            time.sleep(30)
    # 开打
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    place_arms_pos = (mid_pos[0], top + 755)
    zoomOut(kb, ms, mid_pos)

    # 屏幕下移
    shiftScreen(mid_pos, -3)
    # 放一个兵
    arm_pos = getTemplatePos(window_loc, templates[UNITS[unit]], pos="top")
    if arm_pos:
        logger.info(f"放{unit}")
        moveThenClick(ms, arm_pos)
        time.sleep(0.2)
        ms.position = place_arms_pos
        time.sleep(0.2)
        for _ in range(1):
            ms.click(pynput.mouse.Button.left)
            time.sleep(0.2)
    if waitUntilMatchThenClick(ms, templates["giveup"], window_loc, timeout=2):
        if waitUntilMatchThenClick(ms, templates["giveup_confirm"], window_loc, timeout=2):
            if waitUntilMatchThenClick(ms, templates["backhome"], window_loc, timeout=2):
                logger.info("回营")
                return
            else:
                logThenExit("未找到回营按钮", "no_backhome.png")
        else:
            logThenExit("未找到确认按钮", "giveup_confirm.png")
    else:
        logThenExit("未找到放弃按钮", "no_giveup.png")


def main(collect_interval=4, execute_time=3.0, unit="龙", number=4):
    """
    :param collect_interval: 收集间隔（场）
    :param execute_time: 执行时间（小时）
    :param unit:
    :param number:
    """
    if getScaling() != 1.0:
        logger.error("请将显示设置为100%")
        exit(0)
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title="MuMu安卓设备")[1]
    left, top, right, bottom = window_loc

    execute_time *= 60 * 60
    start_time = time.time()

    while True:
        # 每打collect_interval场战斗，就收集一次圣水
        for i in range(collect_interval):
            logger.info(f"距离收集圣水还有{collect_interval - i}场战斗")
            # 缩小视野至最小
            zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
            # 进攻
            attack(keyboard, mouse, window_loc, ocr, TEMPLATES, (unit, UNITS[unit]), number)
            time.sleep(6)
            # 检查是否弹出胜利之星奖励
            logger.info("检查胜利之星")
            matchTemplateThenClick(mouse, TEMPLATES["victory_star"], window_loc)
        # 收集圣水
        collect(keyboard, mouse, window_loc, TEMPLATES)
        # 判断是否到达执行时间，
        if time.time() - start_time >= execute_time:
            break
        else:
            logger.info(f"已用时：{time.time() - start_time:.1f}/{execute_time}秒，继续执行")


if __name__ == "__main__":
    # main()

    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title="MuMu安卓设备")[1]
    left, top, right, bottom = window_loc
    time.sleep(1)
    template = cv2.cvtColor(cv2.imread(resource_path(os.path.join(ARM_DIR, "dragon.png"))), cv2.COLOR_BGR2RGB)
    # src = ImageGrab.grab((left, top, right, bottom))
    # src = np.array(src)
    src = ImageGrab.grab(window_loc)
    src = np.array(src)
    src = cv2.cvtColor(cv2.imread("test.png"), cv2.COLOR_BGR2RGB)
    pos = getTemplatePos((left, top, right, bottom), template, src)
    if pos:
        mouse.position = pos
    else:
        print("未找到")