import json
import os

import execjs
import re
import aiohttp
import aiofiles
import asyncio

js = execjs.compile(open("wangyiyun.js", "r", encoding="utf-8").read())
loop = asyncio.get_event_loop()
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
async def get_video_url(id, session):
    d = f'{{"ids": "[{id}]", "level": "standard", "encodeType": "aac", "csrf_token": ""}}'
    enc = await loop.run_in_executor(None, js.call, "d", d)
    data = {
        "params": enc['encText'],
        "encSecKey": enc['encSecKey']
    }
    params['id'] = id
    async with session.get(title_url, headers=headers, params=params) as res:
        dom = await res.text()
        name = re.findall(r'<title>(.*?)</title>', dom)[0]
        name = name.replace(" ", "").replace("\n", "").replace("/", ";")

    async with session.post(url, headers=headers, data=data) as res:
        all_data = await res.text()
        all_data = json.loads(all_data)
        download_url = all_data['data'][0]['url']
    return name, download_url

async def download_video(id, session):
    name, url = await get_video_url(id, session)
    print(f"{name}开始下载")
    async with aiofiles.open(f"./songs/{name}.mp4", mode="wb") as f:
        async with session.get(url) as res:
            await f.write(await res.content.read())
            print(f"{name}下载完成")



async def main():
    async with aiohttp.ClientSession() as session:
        # https://music.163.com/#/song?id=2061887794
        url_list = [
            'https://music.163.com/#/song?id=2061887794',
            'https://music.163.com/#/song?id=2061888566'
        ]
        id_list = []
        for url in url_list:
            id = re.findall(r"id=(\d+)", url)[0]
            id_list.append(id)
        tasks = [asyncio.create_task(download_video(id, session)) for id in id_list]
        await asyncio.wait(tasks)

if __name__ == '__main__':
    loop.run_until_complete( main() )
