"""
作者：Yuanl
日期：2025年7月25日
"""

import os.path
import pyautogui
from paddleocr import PaddleOCR
from tqdm import tqdm
import time
import pickle
from PyQt5.QtCore import QThread
import math
import threading

from day_world.key_words import *
from common.utils import *


def buildArmy(
    ms: pynput.mouse.Controller,
    window_loc: tuple[int, int, int, int],
    templates: dict[str, np.ndarray],
    number: int = 16
):
    left, top, right, bottom = window_loc
    if not matchTemplateThenClick(ms, templates["build_army"], window_loc):
        logThenExit("未找到建造按钮", "no_build_army.png")
    time.sleep(1)
    # 删除所有部队
    if not getTemplatePos(window_loc, templates["delete"]):
        logThenExit("未找到删除部队按钮", "no_delete_army.png")
    moveThenClick(ms, (left + 1543, top + 254))
    if not waitUntilMatchThenClick(ms, templates["delete_confirm"], window_loc, timeout=3):
        logThenExit("未找到删除确认按钮", "no_delete_confirm.png")
    time.sleep(1)
    # 建造部队
    moveThenClick(ms, (left + 1110, top + 354))
    time.sleep(1)
    build_dragon_pos = getTemplatePos(window_loc, templates["build_dragon"])
    if not build_dragon_pos:
        logThenExit("未找到建造龙按钮", "no_build_dragon.png")
    ms.position = build_dragon_pos
    for _ in range(number):
        ms.click(pynput.mouse.Button.left)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    moveThenClick(ms, (left + 1110, top + 354))
    time.sleep(1)
    # 删除所有法术
    if not getTemplatePos(window_loc, templates["delete"]):
        logThenExit("未找到删除法术按钮", "no_delete_spell.png")
    moveThenClick(ms, (left + 1222, top + 477))
    if not waitUntilMatchThenClick(ms, templates["delete_confirm"], window_loc, timeout=3):
        logThenExit("未找到删除确认按钮", "no_delete_confirm.png")
    time.sleep(1)
    # 建造法术
    moveThenClick(ms, (left + 963, top + 572))
    time.sleep(1)
    # build_rage_pos = getTemplatePos(window_loc, templates["build_rage"])
    # if not build_rage_pos:
    #     logThenExit("未找到建造狂暴法术按钮", "no_build_rage.png")
    # ms.position = build_rage_pos
    # for _ in range(3):
    #     ms.click(pynput.mouse.Button.left)
    #     time.sleep(0.1)
    # time.sleep(1)

    # build_lightning_pos = getTemplatePos(window_loc, templates["build_lightning"])
    # if not build_lightning_pos:
    #     logThenExit("未找到建造闪电法术按钮", "no_build_lightning.png")
    # ms.position = build_lightning_pos
    # for _ in range(5):
    #     ms.click(pynput.mouse.Button.left)
    #     time.sleep(0.1)
    # time.sleep(1)

    build_bat_pos = getTemplatePos(window_loc, templates["build_bat"])
    if not build_bat_pos:
        logThenExit("未找到建造蝙蝠法术按钮", "no_build_bat.png")
    ms.position = build_bat_pos
    for _ in range(11):
        ms.click(pynput.mouse.Button.left)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    moveThenClick(ms, (left + 1110, top + 354))
    time.sleep(1)
    # 删除所有攻城武器
    if not getTemplatePos(window_loc, templates["delete"]):
        logThenExit("未找到删除攻城武器按钮", "no_delete_siege_weapons.png")
    moveThenClick(ms, (left + 1543, top + 477))
    if not waitUntilMatchThenClick(ms, templates["delete_confirm"], window_loc, timeout=3):
        logThenExit("未找到删除确认按钮", "no_delete_confirm.png")
    time.sleep(1)
    # 建造攻城武器
    moveThenClick(ms, (left + 1427, top + 574))
    time.sleep(1)
    build_airship_pos = getTemplatePos(window_loc, templates["build_airship"])
    if not build_airship_pos:
        logThenExit("未找到建造攻城气球按钮", "no_build_airship.png")
    ms.position = build_airship_pos
    for _ in range(3):
        ms.click(pynput.mouse.Button.left)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    moveThenClick(ms, (left + 1110, top + 354))
    time.sleep(1)
    # 结束建造
    if not waitUntilMatchThenClick(ms, templates["build_end"], window_loc, timeout=3):
        logThenExit("未找到结束建造按钮", "no_build_end.png")
    time.sleep(1)


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


def detectOpponentResources(
    ocr: PaddleOCR,
    window_loc: tuple[int, int, int, int],
    gold: int = 0,
    elixir: int = 0,
    oil: int = 0
):
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    time.sleep(1)
    scr = ImageGrab.grab(window_loc)
    scr = np.array(scr)[round(h * 1 / 7):round(h * 1 / 3), :round(1 / 6 * w), :]
    # 识别资源
    idx = -math.inf
    result = ocr.predict(scr)
    for line in result[0]['rec_texts']:
        # print(line)
        idx += 1
        if idx == 1:
            op_gold = int(line.replace(' ', '').replace('.', '').replace(',', ''))
            if gold > op_gold:
                logger.info(f"对手金币不足：{formatInt(op_gold)} < {formatInt(gold)}")
                return False
        elif idx == 2:
            op_elixir = int(line.replace(' ', '').replace('.', '').replace(',', ''))
            if elixir > op_elixir:
                logger.info(f"对手圣水不足：{formatInt(op_elixir)} < {formatInt(elixir)}")
                return False
        elif idx == 3:
            op_oil = int(line.replace(' ', '').replace('.', '').replace(',', ''))
            if oil > op_oil:
                logger.info(f"对手黑油不足：{formatInt(op_oil)} < {formatInt(oil)}")
                return False
        elif idx == -math.inf:
            pass
        else:
            return False
        if '可获得的战利品' in line:
            idx = 0
    return True


def attack(
    kb: pynput.keyboard.Controller,
    ms: pynput.mouse.Controller,
    window_loc: tuple[int, int, int, int],
    ocr: PaddleOCR,
    templates: dict[str, np.ndarray],
    number: int,
    resource: tuple[int, int, int] = (0, 0, 0),
    event: threading.Event = None
):
    gold, elixir, oil = resource
    left, top, right, bottom = window_loc
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    h, w = bottom - top, right - left
    while True:
        find = False
        if not matchOcrThenClick(ms, "进攻", ocr, window_loc, (2 / 3, 1.0, 0.0, 1 / 3)):
            logThenExit("未找到进攻按钮", "no_attack.png")
        if not waitUntilMatchThenClick(ms, templates["search"], window_loc, timeout=2):
            logThenExit("未找到搜索按钮", "no_search.png")
        # 找到对手
        while matchOpponent(ocr, window_loc):
            if event and event.is_set():
                return
            # 检测对手资源
            if detectOpponentResources(ocr, window_loc, gold, elixir, oil):
                logger.info("找到资源足够的对手")
                find = True
                break
            else:
                logger.info('搜索下一个对手')
                if not matchTemplateThenClick(ms, templates["next"], window_loc):
                    logThenExit("未找到搜索下一个对手按钮", "no_next.png")
                ms.position = mid_pos
        # 规定时间内未找到对手
        if not find:  
            logger.warning(f"规定时间内没匹配到，退出重新搜索对手")
            if not matchTemplateThenClick(ms, templates["backhome"], window_loc):
                logThenExit("未找到回营按钮", "no_cancel.png")
            time.sleep(3)
        else:
            logger.info("开始进攻")
            break
    # 开打
    zoomOut(kb, ms, mid_pos)
    shiftScreen(mid_pos, -3)
    queen_pos = (left + 848, top + 744)
    bbrking_pos = (left + 1367, top + 355)
    warden_pos = ((queen_pos[0] + bbrking_pos[0]) // 2, (queen_pos[1] + bbrking_pos[1]) // 2)
    siege_weapon = True
    # 选攻城武器
    if not getTemplatePos(window_loc, templates["airship"]):
        if matchTemplateThenClick(ms, templates["switch"], window_loc):
            if not waitUntilMatchThenClick(ms, templates["switch_airship"], window_loc, timeout=3):
                logger.warning("未找到攻城气球")
                siege_weapon = False
                ms.click(pynput.mouse.Button.left)
        else:
            logger.warning("未找到切换按钮，无法切换到攻城气球")
            siege_weapon = False
    # 放女王
    queen = getTemplatePos(window_loc, templates["archer_queen"])
    if queen:
        moveThenClick(ms, queen)
        time.sleep(0.5)
        moveThenClick(ms, queen_pos)
        # 放技能（穿云箭）
        time.sleep(0.5)
        moveThenClick(ms, queen)
    # 放蛮王
    bbrking = getTemplatePos(window_loc, templates["bbrking"])
    if bbrking:
        moveThenClick(ms, bbrking)
        time.sleep(0.5)
        moveThenClick(ms, bbrking_pos)
    # 放龙
    dragons_pos = generate_gaussian_points(*queen_pos, *bbrking_pos, *warden_pos, num_points=number)
    dragon = getTemplatePos(window_loc, templates["dragon"])
    if dragon:
        moveThenClick(ms, dragon)
        time.sleep(0.5)
        for pos in dragons_pos:
            moveThenClick(ms, pos)
            time.sleep(0.05)
    # 放大守护者
    grand_warden = getTemplatePos(window_loc, templates["grand_warden"])
    if grand_warden:
        moveThenClick(ms, grand_warden)
        time.sleep(0.5)
        moveThenClick(ms, warden_pos)
    # 放亡灵王子
    minion_prince = getTemplatePos(window_loc, templates["minion_prince"])
    if minion_prince:
        moveThenClick(ms, minion_prince)
        time.sleep(0.5)
        moveThenClick(ms, warden_pos)
    # 放飞盾战神
    royal_champion = getTemplatePos(window_loc, templates["royal_champion"])
    if royal_champion:
        moveThenClick(ms, royal_champion)
        time.sleep(0.5)
        moveThenClick(ms, bbrking_pos)
    # 放蝙蝠法术
    bats_pos = generate_gaussian_points(*queen_pos, *bbrking_pos, *warden_pos, num_points=11)
    bat = getTemplatePos(window_loc, templates["bat"])
    if bat:
        moveThenClick(ms, bat)
        time.sleep(0.5)
        for pos in bats_pos:
            moveThenClick(ms, pos)
            time.sleep(0.05)
    # 放飞艇
    if siege_weapon:
        airship = getTemplatePos(window_loc, templates["airship"])
        if airship:
            moveThenClick(ms, airship)
            time.sleep(0.5)
            moveThenClick(ms, warden_pos)
    # 等待几秒
    time.sleep(5)
    # 大守护者放技能（金身）
    if grand_warden:
        moveThenClick(ms, grand_warden)
    time.sleep(0.5)
    # 飞盾战神放技能（火箭长矛）
    if royal_champion:
        moveThenClick(ms, royal_champion)
    time.sleep(0.5)
    # 再等待几秒
    time.sleep(5)
    # 蛮王放技能（足球）
    if bbrking:
        moveThenClick(ms, bbrking)
    # 再等待几秒
    time.sleep(2)
    # 亡灵王子放技能（减速法球）
    if minion_prince:
        moveThenClick(ms, minion_prince)
    time.sleep(0.5)
    ms.position = mid_pos

    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        destruction_time = time.time()
        destruction_rate = 0
        while True:
            # 摧毁率超过5秒没有变化
            if time.time() - destruction_time > 5:
                end = matchTemplateThenClick(ms, templates["giveup"], window_loc)
                if not end:
                    end = matchTemplateThenClick(ms, templates["end_fight"], window_loc)
                if end:
                    if waitUntilMatchThenClick(ms, templates["end_fight_confirm"], window_loc, timeout=3):
                        if waitUntilMatchThenClick(ms, templates["victory_back"], window_loc, timeout=3):
                            pbar.close()
                            logger.info("摧毁率超过5秒没有变化，结束战斗")
                            ms.position = mid_pos
                            return
                        else:
                            logThenExit("未找到回营按钮")
                    else:
                        logThenExit("未找到结束战斗确认按钮", "no_end_fight_confirm.png")
                else:
                    logThenExit("未找到放弃/结束战斗按钮", "no_end_fight.png")
            if matchTemplateThenClick(ms, templates["victory_back"], window_loc):
                pbar.close()
                logger.info("战斗结束，回营")
                ms.position = mid_pos
                return
            # img_dir = 'imgs'
            # if not os.path.exists(img_dir):
            #     os.makedirs(img_dir)
            scr_shot = ImageGrab.grab(window_loc)
            # cv2.imwrite(f'{img_dir}/whole_{time.strftime("%Y%m%d_%H%M%S")}.png', np.array(scr_shot))
            scr_shot = np.array(scr_shot)[round(h * 1 / 2):, round(w * 2 / 3):, :]
            # cv2.imwrite(f'{img_dir}/{time.strftime("%Y%m%d_%H%M%S")}.png', scr_shot)
            result = ocr.predict(scr_shot)
            if result[0] and result[0]['rec_texts']:
                for text in result[0]['rec_texts']:
                    if '%' in text and destruction_rate != text.split('%')[0]:
                        destruction_rate = text.split('%')[0]
                        destruction_time = time.time()
            time.sleep(1)
            pbar.update(round(time.time() - last_time, 1))
            last_time = time.time()
            pbar.set_description(f"进攻中：{(time.time() - start_time):.1f}/{BATTLE_TIME}秒， 当前摧毁率：{destruction_rate}%")


def main(collect_interval=4, execute_time=3.0, unit="龙", number=4):
    """
    :param collect_interval: 收集间隔（场）
    :param execute_time: 执行时间（小时）
    :param unit:
    :param number:
    """
    pass
    # if getScaling() != 1.0:
    #     logger.error("请将显示设置为100%")
    #     exit(0)
    # ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
    # keyboard = pynput.keyboard.Controller()
    # mouse = pynput.mouse.Controller()
    # window_loc = getWindowLocation(title="MuMu模拟器12")[1]
    # left, top, right, bottom = window_loc

    # execute_time *= 60 * 60
    # start_time = time.time()

    # while True:
    #     # 每打collect_interval场战斗，就收集一次圣水
    #     for i in range(collect_interval):
    #         logger.info(f"距离收集圣水还有{collect_interval - i}场战斗")
    #         # 缩小视野至最小
    #         zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))
    #         # 进攻
    #         attack(keyboard, mouse, window_loc, ocr, TEMPLATES, (unit, UNITS[unit]), number)
    #         time.sleep(6)
    #         # 检查是否弹出胜利之星奖励
    #         logger.info("检查胜利之星")
    #         matchTemplateThenClick(mouse, TEMPLATES["victory_star"], window_loc)
    #     # 收集圣水
    #     collect(keyboard, mouse, window_loc, TEMPLATES)
    #     # 判断是否到达执行时间，
    #     if time.time() - start_time >= execute_time:
    #         break
    #     else:
    #         logger.info(f"已用时：{time.time() - start_time:.1f}/{execute_time}秒，继续执行")


if __name__ == "__main__":
    # main()

    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title="MuMu模拟器12")[1]
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
