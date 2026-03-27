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
        # 识别白色/红色背景圣水
        wheelbarrow_pos = getTemplatePos(hwnd, cap, TEMPLATES["elixir1"], scr_shot, threshold=0.8) or getTemplatePos(hwnd, cap, TEMPLATES["elixir2"], scr_shot, threshold=0.8)
        if not wheelbarrow_pos:
            find_wheelbarrow = False
            # 识别斧子
            print("识别斧子")
            for filename in os.listdir(TEMPLATES["axe"]):
                axe = None
                with open(os.path.join(TEMPLATES["axe"], filename), "rb") as f:
                    axe = cv2.cvtColor(pickle.load(f), cv2.COLOR_BGR2RGB)
                wheelbarrow_pos = getTemplatePos(hwnd, cap, axe, scr_shot, threshold=0.75, record_fail=False)
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
    time_limit: float = 20.0,
    event: threading.Event = None
):
    time.sleep(1)
    start_time = time.time()
    while True:
        if event and event.is_set():
            return False
        if time.time() - start_time >= time_limit:
            return False
        logger.info(f"正在匹配对手：[{time.time() - start_time:.2f}/{time_limit:.2f}]")
        if getOcrPos(hwnd, cap, ocr, "开战倒计时", crop=(0.0, 1 / 3, 1 / 3, 2 / 3)):
            return True
        time.sleep(1)


def searchOpponentUntilFind(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    search_times: int = 5,
    event: threading.Event = None,
):
    """
    有时候会一直搜不到人，所以要判断一下，如果连续搜了几次都搜不到人，就等一会再搜
    """
    while True:
        for i in range(search_times):
            attack_pos = getOcrPos(hwnd, cap, ocr, "进攻", crop=(0.5, 1.0, 0.0, 0.5))
            if not attack_pos:
                logThenExit("未找到进攻按钮")
            click(hwnd, attack_pos)
            if not waitUntilMatchThenClick(hwnd, cap, TEMPLATES["search"], timeout=2):
                logThenExit("未找到搜索按钮")
            if matchOpponent(hwnd, cap, ocr, event=event):
                logger.info("开始进攻")
                return
            if event and event.is_set():
                return
            # 规定时间内未找到对手，取消后继续尝试
            logger.warning(f"规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]")
            if not matchTemplateThenClick(hwnd, cap, TEMPLATES["cancel"]):
                logThenExit("未找到取消按钮")
            time.sleep(3)
        logger.warning(f"连续{search_times}次未找到对手，等半分钟再搜")
        time.sleep(30)


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
    searchOpponentUntilFind(hwnd, cap, ocr, event=event)
    if event and event.is_set():
        return
    # 开打
    place_arms_pos = (mid_pos[0], mid_pos[1] + 230)
    zoomOut(hwnd)

    def placeArms():
        shiftScreen(hwnd, mid_pos, -3)
        # 如果第一阶段战争机器挂了，第二阶段直升机图像会自动高亮。因此先点一下
        time.sleep(0.5)
        click(hwnd, place_arms_pos)
        time.sleep(0.5)
        # 同一帧截屏复用
        scr_shot = cap.grab()
        war_machine_pos = getTemplatePos(hwnd, cap, TEMPLATES["war_machine"], scr_shot, threshold=0.9)
        if war_machine_pos:
            logger.info("放战争机器")
            click(hwnd, war_machine_pos)
            time.sleep(0.2)
            click(hwnd, place_arms_pos)
            time.sleep(0.2)
        else:
            helicopter_pos = getTemplatePos(hwnd, cap, TEMPLATES["helicopter"], scr_shot, threshold=0.9)
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
            for _ in range(number):
                click(hwnd, place_arms_pos)
                time.sleep(0.2)
        if unit == "女巫":
            logger.info("女巫放技能")
            for _ in range(number):
                matchTemplateThenClick(hwnd, cap, TEMPLATES["skill"], offset='bottom')
                time.sleep(0.5)

    def runPhase(phase: int) -> bool:
        """
        进攻阶段的等待循环。
        返回 True 表示进入下一阶段。
        返回 False 表示战斗结束。
        """
        placeArms()
        phase_start = time.time()
        last_time = phase_start
        with tqdm(total=BATTLE_TIME, unit="秒") as pbar:
            while True:
                if event and event.is_set():
                    return False
                if time.time() - phase_start >= BATTLE_TIME:
                    logThenExit(f"超过战斗时间上限（{BATTLE_TIME}秒），可能界面出了问题", fail_type='none')
                if matchTemplateThenClick(hwnd, cap, TEMPLATES["backhome"]):
                    pbar.close()
                    logger.info(f"第{phase}阶段进攻结束，用时：{time.time() - phase_start:.1f}秒")
                    logger.info("回营")
                    return False
                if (phase == 1) and getOcrPos(hwnd, cap, ocr, "开战倒计时", crop=(0.0, 1 / 3, 1 / 3, 2 / 3)):
                    logger.info(f"第{phase}阶段进攻结束，用时：{time.time() - phase_start:.1f}秒")
                    return True
                matchTemplateThenClick(hwnd, cap, TEMPLATES["machine_skill"], 'bottom')
                time.sleep(2)
                now = time.time()
                pbar.update(round(now - last_time, 1))
                last_time = now
                pbar.set_description(f"第{phase}阶段进攻中：{now - phase_start:.1f}/{BATTLE_TIME}秒")

    if not runPhase(1):
        return
    logger.info("进入二阶段")
    time.sleep(2)
    if event and event.is_set():
        return
    runPhase(2)


def attackThenRetreat(
    hwnd: int,
    cap: WindowCapture,
    ocr: PaddleOCR,
    unit: str,
    event: threading.Event = None
):
    w, h = getWindowSize(hwnd)
    mid_pos = (w // 2, h // 2)
    searchOpponentUntilFind(hwnd, cap, ocr, event=event)
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
                logThenExit("未找到回营按钮")
        else:
            logThenExit("未找到确认按钮")
    else:
        logThenExit("未找到放弃按钮")


if __name__ == "__main__":
    pass
