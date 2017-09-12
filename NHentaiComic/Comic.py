import re

import os
import urllib.request

import requests
from bs4 import BeautifulSoup


class Comic:
    '''
    A class for operate comics.
    '''
    def __init__(self, comicID):
        self.comicID = comicID
        self.indexURL = 'https://nhentai.net/g/%s/' % comicID
        self.indexHTML = Common.parse_html(self.indexURL)
        self.title = self.indexHTML.select('div#info')[0].select('h2')[0].string
        self.galleryID = Common.getBetween(
            self.indexHTML.select("img.lazyload")[0].get('data-src'),
            'https://t.nhentai.net/galleries/',
            '/'
        )
        return

    def getMaxPage(self):
        gallerythumbs = self.indexHTML.select("a.gallerythumb")
        pageList = []
        for gallerythumb in gallerythumbs:
            pageList.append(int(gallerythumb.get('href').split('/')[3]))
        return max(pageList)

    def getImgType(self):
        url = 'https://nhentai.net/g/%s/1/' % self.comicID
        response = Common.parse_html(url)
        return Common.getBetween(
            response.select('img.fit-horizontal')[0].get('src'),
            'https://i.nhentai.net/galleries/%s/1.' % self.galleryID,
            ''
        )

    def downImgs(self):
        imgType = self.getImgType()
        if not os.path.exists('Comic'):
            os.mkdir('Comic')
        if not os.path.exists('Comic/%s - %s' % (self.title, self.comicID)):
            os.mkdir('Comic/%s - %s' % (self.title, self.comicID))
        for i in range(1, self.getMaxPage() + 1):
            url = 'https://i.nhentai.net/galleries/%s/%s.%s' % (self.galleryID, i, imgType)
            path = 'Comic/%s - %s/%s.%s' % (self.title, self.comicID, i, imgType)
            try:
                Common.down_img(url, path)
            except BaseException as e:
                print('Error! Error info is: %s' % e)






class Common:
    @staticmethod
    def getBetween(s, start, end):
        return re.search('%s(.*)%s' % (start, end), s).group(1)
    @staticmethod
    def parse_html(url):
        '''Use lxml to parse html.'''
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/55.0.2883.103 Safari/537.36'
        }
        response = requests.get(url).content
        return BeautifulSoup(response, 'lxml')
    @staticmethod
    def down_img(imgurl, localpath):
        '''A function to save img'''
        if os.path.exists(localpath):
            print('%s exist!' % localpath)
            return
        print(imgurl, localpath)
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/55.0.2883.103 Safari/537.36'
        }
        request = urllib.request.Request(url=imgurl, headers=headers)
        data = urllib.request.urlopen(request).read()
        img_file = open(localpath, 'wb')
        img_file.write(data)
        img_file.close()
        return
