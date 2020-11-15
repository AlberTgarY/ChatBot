# coding=utf-8
from sqlite3.dbapi2 import connect
import url_manager, html_downloader, html_parser
import configparser
from Logger import get_log

config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
counter = config.get("num", "num_page")
page = config.get("num", "page")
logger = get_log()


# Main program of the crawler
class SpiderMain(object):

    # init
    def __init__(self):

        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()

    def craw(self, root_url):

        # count for url successfully downloaded
        count = 0

        # add the root url
        self.urls.add_new_url(root_url)

        # for i in range(page+1, page+2):
        #     url_l = "https://github.com/search?l=Python&o=desc&p="
        #     url_r = "&q=slackbot&s=stars&type=Repositories"
        #     new_url = url_l+str(i)+url_r
        #     self.urls.add_new_url(new_url)

        print(self.urls.new_urls)
        # running until set() has no new url
        while self.urls.has_new_url():
            try:

                new_url = self.urls.get_new_url()

                print("craw %d : %s" % (count, new_url))
                # download code
                html_cont = self.downloader.download(new_url)
                logger.info(">>>Start crawling: "+new_url)
                # parse the code
                res_data = self.parser.parse(new_url, html_cont)
                self.parser.fetch_python_code(res_data)

                if count == int(counter):
                    break

                count = count + 1

            except Exception as e:
                logger.debug("Got a Error in method [craw]: " +str(e))
                print("Got a Error in method [craw]: " +str(e))


if __name__ == "__main__":
    # channels:history
    # groups:history
    # groups: history
    # mpim:history
    # 设置入口页 URL
    # https://news.sina.com.cn/  https://news.163.com/
    logger.info("----------------------Crawler has started---------------------------")
    root_url = "https://github.com/search?l=Python&o=desc&p=" + str(page) + "&q=slackbot&s=stars&type=Repositories"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
