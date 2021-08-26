import json
import os

import requests
import pypandoc
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

cookie = {

}

# 盐选专栏的id, 每次只需要更换这个Id就好
# yanxuanId = '1408027608021471232'  # 饲养员的前半生
# yanxuanId = '1312724340308398080'  # 三尸语：打不开的神秘悬棺
# yanxuanId = '1396466111030906880'  # 硬派历史：洪流下的狠人与真相
yanxuanId = '1384200455946293248'  # 罪恶无声：冷门行业发生过的凶案

# 创建盐选专栏文件夹
if not os.path.exists(yanxuanId):
    os.makedirs(yanxuanId)
# 获取sectionId列表
yanxuanUrl = 'https://www.zhihu.com/xen/market/remix/paid_column/{}'.format(yanxuanId)
yanxuanHtml = requests.request('get', yanxuanUrl, headers=headers, cookies=cookie)
soup = BeautifulSoup(yanxuanHtml.text, 'html.parser')
yanxuanJsonStr = ''
for ta in soup.find_all(name='textarea'):
    yanxuanJsonStr = ta.string

yanxuanJson = json.loads(yanxuanJsonStr)

# 通过盐选专栏Id和sectionId来爬取文章
for item in yanxuanJson['appContext']['catalogData']['default']:
    sectionId = item['id']
    serialNumber = item['index']['serialNumberTxt']
    title = item['title']
    print(item['index']['serialNumberTxt'] + '---->' + item['title'] + '----->' + item['id'])
    if os.path.exists('{}/{}_{}.docx'.format(yanxuanId, serialNumber, title)):
        continue
    sectionUrl = "https://www.zhihu.com/market/paid_column/{}/section/{}".format(yanxuanId, sectionId)
    sectionReq = requests.request("get", sectionUrl, headers=headers, cookies=cookie)
    with open("temp.html", 'w+', encoding='utf-8') as html:
        html.write(sectionReq.text)
    pypandoc.convert_file("temp.html", 'docx',
                          outputfile='{}/{}_{}.docx'.format(yanxuanId, serialNumber, title))
    # 删除 temp.html
    if os.path.exists("temp.html"):
        os.remove("temp.html")
