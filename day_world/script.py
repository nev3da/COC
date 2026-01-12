"""
作者：Yuanl
日期：2025年7月25日
"""
from paddleocr import PaddleOCR
from tqdm import tqdm
import time
import threading

from day_world.key_words import *
from common.utils import *


def buildArmy(
    hwnd: int,
    cap: WindowCapture,
    number: int = 16
):
    if not matchTemplateThenClick(hwnd, cap, TEMPLATES["build_army"]):
        logThenExit("未找到建造按钮", "no_build_army.png")
    time.sleep(1)
    # 删除所有部队
    if not getTemplatePos(hwnd, cap, TEMPLATES["delete"]):
        logThenExit("未找到删除部队按钮", "no_delete_army.png")
    click(hwnd, (1543, 208))
    waitUntilMatchThenClick(hwnd, cap, TEMPLATES["delete_confirm"], timeout=3)
    time.sleep(1)
    # 建造部队
    click(hwnd, (1000, 300))
    time.sleep(1)
    build_dragon_pos = getTemplatePos(hwnd, cap, TEMPLATES["build_dragon"])
    if not build_dragon_pos:
        logThenExit("未找到建造龙按钮", "no_build_dragon.png")
    for _ in range(number):
        click(hwnd, build_dragon_pos)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    click(hwnd, (1000, 300))
    time.sleep(1)
    # 删除所有法术
    if not getTemplatePos(hwnd, cap, TEMPLATES["delete"]):
        logThenExit("未找到删除法术按钮", "no_delete_spell.png")
    click(hwnd, (1222, 430))
    waitUntilMatchThenClick(hwnd, cap, TEMPLATES["delete_confirm"], timeout=3)
    time.sleep(1)
    # 建造法术
    click(hwnd, (1000, 520))
    time.sleep(1)
    build_bat_pos = getTemplatePos(hwnd, cap, TEMPLATES["build_bat"])
    if not build_bat_pos:
        logThenExit("未找到建造蝙蝠法术按钮", "no_build_bat.png")
    for _ in range(11):
        click(hwnd, build_bat_pos)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    click(hwnd, (1000, 300))
    time.sleep(1)
    # 删除所有攻城武器
    if not getTemplatePos(hwnd, cap, TEMPLATES["delete"]):
        logThenExit("未找到删除攻城武器按钮", "no_delete_siege_weapons.png")
    click(hwnd, (1543, 430))
    waitUntilMatchThenClick(hwnd, cap, TEMPLATES["delete_confirm"], timeout=3)
    time.sleep(1)
    # 建造攻城武器
    click(hwnd, (1427, 520))
    time.sleep(1)
    build_airship_pos = getTemplatePos(hwnd, cap, TEMPLATES["build_airship"])
    if not build_airship_pos:
        logThenExit("未找到建造攻城气球按钮", "no_build_airship.png")
    for _ in range(3):
        click(hwnd, build_airship_pos)
        time.sleep(0.1)
    time.sleep(1)
    # 返回
    click(hwnd, (1000, 300))
    time.sleep(1)
    # 结束建造
    if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["build_end"], timeout=3):
        logThenExit("未找到结束建造按钮", "no_build_end.png")
    time.sleep(1)


def matchOpponent(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    time_limit: float = 20.0
):
    time.sleep(1)
    start_time = time.time()
    while True:
        if time.time() - start_time >= time_limit:
            return False
        logger.info(f"正在匹配对手：[{time.time() - start_time:.2f}/{time_limit:.2f}]")
        if getTemplatePos(hwnd, cap, TEMPLATES['next'], crop=(1 / 2, 1.0, 2 / 3, 1.0)):
            return True
        time.sleep(1)


def detectOpponentResources(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    gold: int = 0,
    elixir: int = 0,
    oil: int = 0
):
    time.sleep(1)
    w, h = getWindowSize(hwnd)
    scr = cap.grab()[round(h * 1 / 7) - 10:round(h * 1 / 3) - 30, :round(1 / 7 * w), :]
    # cv2.imwrite("debug_opponent_resources.png", cv2.cvtColor(scr, cv2.COLOR_RGB2BGR))
    # 识别资源
    idx = 0
    result = ocr.predict(scr)
    try:
        op_gold, op_elixir, op_oil = 0, 0, 0
        for line in result[0]['rec_texts']:
            idx += 1
            if idx == 1:
                op_gold = int(''.join(c for c in line if c.isdigit()))
                if gold > op_gold:
                    logger.info(f"对手金币不足：{formatInt(op_gold)} < {formatInt(gold)}")
                    return False
            elif idx == 2:
                op_elixir = int(''.join(c for c in line if c.isdigit()))
                if elixir > op_elixir:
                    logger.info(f"对手圣水不足：{formatInt(op_elixir)} < {formatInt(elixir)}")
                    return False
            elif idx == 3:
                op_oil = int(''.join(c for c in line if c.isdigit()))
                if oil > op_oil:
                    logger.info(f"对手黑油不足：{formatInt(op_oil)} < {formatInt(oil)}")
                    return False
            else:
                return False
    except Exception as e:
        logger.error(f"资源检测失败：{e}")
        return False
    logger.info(f"对手资源：金币 {formatInt(op_gold)}, 圣水 {formatInt(op_elixir)}, 黑油 {formatInt(op_oil)}")
    return True


def checkCastleCake(
    hwnd: int,
    cap: WindowCapture,
):
    if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["castle_cake"], timeout=1, crop=(0.5, 1, 2 / 3, 1)):
        if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["castle_confirm"], timeout=2):
            time.sleep(1)
            # 可能没有设置援军
            if matchTemplateThenClick(hwnd, cap, TEMPLATES["castle_cancel"]):
                logger.warning("未设置援军")
            else:
                logger.info("设置援军成功")
        else:
            logThenExit("未找到援军确认按钮", "no_castle_confirm.png")


def attack(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    number: int,
    resource: tuple[int, int, int] = (0, 0, 0),
    event: threading.Event = None
):
    gold, elixir, oil = resource
    w, h = getWindowSize(hwnd)
    mid_pos = (w // 2, h // 2)
    while True:
        find = False
        if not matchOcrThenClick(hwnd, cap, ocr, "进攻", (2 / 3, 1, 0, 1 / 3)):
            logThenExit("未找到进攻按钮", "no_attack.png")
        if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["search"], timeout=2, crop=(0, 1, 0, 1 / 3)):
            logThenExit("未找到搜索按钮", "no_search.png")
        # 如果吃了部落城堡免费增援的蛋糕
        checkCastleCake(hwnd, cap)
        if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["attack"], timeout=2, crop=(2 / 3, 1, 2 / 3, 1)):
            logThenExit("未找到进攻按钮", "no_attack.png")
        # 找到对手
        while matchOpponent(hwnd, cap, ocr):
            if event and event.is_set():
                return
            # 检测对手资源
            if detectOpponentResources(hwnd, cap, ocr, gold, elixir, oil):
                logger.info("找到资源足够的对手")
                find = True
                break
            else:
                logger.info('搜索下一个对手')
                if not matchTemplateThenClick(hwnd, cap, TEMPLATES["next"]):
                    logThenExit("未找到搜索下一个对手按钮", "no_next.png")
        # 规定时间内未找到对手
        if not find:
            logger.warning(f"规定时间内没匹配到，退出重新搜索对手")
            if not matchTemplateThenClick(hwnd, cap, TEMPLATES["backhome"]):
                logThenExit("未找到回营按钮", "no_cancel.png")
            time.sleep(3)
        else:
            logger.info("开始进攻")
            break
    # 开打
    zoomOut(hwnd)
    shiftScreen(hwnd, mid_pos, -3)
    queen_pos = (870, 695)
    bbrking_pos = (1400, 300)
    warden_pos = ((queen_pos[0] + bbrking_pos[0]) // 2, (queen_pos[1] + bbrking_pos[1]) // 2)
    siege_weapon = True
    # 选攻城武器
    if not getTemplatePos(hwnd, cap, TEMPLATES["airship"]):
        if matchTemplateThenClick(hwnd, cap, TEMPLATES["switch"]):
            if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["switch_airship"], timeout=3):
                logger.warning("未找到攻城气球")
                siege_weapon = False
                click(hwnd, mid_pos)
        else:
            logger.warning("未找到切换按钮，无法切换到攻城气球")
            siege_weapon = False
    # 放女王
    queen = getTemplatePos(hwnd, cap, TEMPLATES["archer_queen"])
    if queen:
        click(hwnd, queen)
        time.sleep(0.5)
        click(hwnd, queen_pos)
        # 放技能（穿云箭）
        time.sleep(0.5)
        click(hwnd, queen)
    # 放蛮王
    bbrking = getTemplatePos(hwnd, cap, TEMPLATES["bbrking"])
    if bbrking:
        click(hwnd, bbrking)
        time.sleep(0.5)
        click(hwnd, bbrking_pos)
    # 放龙
    dragons_pos = generateGaussianPoints(*queen_pos, *bbrking_pos, num_points=number)
    dragon = getTemplatePos(hwnd, cap, TEMPLATES["dragon"])
    if dragon:
        click(hwnd, dragon)
        time.sleep(0.5)
        for pos in dragons_pos:
            click(hwnd, pos)
            time.sleep(0.05)
    # 放大守护者
    grand_warden = getTemplatePos(hwnd, cap, TEMPLATES["grand_warden"])
    if grand_warden:
        click(hwnd, grand_warden)
        time.sleep(0.5)
        click(hwnd, warden_pos)
    # 放亡灵王子
    minion_prince = getTemplatePos(hwnd, cap, TEMPLATES["minion_prince"])
    if minion_prince:
        click(hwnd, minion_prince)
        time.sleep(0.5)
        click(hwnd, warden_pos)
    # 放飞盾战神
    royal_champion = getTemplatePos(hwnd, cap, TEMPLATES["royal_champion"])
    if royal_champion:
        click(hwnd, royal_champion)
        time.sleep(0.5)
        click(hwnd, bbrking_pos)
    # 放蝙蝠法术（14 = 11 + 3部落城堡）
    bats_pos = generateGaussianPoints(*queen_pos, *bbrking_pos, num_points=14)
    bat = getTemplatePos(hwnd, cap, TEMPLATES["bat"])
    if bat:
        click(hwnd, bat)
        time.sleep(0.5)
        for pos in bats_pos:
            click(hwnd, pos)
            time.sleep(0.05)
    # 放飞艇
    if siege_weapon:
        airship = getTemplatePos(hwnd, cap, TEMPLATES["airship"])
        if airship:
            click(hwnd, airship)
            time.sleep(0.5)
            click(hwnd, warden_pos)
    # 等待几秒
    time.sleep(5)
    # 大守护者放技能（金身）
    if grand_warden:
        click(hwnd, grand_warden)
    time.sleep(0.5)
    # 飞盾战神放技能（火箭长矛）
    if royal_champion:
        click(hwnd, royal_champion)
    time.sleep(0.5)
    # 再等待几秒
    time.sleep(3)
    # 蛮王放技能（足球）
    if bbrking:
        click(hwnd, bbrking)
    # 再等待几秒
    time.sleep(2)
    # 亡灵王子放技能（减速法球）
    if minion_prince:
        click(hwnd, minion_prince)
    time.sleep(0.5)

    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        destruction_time = time.time()
        destruction_rate = 0
        while True:
            if event and event.is_set():
                pbar.close()
                return
            # 摧毁率超过5秒没有变化
            limit_time = 5
            try:
                rate = int(destruction_rate)
                if rate > 97:
                    limit_time = 20
            except ValueError:
                pass
            if time.time() - destruction_time > limit_time:
                end = matchTemplateThenClick(hwnd, cap, TEMPLATES["giveup"])
                if not end:
                    end = matchTemplateThenClick(hwnd, cap, TEMPLATES["end_fight"])
                if end:
                    if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["end_fight_confirm"], timeout=3):
                        # 考虑战场寻宝活动
                        if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["victory_back"], timeout=3) or waitUntilMatchThenClick(hwnd, cap, TEMPLATES["receive_chest"], timeout=3):
                            pbar.close()
                            logger.info("摧毁率超过5秒没有变化，结束战斗")
                            return
                        else:
                            logThenExit("未找到回营按钮")
                    else:
                        logThenExit("未找到结束战斗确认按钮", "no_end_fight_confirm.png")
                else:
                    logThenExit("未找到放弃/结束战斗按钮", "no_end_fight.png")
            if matchTemplateThenClick(hwnd, cap, TEMPLATES["victory_back"]) or matchTemplateThenClick(hwnd, cap, TEMPLATES["receive_chest"]):
                pbar.close()
                logger.info("战斗结束，回营")
                return
            scr_shot = cap.grab()[round(h * 1 / 2):, round(w * 2 / 3):, :]
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


def receiveChest(
    hwnd: int,
    cap: WindowCapture,
):
    hammer_pos = getTemplatePos(hwnd, cap, TEMPLATES["chest_hammer"])
    if hammer_pos:
        for _ in range(4):
            click(hwnd, hammer_pos)
            time.sleep(0.5)
        time.sleep(1)
        if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["continue_chest"], timeout=5):
            logger.info("宝箱已领取并关闭")
            time.sleep(5)
        else:
            logThenExit("未找到领取宝箱继续按钮", "no_continue_chest.png")


if __name__ == "__main__":
    pass
