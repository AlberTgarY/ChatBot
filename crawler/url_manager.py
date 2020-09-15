# coding=utf-8

# URL 管理器
class UrlManager(object):

    # 初始化新旧 URL 管理器为 set()
    def __init__(self):

        self.new_urls = set()
        self.old_urls = set()

    # 添加一个 URL
    def add_new_url(self, url):

        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 添加一堆 URL
    def add_new_urls(self, urls):

        if urls is None or len(urls) == 0:
            return

        for url in urls:
            self.add_new_url(url)



    # URL 管理器内是否存在 URL
    def has_new_url(self):

        return len(self.new_urls) != 0

    # 从 URL 管理器内获取一个 URL
    def get_new_url(self):

        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url