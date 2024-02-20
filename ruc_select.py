import asyncio
from pyppeteer import launch
import ddddocr
from pyppeteer.browser import Page
from pyppeteer.page import Request
from typing import Optional
import argparse
import time
import requests
import getpass


TOKEN = None


def bark(title: str, body: str):
    if TOKEN:
        requests.post("https://api.day.app/" + TOKEN + "/" + title + "/" + body)


async def login(page: Page, username: str, password: str) -> bool:
    await page.goto('https://v.ruc.edu.cn')
    print("Goto main page.")

    await asyncio.sleep(1)

    login_frame = await page.J("#login-iframe")
    assert login_frame is not None
    login_frame = await login_frame.contentFrame()
    assert login_frame is not None

    await login_frame.waitForSelector("#username > input[type=text]")
    await login_frame.type("#username > input[type=text]", username)
    print("Enter username.")

    await login_frame.waitForSelector("#password > input[type=password]")
    await login_frame.type("#password > input[type=password]", password)
    print("Enter password.")

    code = await login_frame.J("#codeImg")
    assert code is not None
    await code.screenshot(path="code.png")
    with open('code.png', 'rb') as f:
        img_bytes = f.read()
    res = ddddocr.DdddOcr().classification(img_bytes)
    print(f"Classify captcha {res}.")

    await login_frame.waitForSelector("#captcha-input > input[type=text]")
    await login_frame.type("#captcha-input > input[type=text]", res)
    print("Enter captcha.")

    await login_frame.click("#remember_me > span.left > div > label > i")
    print("Remeber me.")

    await login_frame.click("#login-submit")
    print("Login submit.")
    await asyncio.sleep(1)

    app= await page.JJ("#app")
    if len(app) == 0:
        return await login(page, username, password)
    else:
        return True


template = "#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-5 > div:nth-child(2) > div > div:nth-child(7) > ul > li:nth-child(1) > ul > li:nth-child({idx})"
schools = [
    [
        "数学学院",
        "外国语学院",
        "商学院",
        "财政金融学院",
        "经济学院",
        "统计学院",
        "新闻学院",
        "社会与人口学院",
        "公共管理学院",
        "高瓴人工智能学院",
        "应用经济学院",
        "马克思主义学院",
        "信息资源管理学院",
        "心理学系",
        "农业与农村发展学院",
        "理学院-化学系",
        "理学院-物理学系",
        "国际关系学院",
        "环境学院",
        "文学院",
        "法学院",
        "明德书院",
        "哲学院",
        "劳动人事学院",
        "国学院",
        "历史学院",
        "信息学院",
        "中共党史党建学院",
        "国际文化交流学院",
        "理学院",
    ],
    [
        "宏观经济",
        "外国文化",
        "教育与社会",
        "教育的经济分析",
        "宗教学",
        "管理学",
        "教育管理",
        "文化与思潮",
        "大数据及其交叉学科",
        "心理学基础理论",
        "中国史",
        "应用法学",
        "国际经贸",
        "环境污染治理",
    ],
    [
        "认知科学与哲学",
        "调查与商业分析",
        "数字人文",
        "可持续发展",
        "定量数据分析方法及其应用",
        "全球治理与国际组织人才培养",
        "空间云数据竞争力分析师",
        "马克思主义理论",
        "全球化与伦理学",
        "房地产经济与管理",
        "数据法学",
        "健康政策与治理创新",
        "认知科学与哲学",
        "区块链与数字经济",
    ]
]


async def navigate(page: Page, first: int, second: Optional[int] = None, school: Optional[str] = None):
    await asyncio.sleep(1)
    await page.goto("https://jw.ruc.edu.cn/Njw2017/index.html#/")
    print("Goto jw page.")

    await asyncio.sleep(3)
    await page.waitForSelector("#app")
    await page.goto("https://jw.ruc.edu.cn/Njw2017/index.html#/student/student-choice-center/")
    await asyncio.sleep(1)
    await page.goto("https://jw.ruc.edu.cn/Njw2017/student/student-choice-center/student-select-course.html#/?wf=undefined&resCode=undefined&jczy013id=2023-2024-2&xkgl017id=c134b4230000WH&xkgl019id=c134d7580000WH&language=zh")
    await asyncio.sleep(5)

    await page.click(f"body > div#app > div.main > div#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-5 > div:nth-child(2) > div > div:nth-child({first + 1}) > div > div.serial.el-col")
    first_menu = [
            "思想政治理论课",
            "大学外语（拓展类课程）",
            "通识核心课",
            "通识教育大讲堂",
            "个性化选修",
            "跨学科专业选修",
            "公共艺术教育",
            "发展指导",
            "原典选读类",
            "发展指导（北外共享课）",
            "大学体育",
    ]
    print("Click " + first_menu[first - 1])

    if second is not None:
        second_menu = {
            3: ["思辨与表达", "科学与技术", "历史与文化", "生命与环境", "世界与中国", "哲学与伦理", "实证与推理", "审美与诠释"],
            6: ["双选认证", "非双选认证", "荣誉选课"],
            8: ["创新创业指导", "兴趣与爱好", "心理素质与心理健康-心理健康指导", "基础技能强化与拓展-方法与工具", "职业发展与就业指导-职业技能强化", "基础技能强化与拓展-第二外国语学习"],

        }
        await asyncio.sleep(1)
        await page.click(f"#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-5 > div:nth-child(2) > div > div:nth-child(7) > ul > li:nth-child({second}) > div > i")
        print("Click " + second_menu[first][second - 1])

    if school is not None:
        await asyncio.sleep(1)
        assert second is not None
        idx = schools[second-1].index(school)
        await page.click(template.format(idx=idx + 1))
        print("Click " + school)


async def refresh_spots(page: Page, candidate: list, drop: list):
    while True:
        await asyncio.sleep(1)
        await page.click("#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-19 > form > div:nth-child(6) > div > button")
        await asyncio.sleep(1)
        for idx in candidate:
            div = await page.evaluate('''() => {
    return {
    '''+f'''"text": document.querySelector("#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-19 > div > div.qz-table > div > div.el-table__body-wrapper > table > tbody > tr:nth-child({idx}) > td:nth-child(10)").textContent,
    "name": document.querySelector("#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-19 > div > div.qz-table > div > div.el-table__body-wrapper > table > tbody > tr:nth-child({idx}) > td:nth-child(6)").textContent
''' + '};}')
            if div["text"] != "已满":
                for to_drop in drop:
                    await page.click(f"#twoTable > div.twoCont > div > div > div.qz-table.result-table > div > div.el-table__fixed-right > div.el-table__fixed-body-wrapper > table > tbody > tr:nth-child({to_drop}) > td.el-table_1_column_2.is-left > div > button")
                    await asyncio.sleep(0.1)
                    await page.click("#myDialog > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--primary")
                    await asyncio.sleep(0.1)
                    print("退课" + to_drop)

                await page.click(f"#oneTable > div.oneCont > div:nth-child(1) > div > div.el-col.el-col-19 > div > div.qz-table > div > div.el-table__fixed-right > div.el-table__fixed-body-wrapper > table > tbody > tr:nth-child({idx}) > td.el-table_1_column_1.is-left > div > button")
                await asyncio.sleep(0.1)
                if await page.J("#myDialog > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--primary"):
                    await page.click("#myDialog > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--primary")
                    print("选课成功!!" + div["name"])
                    bark("选课成功!!", div["name"])
                    exit(0)
                else:
                    print("课程时间冲突." + div["name"])
                    bark("课程时间冲突", div["name"])
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), div["name"], div["text"])


async def main(arg):
    browser = await launch(headless=not arg.chrome)
    page = await browser.targets()[0].page()
    assert page is not None
    # page = await browser.newPage()
    
    await login(page, arg.username, arg.password)
    await navigate(page, arg.first, arg.second, arg.school)
    await refresh_spots(page, list(map(int, arg.monitor)), list(map(int, arg.drop)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="RUCSelect", description="RUC course monitor and selection")
    parser.add_argument("username", type=str, help="username")
    parser.add_argument("first", type=int, help="First level menu")
    parser.add_argument("second", type=int, help="Second level menu", default=None, nargs="?")
    parser.add_argument("school", type=str, help="School menu", default=None, nargs="?")
    parser.add_argument("--monitor", nargs="+", required=True, help="List of line numbers")
    parser.add_argument("--drop", nargs="*", help="List of line numbers in Table2 that want to drop", default=[])
    parser.add_argument("--bark", type=str, help="bark notification token")
    parser.add_argument("--chrome", action="store_true")
    arg = parser.parse_args()
    TOKEN = arg.bark
    arg.password = getpass.getpass("输入微人大密码: ")

    bark("开始", str(arg))
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(main(arg))
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            if isinstance(e, RuntimeError) and "This event loop is already running" in str(e):
                exit(0)
            print("尝试重启中...")
            print(e)
            time.sleep(5)
            bark("报错", str(e))

