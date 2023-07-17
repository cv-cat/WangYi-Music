import time
from io import BytesIO
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import cv2
import numpy as np
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
import json
import os
import execjs
import re
import requests

base_url = "https://music.163.com/"

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--disable-blink-features=AutomationControlled")
# option.add_argument('--headless')
# option.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'")
s = Service(r"D:\Desktop\Data\DriverBug\chromedriver.exe")
bro = webdriver.Chrome(service=s, options=option,)
# bro.maximize_window()
bro.implicitly_wait(10)
bro.get(base_url)
page_text = bro.page_source
tree = etree.HTML(page_text)
login = tree.xpath('/html/body/div[1]/div[1]/div/div[1]/a')
wangyi_phonenum = '1'
wangyi_password = '1'
wait = WebDriverWait(bro, 3)

def handel_img(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 60, 60)
    return imgCanny

def add_alpha_channel(img):
    r_channel, g_channel, b_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_new = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))
    return img_new


def match(jpg_content, png_content):
    f1 = BytesIO()
    f1.write(jpg_content)
    img_jpg = Image.open(f1)
    img_jpg = cv2.cvtColor(np.asarray(img_jpg), cv2.COLOR_RGB2BGR)
    f2 = BytesIO()
    f2.write(png_content)
    img_png= Image.open(f2)
    img_png = cv2.cvtColor(np.asarray(img_png), cv2.COLOR_RGB2BGR)
    if img_jpg.shape[2] == 3:
        img_jpg = add_alpha_channel(img_jpg)
    img = handel_img(img_jpg)
    small_img = handel_img(img_png)
    res_TM_CCOEFF_NORMED = cv2.matchTemplate(img, small_img, 3)
    value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
    value = value[3][0]
    return value



if login:
    print("需要登录")
    time.sleep(1)
    print('正在点击主页登录按钮')
    # login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/a')))
    # login = wait.until(lambda x: x.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/a'))
    login = bro.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/a')
    login.click()
    time.sleep(1)
    print('正在更改登录模式按钮')
    change_mode = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div/div/div/a')))
    change_mode.click()
    time.sleep(1)
    print('正在点击同意许可按钮')
    agree = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div/div/div/div[2]/input')))
    agree.click()
    time.sleep(1)
    print('正在点击手机号登录按钮')
    new_login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div/div/div/div[1]/div[1]/a/div')))
    new_login.click()
    time.sleep(1)
    print('正在点击密码登录按钮')
    password_login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div[1]/a')))
    password_login.click()
    time.sleep(1)
    print('正在输入手机号')
    phone = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/section/div[1]/div/input')))
    phone.send_keys(wangyi_phonenum)
    time.sleep(1)
    print('正在输入密码')
    password = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/section/div[2]/div/input')))
    password.send_keys(wangyi_password)
    time.sleep(1)
    # auto_login = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/section/div[3]/label/input')))
    # auto_login.click()
    # time.sleep(1)
    print('正在点击登录按钮')
    login_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/section/a/div')))
    login_button.click()
    time.sleep(1)
    print('正在处理滑块')
    script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
    bro.execute_script(script)
    time.sleep(1)
    slider_box = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div[2]')))
    error_more = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div[2]/div/div[2]/div[3]')))
    time.sleep(1)
    slider = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div[2]/div/div[2]/div[2]/span')))
    actions = ActionChains(bro)
    # 判断是否登录成功
    while True:
        print('正在获取滑块图片')
        png = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[8]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]')))
        png_src = png.get_attribute('src')
        png_content = requests.get(png_src).content
        jpg = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[8]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]')))
        jpg_src = jpg.get_attribute('src')
        jpg_content = requests.get(jpg_src).content
        value = match(jpg_content, png_content) + 11
        print('正在点击滑块按钮')
        time.sleep(1)
        actions.click_and_hold(slider).move_by_offset(value, 0).release().perform()
        time.sleep(1)
        try:
            if slider_box.is_displayed():
                print('滑块验证失败，正在重试')
            if error_more.is_displayed():
                error_more.click()
                continue
        except:
            print('滑块验证成功')
            break

else:
    print("不需要登录")

dynamic_cookie = bro.execute_script("return document.cookie;")
print("dynamic_cookie:", dynamic_cookie)
print(bro.get_cookies())
try:
    csrf_token = re.findall(r'__csrf=(.*?);', dynamic_cookie)[0]
except:
    csrf_token = re.findall(r'__csrf=(.*)', dynamic_cookie)[0]
try:
    WNMCID = re.findall(r'WNMCID=(.*?);', dynamic_cookie)[0]
except:
    WNMCID = re.findall(r'WNMCID=(.*)', dynamic_cookie)[0]
MUSIC_U = re.findall("'MUSIC_U', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '(.*?)'", str(bro.get_cookies()))[0]
bro.quit()
print("csrf_token:", csrf_token)
print("MUSIC_U:", MUSIC_U)

js = execjs.compile(open("wangyiyun.js", "r", encoding="utf-8").read())
if not os.path.exists("songs"):
    os.mkdir("songs")

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
}

url = "https://music.163.com/weapi/song/enhance/player/url/v1"
title_url = 'https://music.163.com/song'
data = {
    "params": "",
    "encSecKey": ""
}
params = {
    "csrf_token": csrf_token,
}
cookies = {
    "WNMCID": WNMCID,
    "MUSIC_U": MUSIC_U,
}
title_params = {
    "id": "",
}
def get_video_url(id):
    d = f'{{"ids": "[{id}]", "level": "standard", "encodeType": "aac", "csrf_token": "{csrf_token}"}}'
    print(d)
    enc = js.call("d", d)
    data = {
        "params": enc['encText'],
        "encSecKey": enc['encSecKey']
    }
    title_params['id'] = id
    dom = requests.get(title_url, headers=headers, params=title_params).text
    name = re.findall(r'<title>(.*?)</title>', dom)[0]
    name = name.replace(" ", "").replace("\n", "").replace("/", ";")

    all_data = requests.post(url, headers=headers, data=data, params=params, cookies=cookies).text
    all_data = json.loads(all_data)
    download_url = all_data['data'][0]['url']
    print(name, download_url)
    return name, download_url

def download_video(id):
    name, url = get_video_url(id)
    content = requests.get(url).content
    print(f"{name}开始下载")
    with open(f"./songs/{name}.mp3", mode="wb") as f:
        f.write(content)
        print(f"{name}下载完成")

def main():
    url_list = [
        'https://music.163.com/#/song?id=518682659',
        'https://music.163.com/#/song?id=233931',
    ]
    id_list = []
    for url in url_list:
        id = re.findall(r"id=(\d+)", url)[0]
        id_list.append(id)
    for id in id_list:
        download_video(id)


main()


