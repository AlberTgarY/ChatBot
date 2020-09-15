# coding=utf-8

import url_manager, html_downloader, html_parser
import configparser

config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
counter = config.get("num", "num_page")

# 爬虫主调程序，主要逻辑
class SpiderMain(object):

    # 初始化，设置 URL 管理器、下载器、解析器、输出器
    def __init__(self):

        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()

    def craw(self, root_url):

        # 下载成功页面计数
        count = 0

        # 添加第一个 URL
        self.urls.add_new_url(root_url)

        for i in range(2, int(counter)):
            url_l = "https://github.com/search?l=Python&o=desc&p="
            url_r = "&q=slackbot&s=stars&type=Repositories"
            new_url = url_l+str(i)+url_r
            self.urls.add_new_url(new_url)
        print(self.urls.new_urls)
        # URL 管理器中存在 URL 时处理
        while self.urls.has_new_url():
            try:

                new_url = self.urls.get_new_url()

                print("craw %d : %s" % (count, new_url))

                html_cont = self.downloader.download(new_url)
                res_data = self.parser.parse(new_url, html_cont)
                self.parser.fetch_python_code(res_data)

                if count == int(counter):
                    break

                count = count + 1

            except Exception as e:
                print(e)

        # self.outputer.output_excel()


if __name__ == "__main__":
    # 设置入口页 URL
    # https://news.sina.com.cn/  https://news.163.com/
    root_url = "https://github.com/search?l=Python&o=desc&p=1&q=slackbot&s=stars&type=Repositories"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
