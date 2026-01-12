"""
作者：yuanl
日期：2024年12月22日
"""
import threading
from paddleocr import PaddleOCR
from tqdm import tqdm
import time
import pickle

from night_world.key_words import *
from common.utils import *


def collectElixir(
    hwnd: int,
    cap: WindowCapture,
):
    w, h = getWindowSize(hwnd)
    mid_pos = (w // 2, h // 2)
    zoomOut(hwnd)
    shiftScreen(hwnd, mid_pos, 3)
    time.sleep(1)
    logger.info("识别圣水车")
    while True:
        scr_shot = cap.grab()
        # 识别白色背景圣水
        wheelbarrow_pos = getTemplatePos(hwnd, cap, TEMPLATES["elixir1"], scr_shot, threshold=0.8)
        if not wheelbarrow_pos:
            # 识别红色背景圣水
            wheelbarrow_pos = getTemplatePos(hwnd, cap, TEMPLATES["elixir2"], scr_shot, threshold=0.8)
            if not wheelbarrow_pos:
                find_wheelbarrow = False
                # 识别斧子
                for filename in os.listdir(TEMPLATES["axe"]):
                    axe = None
                    with open(os.path.join(TEMPLATES["axe"], filename), "rb") as f:
                        axe = cv2.cvtColor(pickle.load(f), cv2.COLOR_BGR2RGB)
                    wheelbarrow_pos = getTemplatePos(hwnd, cap, axe, scr_shot, threshold=0.75)
                    if wheelbarrow_pos:
                        find_wheelbarrow = True
                        break
                if not find_wheelbarrow:
                    logger.warning("未找到圣水车")
                    return
        click(hwnd, wheelbarrow_pos)
        time.sleep(1)
        logger.info("识别收集和关闭按钮")
        close_pos = getTemplatePos(hwnd, cap, TEMPLATES["close"])
        if not close_pos:
            logger.info("识别到了圣水瓶，重新识别圣水车")
        else:
            break
    collect_pos = getTemplatePos(hwnd, cap, TEMPLATES["collect"])
    # 如果找到收集按钮就点一下，没找到可能是因为圣水满了，收集按钮变灰，识别不到，所以直接点关闭
    if collect_pos:
        logger.info("收集")
        click(hwnd, collect_pos)
        time.sleep(1)
    logger.info("关闭")
    click(hwnd, close_pos)


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
        if getOcrPos(hwnd, cap, ocr, "开战倒计时", crop=(0.0, 1 / 3, 1 / 3, 2 / 3)):
            return True
        time.sleep(1)


def attack(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    unit: str,
    number: int,
    event: threading.Event = None,
):
    w, h = getWindowSize(hwnd)
    mid_pos = (w // 2, h // 2)
    search_times = 5
    # 寻找对手
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getOcrPos(hwnd, cap, ocr, "进攻", crop=(0.5, 1.0, 0.0, 0.5))
            if not attack_pos:
                logThenExit("未找到进攻按钮", "no_attack.png")
            click(hwnd, attack_pos)
            if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["search"], timeout=2):
                logThenExit("未找到搜索按钮", "no_search.png")
            if matchOpponent(hwnd, cap, ocr):
                # 找到对手
                find = True
                break
            else:  # 规定时间内未找到对手
                logger.warning(f"规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]")
                if not matchTemplateThenClick(hwnd, cap, TEMPLATES["cancel"]):
                    logThenExit("未找到取消按钮", "no_cancel.png")
            time.sleep(3)
        if find:
            logger.info("开始进攻")
            break
        else:
            logger.warning(f"连续{search_times}次未找到对手，等半分钟再搜")
            time.sleep(30)
    if event and event.is_set():
        return
    # 开打
    place_arms_pos = (mid_pos[0], mid_pos[1] + 230)
    zoomOut(hwnd)

    def placeArms(arm_num):
        shiftScreen(hwnd, mid_pos, -3)
        # 如果第一阶段战争机器挂了，第二阶段直升机图像会自动高亮。因此先点一下
        time.sleep(0.5)
        click(hwnd, place_arms_pos)
        time.sleep(0.5)

        scr_shot = cap.grab()
        war_machine_pos = getTemplatePos(hwnd, cap, TEMPLATES["war_machine"], scr_shot)
        if war_machine_pos:
            logger.info("放战争机器")
            click(hwnd, war_machine_pos)
            time.sleep(0.2)
            click(hwnd, place_arms_pos)
            time.sleep(0.2)
        else:
            helicopter_pos = getTemplatePos(hwnd, cap, TEMPLATES["helicopter"], scr_shot)
            if helicopter_pos:
                logger.info("放直升机")
                click(hwnd, helicopter_pos)
                time.sleep(0.2)
                click(hwnd, place_arms_pos)
                time.sleep(0.2)

        arm_pos = getTemplatePos(hwnd, cap, TEMPLATES[UNITS[unit]], scr_shot, offset="top")
        if arm_pos:
            logger.info(f"放{unit}")
            click(hwnd, arm_pos)
            time.sleep(0.2)
            click(hwnd, place_arms_pos)
            time.sleep(0.2)
            for _ in range(arm_num):
                click(hwnd, place_arms_pos)
                time.sleep(0.2)
        if unit == "女巫":
            logger.info("女巫放技能")
            for _ in range(number):
                matchTemplateThenClick(hwnd, cap, TEMPLATES["skill"], offset='bottom')
                time.sleep(0.5)
    # 第一阶段进攻
    placeArms(number)
    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        # 等待战斗结束
        while True:
            if event and event.is_set():
                return
            if matchTemplateThenClick(hwnd, cap, TEMPLATES["backhome"]):
                pbar.close()
                logger.info(f"第1阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
                logger.info("回营")
                return
            if getOcrPos(hwnd, cap, ocr, "开战倒计时", crop=(0.0, 1 / 3, 1 / 3, 2 / 3)):
                # 进入第二阶段
                break
            matchTemplateThenClick(hwnd, cap, TEMPLATES["machine_skill"], 'bottom')
            time.sleep(2)
            pbar.update(round(time.time() - last_time, 1))
            last_time = time.time()
            pbar.set_description(f"第1阶段进攻中：{(time.time() - start_time):.1f}/{BATTLE_TIME}秒")

    logger.info(f"第1阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
    logger.info("进入二阶段")
    time.sleep(2)
    if event and event.is_set():
        return
    placeArms(number)
    with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
        start_time = time.time()
        last_time = time.time()
        while True:
            if event and event.is_set():
                return
            if matchTemplateThenClick(hwnd, cap, TEMPLATES["backhome"]):
                pbar.close()
                logger.info(f"第2阶段进攻结束，用时：{time.time() - start_time:.1f}秒")
                logger.info("回营")
                return
            matchTemplateThenClick(hwnd, cap, TEMPLATES["machine_skill"], 'bottom')
            time.sleep(2)
            pbar.update(round(time.time() - last_time, 1))
            last_time = time.time()
            pbar.set_description(f"第2阶段进攻中：{(time.time() - start_time):.1f}/{BATTLE_TIME}秒")


def attackThenRetreat(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    unit: str,
):
    w, h = getWindowSize(hwnd)
    mid_pos = (w // 2, h // 2)
    search_times = 5
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getOcrPos(hwnd, cap, ocr, "进攻", crop=(0.5, 1.0, 0.0, 0.5))
            if not attack_pos:
                logThenExit("未找到进攻按钮", "no_attack.png")
            click(hwnd, attack_pos)
            if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["search"], timeout=2):
                logThenExit("未找到搜索按钮", "no_search.png")
            if matchOpponent(hwnd, cap, ocr):
                # 找到对手
                find = True
                break
            else:  # 规定时间内未找到对手
                logger.warning(f"规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]")
                if not matchTemplateThenClick(hwnd, cap, TEMPLATES["cancel"]):
                    logThenExit("未找到取消按钮", "no_cancel.png")
            time.sleep(3)
        if find:
            logger.info("开始进攻")
            break
        else:
            logger.warning(f"连续{search_times}次未找到对手，等半分钟再搜")
            time.sleep(30)
    # 开打
    place_arms_pos = (mid_pos[0], mid_pos[1] + 230)
    zoomOut(hwnd)
    # 屏幕下移
    shiftScreen(hwnd, mid_pos, -3)
    # 放一个兵
    arm_pos = getTemplatePos(hwnd, cap, TEMPLATES[UNITS[unit]], offset="top")
    if arm_pos:
        logger.info(f"放{unit}")
        click(hwnd, arm_pos)
        time.sleep(0.2)
        click(hwnd, place_arms_pos)
        time.sleep(0.2)
    if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["giveup"], timeout=2):
        if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["giveup_confirm"], timeout=2):
            if waitUntilMatchThenClick(hwnd, cap, TEMPLATES["backhome"], timeout=2):
                logger.info("回营")
                return
            else:
                logThenExit("未找到回营按钮", "no_backhome.png")
        else:
            logThenExit("未找到确认按钮", "giveup_confirm.png")
    else:
        logThenExit("未找到放弃按钮", "no_giveup.png")


if __name__ == "__main__":
    pass
