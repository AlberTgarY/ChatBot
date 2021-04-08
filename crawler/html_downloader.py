# coding=utf-8
import ssl
from urllib import request
from fake_useragent import UserAgent
from Logger import get_log
'''
This file contains the HTMLDownloader, it will access and download the HTML raw code from the target website.
author: ZHAN YICHENG 03/04/2021
'''
logger = get_log()


class HtmlDownloader(object):

    # This method downloads the HTML page
    @staticmethod
    def download(url):
        context = ssl._create_unverified_context()
        if url is None:
            raise ValueError('target url is None')

        try:
            ua = UserAgent()
            # fake headers will help the crawler to dodge the website`s anti-crawling module.
            headers = {"User-Agent": ua.random}
            # request website`s context
            r = request.Request(url=url,headers=headers)
            response = request.urlopen(r, context=context)
            if response.getcode() != 200:
                return None
            else:
                return response.read()
        except Exception as e:
            logger.debug(url+' got a error: [' + str(e) + " ]")
            print(url+' got a error: [' + str(e) + " ]")

