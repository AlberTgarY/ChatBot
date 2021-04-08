# coding=utf-8
from bs4 import BeautifulSoup
import json
import os
# HTML Parser
import html_downloader
import configparser
from Logger import get_log
import time
import random

type_list = ["py", "js"]
config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
TEMP_path = config.get("path", "temp_path_JavaScript")
counter = config.get("num", "num_of_branch_in_current")
page = config.get("num", "page")
logger = get_log()

'''
This file is the HTMLParser, it recursively searches the whole repository and returns the .py or .js files only.
These files will be saved to a nested output folder(for python, it will be ./py, for JavaScript, it will be ./js) for
further analysis. You can also add more languages` file prefixes to extend the file type.
author: ZHAN YICHENG 03/04/2021
'''


# This method randomly sets the crawling time per file, which simulates the normal exploring(avoid anti-crawling).
def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)


# This method gets the keys in a dictionary(reverse the dict)
def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


# This method creates the nested folders structure to save the code files.
# For example: the files in repository: 'Albert/slackbot' in page 15 will be saved to a folder called:
# 'Albert-slackbot'. And this folder will be saved to a folder called '15'.
class HtmlParser(object):
    @staticmethod
    def fetch_code(file_dict):
        try:
            downloader = html_downloader.HtmlDownloader()

            for urls_dict in file_dict.values():
                folder_name = get_keys(file_dict, urls_dict)

                # find the branch name
                reversed_url = "".join(reversed(folder_name[0]))
                reversed_name = reversed_url.split("/")
                branch = "".join(reversed(reversed_name[0]))
                name = "".join(reversed(reversed_name[1]))

                # create dir for current page
                folder_page_path = TEMP_path + page + '/'
                if not os.path.exists(folder_page_path):
                    os.mkdir(folder_page_path)

                # create dir for current branch
                folder_branch_path = folder_page_path + name + "-" + branch + '/'
                if not os.path.exists(folder_branch_path):
                    os.mkdir(folder_branch_path)
                    logger.debug("Create dir: " + folder_branch_path)

                # use BeautifulSoup to search code
                for url in urls_dict.values():
                    random_sleep()
                    html_cont = downloader.download(url)
                    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
                    code = soup.find_all(name="td", attrs={"class": "blob-code blob-code-inner js-file-line"})

                    file_name = get_keys(urls_dict, url)
                    path = folder_branch_path + file_name[0]

                    logger.info("Writing file to: " + path)

                    if not os.path.exists(path):
                        with open(path, "w", encoding="utf-8") as f:
                            logger.debug(str(f))
                            print(f)

                    with open(path, "a", encoding="utf-8") as f:
                        for row in code:
                            f.write(row.text+"\n")

        except Exception as e:
            logger.debug("Got a Error in method [fetch_code]: " + str(e))
            print("Got a Error in method [fetch_code]: " + str(e))

# This method will search GitHub repository page recursively.
# Only .py or .js files will be recorded.
    def recursive_search_file(self, url, file_dict):
        try:
            html_cont = self.downloader.download(url)
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
            # search for file and folder
            news_content = soup.find_all(name="span",
                                         attrs={"class": "css-truncate css-truncate-target d-block width-fit"})
            for span in news_content:
                found = False
                # the url of current folder or file
                target_url = "https://github.com" + span.a['href']
                filename = span.a.string

                print("Searching for: " + target_url)
                logger.debug("Searching for: " + target_url)
                # separate file name and suffix
                revert = ''.join(reversed(filename))
                suffix_index = revert.find('.')
                suffix = ''.join(reversed(revert[0: suffix_index]))
                prefix = ''.join(reversed(revert[suffix_index:]))#

                # the suffix is '.py' or '.js'
                if suffix_index != -1:
                    found = True
                if self.has_key(found, prefix, suffix, file_dict):
                        key = self.has_key(found, prefix, suffix, file_dict)
                        tempdict = {key: str(target_url)}
                        # the crawler uses Dict to store the repository data.
                        file_dict.update(tempdict)
                        logger.debug("Found File: " + str(key))
                        print("Found File: " + str(key))
                else:
                    self.recursive_search_file(target_url, file_dict)
        except Exception as e:
            print("Got a Error in method [recursive_search_file]: " +str(e))
        return file_dict

# This method will check if current file is a python or JavaScript file.
# If so, it will create a .txt file and record the code into it.
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

# This method will download and scan the GitHub search page. Every page has 10 repositories, the crawler will find
# their url links and browse them separately.
    def get_new_data(self, soup):
        self.downloader = html_downloader.HtmlDownloader()
        res_data = {}
        # The content in [f4 text-normal][data-hydro-click] is the repository link.
        summary_node = soup.find_all(name="div", attrs={"class": "f4 text-normal"})
        count = int(counter)
        for n in summary_node:
            file_dict = {}
            attr_dict = json.loads(n.a['data-hydro-click'])
            url = attr_dict['payload']['result']['url']
            count = count - 1
            print(url)
            # these 3 repositories are too large to crawl.
            too_large = ["https://github.com/Cog-Creators/Red-DiscordBot", "https://github.com/msdevstep/subroute.io"
                         ,"https://github.com/kmaida/speakerbot"]
            if url in too_large:
                print("url: "+url+" is too large ")
                get_log().info("url: "+url+" is too large ")
                continue
            if count >= 0:
                file_dict = self.recursive_search_file(url, file_dict)
                temp_dict = {url: file_dict}
                res_data.update(temp_dict)
            else:
                break
        return res_data

# parse the html code and return the result
    def parse(self, page_url, html_cont):

        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        res_data = self.get_new_data(soup)
        print(res_data)
        return res_data
