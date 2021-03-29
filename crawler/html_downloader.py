# coding=utf-8
import ssl
from urllib import request
from fake_useragent import UserAgent
from Logger import get_log

logger = get_log()
# HTML downloader
class HtmlDownloader(object):

    #  download the page
    @staticmethod
    def download(url):
        context = ssl._create_unverified_context()
        if url is None:
            raise ValueError('target url is None')

        try:
            ua = UserAgent()
            # fake headers
            headers = {"User-Agent": ua.random}
            # request website
            r = request.Request(url=url,headers=headers)
            response = request.urlopen(r, context=context)
            if response.getcode() != 200:
                return None
            else:
                return response.read()
        except Exception as e:
            logger.debug(url+' got a error: [' + str(e) + " ]")
            print(url+' got a error: [' + str(e) + " ]")

