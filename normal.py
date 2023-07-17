import json
import os

import execjs
import re
import requests

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
    "id": "",
}
def get_video_url(id):
    d = f'{{"ids": "[{id}]", "level": "standard", "encodeType": "aac", "csrf_token": ""}}'
    enc = js.call("d", d)
    data = {
        "params": enc['encText'],
        "encSecKey": enc['encSecKey']
    }
    params['id'] = id
    dom = requests.get(title_url, headers=headers, params=params).text
    name = re.findall(r'<title>(.*?)</title>', dom)[0]
    name = name.replace(" ", "").replace("\n", "").replace("/", ";")

    all_data = requests.post(url, headers=headers, data=data).text
    all_data = json.loads(all_data)
    download_url = all_data['data'][0]['url']
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
    ]
    id_list = []
    for url in url_list:
        id = re.findall(r"id=(\d+)", url)[0]
        id_list.append(id)
    for id in id_list:
        download_video(id)


if __name__ == '__main__':
    main()