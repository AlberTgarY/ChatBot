'''
This file is the URL Manager. It stores the urls crawled from the crawler.
author: ZHAN YICHENG 03/04/2021
'''
class UrlManager(object):

    # init
    def __init__(self):

        self.new_urls = set()
        self.old_urls = set()

    # add a URL
    def add_new_url(self, url):

        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # add series of URL
    def add_new_urls(self, urls):

        if urls is None or len(urls) == 0:
            return

        for url in urls:
            self.add_new_url(url)

    # check if there`s new url
    def has_new_url(self):

        return len(self.new_urls) != 0

    # get a new url from the manager
    def get_new_url(self):

        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url