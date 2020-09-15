# coding=utf-8

from urllib import parse
from bs4 import BeautifulSoup
import json
import os

# HTML 解析器
import html_downloader
import configparser

type_list = ["py"]
config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
TEMP_path = config.get("path", "temp_path_crawler")
counter = config.get("num", "num_of_branch_in_current")


def get_keys(d, value):
    return [k for k,v in d.items() if v == value]


def get_content(news_content):
    # get the news info and  make it a string
    temp = ''
    for new in news_content:
        temp = temp + new.get_text().replace('\n','')
    if temp != '':
        return temp
    raise ValueError('content is None')


class HtmlParser(object):
    @staticmethod
    def fetch_python_code(file_dict):

        downloader = html_downloader.HtmlDownloader()

        for urls_dict in file_dict.values():
            folder_name = get_keys(file_dict, urls_dict)
            # find the branch name
            reversed_url = "".join(reversed(folder_name[0]))
            reversed_name = reversed_url.split("/")
            branch = "".join(reversed(reversed_name[0]))
            name = "".join(reversed(reversed_name[1]))
            # create dir for current branch
            folder_path = TEMP_path + name + "-" + branch + '/'
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            # input code
            for url in urls_dict.values():

                html_cont = downloader.download(url)
                soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
                code = soup.find_all(name="td", attrs={"class": "blob-code blob-code-inner js-file-line"})

                file_name = get_keys(urls_dict, url)
                path = folder_path + file_name[0]

                if not os.path.exists(path):
                    with open(path, "w", encoding="utf-8") as f:
                        print(f)

                with open(path, "a", encoding="utf-8") as f:
                    for row in code:
                        f.write(row.text+"\n")

    @staticmethod
    def has_key(found, prefix, suffix, file_dict):
        if found:
            if not (suffix in type_list):
                return
            new_key = prefix[0:len(prefix)-1] + "." + "txt"
            count = 0
            while new_key in file_dict.keys():
                count = count + 1
                new_key = prefix[0:len(prefix)-1] + str(count) + "." + "txt"
            return new_key
        else:
            return

    def recursive_search_python_file(self, url, file_dict):
        try:
            html_cont = self.downloader.download(url)
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
            # search for content
            news_content = soup.find_all(name="span",
                                         attrs={"class": "css-truncate css-truncate-target d-block width-fit"})
            for span in news_content:
                found = False
                target_url = "https://github.com" + span.a['href']
                filename = span.a.string

                print("Searching for: " + target_url)
                # separate file name and suffix
                revert = ''.join(reversed(filename))
                suffix_index = revert.find('.')
                suffix = ''.join(reversed(revert[0: suffix_index]))
                prefix = ''.join(reversed(revert[suffix_index:]))

                if suffix_index != -1:
                    found = True
                if self.has_key(found, prefix, suffix, file_dict):
                        key = self.has_key(found, prefix, suffix, file_dict)
                        tempdict = {key: str(target_url)}
                        file_dict.update(tempdict)
                        print("find a python file")
                else:
                    self.recursive_search_python_file(target_url, file_dict)
        except Exception as e:
            print(e)
        return file_dict

    @staticmethod
    # Find the all indexes at the first search
    def _get_all_index(page_url, soup):

        new_urls = set()
        # 查找页面的 URL
        links = soup.find('div', class_="main-nav").find_all('a')
        for link in links:
            new_url = link['href']
            # 将 new_url 按照 page_url 的格式拼接
            new_url_join = parse.urljoin(page_url, new_url)
            new_urls.add(new_url_join)
        return new_urls


    # 获取页面中想要的 DATA
    def _get_new_data(self, soup):
        self.downloader = html_downloader.HtmlDownloader()
        res_data = {}
        # contain all news in current page
        # search for news link
        summary_node = soup.find_all(name="div", attrs={"class": "f4 text-normal"})
        # count = len(summary_node)
        count = int(counter)
        for n in summary_node:
            file_dict = {}
            attr_dict = json.loads(n.a['data-hydro-click'])
            url = attr_dict['payload']['result']['url']
            count = count - 1
            if count >= 0:
                file_dict = self.recursive_search_python_file(url, file_dict)
                temp_dict = {url: file_dict}
                res_data.update(temp_dict)
            else:
                break
        return res_data

    # 解析网页获取 new_urls 与 new_data
    def parse(self, page_url, html_cont):

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        # new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(soup)
        print(new_data)
        return new_data
