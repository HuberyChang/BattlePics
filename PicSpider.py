import requests
from lxml import etree
import time
import os
from concurrent import futures


url = 'http://www.doutula.com/'
headers = {
    #图片下载设置Referer
    'Referer': 'https://www.doutula.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
}

resp = requests.get(url, headers=headers)
html = etree.HTML(resp.text)


def down_load(src, dirname):
    filename = src.split('/')[-1].split('!')[0]
    #先创建imgs文件夹
    dirname = 'imgs/{}'.format(dirname)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    img = requests.get(src, headers=headers)
    with open('{}/{}'.format(dirname, filename), 'wb') as file:
        file.write(img.content)
    # print(src, filename)



def get_page(url):
    resp = requests.get(url, headers=headers)
    dirname = url.split('/?')[-1]
    print(resp, url)
    html = etree.HTML(resp.text)
    srcs = html.xpath('.//img/@data-original')

    #多线程
    ex = futures.ThreadPoolExecutor(max_workers=40)
    for src in  srcs :
        ex.submit(down_load, src, dirname)


    #单线程
    # for src in srcs:
    #     # print(src)
    #     down_load(src, dirname)
    next_link = html.xpath(".//a[@class='page-link']/@href")
    return next_link


def main():
    next_link_base = 'https://www.doutula.com/article/list/?page='
    current_num = 0
    next_link = ['https://www.doutula.com']

    while next_link:
        time.sleep(0.2)
        current_num += 1
        next_link = get_page(next_link_base+str(current_num))
        if current_num >= 10:
            break


if __name__ == '__main__':
    main()





# srcs = html.xpath('.//img/@data-original')
# for src in srcs:
#     filename = src.split('/')[-1]
#     #img是图片响应，不能字符串解析
#     #img.content是图片的字节内容
#     img = requests.get(src, headers=headers)
#     with open('imgs/'+filename, 'wb') as file:
#         file.write(img.content)
#     print(src, filename)

