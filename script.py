"""
作者：yuanl
日期：2024年12月22日
"""
import os.path
import pyautogui
from paddleocr import PaddleOCR
from key_words import *
from utils import *


def collect(kb, ms, window_loc, templates):
    left, top, right, bottom = window_loc
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    zoomOut(kb, ms, mid_pos, times=2000)
    for _ in range(4):
        ms.position = mid_pos
        pyautogui.mouseDown()  # 按下鼠标左键
        time.sleep(0.1)
        pyautogui.moveTo(mid_pos[0], mid_pos[1] + 200, duration=0.2)  # 向上移
        time.sleep(0.1)
        pyautogui.mouseUp()
    time.sleep(1)
    logger.info('识别圣水车')
    while True:
        wheelbarrow_pos = getMidCoordinate(window_loc, templates['elixir1'], threshold=0.8)
        if not wheelbarrow_pos:
            wheelbarrow_pos = getMidCoordinate(window_loc, templates['elixir2'], threshold=0.8)
            if not wheelbarrow_pos:
                logger.warning('未找到圣水车')
                return
        moveThenClick(ms, wheelbarrow_pos)
        time.sleep(1)
        logger.info('识别收集和关闭按钮')
        close_pos = getMidCoordinate(window_loc, templates['close'])
        if not close_pos:
            logger.info('识别到了圣水瓶，重新识别圣水车')
        else:
            break
    collect_pos = getMidCoordinate(window_loc, templates['collect'])
    if collect_pos:  # 如果找到收集按钮就点一下，没找到可能是因为圣水满了，收集按钮变灰，识别不到，所以直接点关闭
        logger.info('收集')
        moveThenClick(ms, collect_pos)
        time.sleep(1)
    logger.info('关闭')
    moveThenClick(ms, close_pos)


def getAttackPos(window_loc, ocr):
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    scr_shot = ImageGrab.grab(window_loc)
    scr_shot = np.array(scr_shot)
    result = ocr.ocr(scr_shot[round(1 / 2 * h):, : round(1 / 2 * w), :])
    if not result[0]:
        return None
    for line in result[0]:
        if '进攻' in line[1][0]:
            four_corner = line[0]
            mid_point = (
                round((four_corner[0][0] + four_corner[1][0]) / 2), round((four_corner[0][1] + four_corner[2][1]) / 2))
            attack_pos = (left + mid_point[0], top + mid_point[1] + round(1 / 2 * h))
            return attack_pos
    return None


def waitUntilMatch(ocr, window_loc, time_limit=10.0):
    time.sleep(1)
    left, top, right, bottom = window_loc
    w, h = right - left, bottom - top
    start_time = time.time()
    while True:
        if time.time() - start_time >= time_limit:
            return False
        logger.info(f'正在匹配对手：[{time.time() - start_time:.2f}/{time_limit:.2f}]')
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        result = ocr.ocr(scr_shot[: round(1 / 3 * h), round(1 / 3 * w): round(2 / 3 * w), :])
        if not result[0]:
            time.sleep(1)
            continue
        for line in result[0]:
            if '开战倒计时' in line[1][0]:
                return True


def attack(kb, ms, window_loc, ocr, templates, unit, number):
    left, top, right, bottom = window_loc
    h, w = bottom - top, right - left
    search_times = 5
    while True:
        find = False
        for i in range(search_times):
            attack_pos = getAttackPos(window_loc, ocr)
            if not attack_pos:
                logThenExit('未找到进攻按钮', 'no_attack.png')
            moveThenClick(ms, attack_pos)
            time.sleep(1)
            if not matchThenClick(ms, templates['search'], window_loc):
                logThenExit('未找到搜索按钮', 'no_search.png')
            if waitUntilMatch(ocr, window_loc):  # 找到对手
                find = True
                break
            else:  # 规定时间内未找到对手
                logger.warning(f'规定时间内没匹配到，退出重新搜索对手：[{i + 1}/{search_times}]')
                if not matchThenClick(ms, templates['cancel'], window_loc):
                    logThenExit('未找到取消按钮', 'no_cancel.png')
            time.sleep(3)
        if find:
            logger.info('开始进攻')
            break
        else:
            logger.warning(f'连续{search_times}次未找到对手，等半分钟再搜')
            time.sleep(30)
    # 开打
    mid_pos = ((left + right) // 2, (top + bottom) // 2)
    place_arms_pos = (mid_pos[0], top + 755)
    zoomOut(kb, ms, mid_pos)
    def placeArms(arm_num):
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        for _ in range(4):  # 屏幕下移
            ms.position = mid_pos
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.moveTo(mid_pos[0], mid_pos[1] - 200, duration=0.2)
            time.sleep(0.1)
            pyautogui.mouseUp()
        war_machine_pos = getMidCoordinate(window_loc, templates['war_machine'], scr_shot)
        if war_machine_pos:
            logger.info('放战争机器')
            moveThenClick(ms, war_machine_pos)
            time.sleep(0.2)
            moveThenClick(ms, place_arms_pos)
            time.sleep(0.2)
        arm_pos = getTopCoordinate(window_loc, templates[f'{unit[1]}'], scr_shot)
        if arm_pos:
            logger.info(f'放{unit[0]}')
            moveThenClick(ms, arm_pos)
            time.sleep(0.2)
            ms.position = place_arms_pos
            time.sleep(0.2)
            for _ in range(number):
                ms.click(pynput.mouse.Button.left)
                time.sleep(0.2)
        if unit[0] == '女巫':
            logger.info('女巫放技能')
            for _ in range(number):
                matchThenClick(ms, templates['skill'], window_loc, mid=False)
        ms.position = mid_pos  # 鼠标移动到中心
    placeArms(number)
    second_phase = False
    while True:  # 等待战斗结束
        if matchThenClick(ms, templates['backhome'], window_loc):
            logger.info('回营')
            return
        scr_shot = ImageGrab.grab(window_loc)
        scr_shot = np.array(scr_shot)
        result = ocr.ocr(scr_shot[: round(1 / 3 * h), round(1 / 3 * w): round(2 / 3 * w), :])
        if result[0]:
            for line in result[0]:
                if '开战倒计时' in line[1][0]:
                    second_phase = True
                    break
        if second_phase:
            break
        time.sleep(5)
    logger.info('进入二阶段')
    time.sleep(2)
    placeArms(number + 1)
    while True:  # 等待战斗结束
        if matchThenClick(ms, templates['backhome'], window_loc):
            logger.info('回营')
            return
        time.sleep(5)

def main(collect_interval=4, execute_time=3.0, unit='龙', number=4):
    """
    :param collect_interval: 收集间隔（场）
    :param execute_time: 执行时间（小时）
    :param unit:
    :param number:
    """
    if getScaling() != 1.0:
        logger.error('请将显示设置为100%')
        exit(0)
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title='MuMu模拟器12')[1]
    left, top, right, bottom = window_loc

    execute_time *= (60 * 60)
    start_time = time.time()

    while True:
        for _ in range(collect_interval):  # 每打collect_interval场战斗，就收集一次圣水
            zoomOut(keyboard, mouse, ((left + right) // 2, (top + bottom) // 2))  # 缩小视野至最小
            attack(keyboard, mouse, window_loc, ocr, TEMPLATES, (unit, UNITS[unit]), number)  # 进攻
            time.sleep(6)
            logger.info('检查胜利之星')
            matchThenClick(mouse, TEMPLATES['victory_star'], window_loc)  # 检查是否弹出胜利之星奖励
        collect(keyboard, mouse, window_loc, TEMPLATES)  # 收集圣水
        if time.time() - start_time >= execute_time:  # 判断是否到达执行时间，
            break


if __name__ == '__main__':
    # main()
    
    keyboard = pynput.keyboard.Controller()
    mouse = pynput.mouse.Controller()
    window_loc = getWindowLocation(title='MuMu模拟器12')[1]
    left, top, right, bottom = window_loc
    time.sleep(1)
    template = cv2.cvtColor(cv2.imread(os.path.join(ARM_DIR, 'dragon.png')), cv2.COLOR_BGR2RGB)
    # src = ImageGrab.grab((left, top, right, bottom))
    # src = np.array(src)
    src = ImageGrab.grab(window_loc)
    src = np.array(src)
    src = cv2.cvtColor(cv2.imread('test.png'), cv2.COLOR_BGR2RGB)
    pos = getMidCoordinate((left, top, right, bottom), template, src)
    if pos:
        mouse.position = pos
    else:
        print('未找到')

    # ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    # window_loc = getWindowLocation(title='MuMu模拟器12')[1]
    # left, top, right, bottom = window_loc
    # h, w = bottom - top, right - left
    # # scr_shot = ImageGrab.grab(window_loc)
    # # scr_shot = np.array(scr_shot)
    # scr_shot = cv2.cvtColor(cv2.imread('test.png'), cv2.COLOR_BGR2RGB)
    # result = ocr.ocr(scr_shot[: round(1 / 3 * h), round(1 / 3 * w):round(2 / 3 * w), :])
    # if not result[0]:
    #     time.sleep(1)
    # for line in result[0]:
    #     if '开战倒计时' in line[1][0]:
    #         print(result)
