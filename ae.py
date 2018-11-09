import requests
import re
import os
from hashlib import md5
import time
from urllib import request
from multiprocessing import Pool
import multiprocessing
import urllib3
urllib3.disable_warnings()

url_set = set()

class Spider:

    def __init__(self):
        self.base_url = 'https://www.ae.com/aerie-bras/aerie/s-cat/4840012?cm=sUS-cUSD&navdetail=mega:cat6610030:c1:p2'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
    def files_name(self, f_name):

        md = md5(f_name.encode('utf-8'))
        return md.hexdigest()

    def parse(self):

        print('---正在请求网址-----')
        response = requests.get(self.base_url, headers=self.headers, verify=False)
        res = re.compile(r'class="product-list">(.+?)<div class="filters-noresult">', re.S).findall(response.text)[0]
        res_find = re.compile(r'class="img-placeholder".+?<img class="item active product-image product-image-front img-responsive lazyload".+?data-srcset="(.+?)">', re.S).findall(res)

        return res_find


    def download_urls(self, urls, page, c):
            senyu = int(c)-int(page)
            t = time.strftime('%Y-%m-%d', time.localtime())
            img = 'img'
            img_day = img+'/'+t
            if not os.path.exists(img):
                os.mkdir(img)
                os.mkdir(img_day)
            else:
                if not os.path.exists(img_day):
                    os.mkdir(img_day)
            path_name = img_day + '/'
            print(urls)

            print('正在下载第%s张图片,剩余%s' % (page, senyu))
            lock = multiprocessing.Lock()
            lock.acquire()
            try:
                request.urlretrieve(urls, filename=path_name+self.files_name(urls)+'.png')

                # res = requests.get(urls)
                # ll = path_name+self.files_name(urls)+'.png'
                # with open(ll, 'wb') as f:
                #     f.write(res.content)
            finally:
                lock.release()

if __name__ == '__main__':
    spider = Spider()
    print('-----------开始下载----------')
    res_urls = spider.parse()
    print('--------准备解析图片-----------')
    p = Pool(20)
    pages = len(res_urls)
    print('共%s张图片' % pages)
    j = 1
    c = pages
    for i in res_urls:
        imges_link = 'https:' + re.compile(r'(.+? )').findall(i)[0].replace('$cat-main_small$', '$PDP_78_Main$').strip()
        p.apply_async(spider.download_urls, args=(imges_link, j, c))
        j += 1

    print('全部下载完成,共%s张图片' % pages)
    p.close()
    p.join()








