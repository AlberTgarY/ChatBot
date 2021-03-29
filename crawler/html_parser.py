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
TEMP_path = config.get("path", "temp_path_crawler")
counter = config.get("num", "num_of_branch_in_current")
page = config.get("num", "page")
logger = get_log()


def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu  # 太小则重置为平均值
    time.sleep(secs)


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


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

                # input code
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

    def recursive_search_file(self, url, file_dict):
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
                logger.debug("Searching for: " + target_url)
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
                        logger.debug("Found File: " + str(key))
                        print("Found File: " + str(key))
                else:
                    self.recursive_search_file(target_url, file_dict)
        except Exception as e:
            print("Got a Error in method [recursive_search_file]: " +str(e))
        return file_dict

    # get the files
    def get_new_data(self, soup):
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
            print(url)
            too_large = ["https://github.com/Cog-Creators/Red-DiscordBot", "https://github.com/msdevstep/subroute.io"
                         ,"https://github.com/MadisonReed/oncall-slackbot", "https://github.com/dasistHYOJIN/martin-slackbot",
                         "https://github.com/prateeksan/code_review_slackbot","https://github.com/lambtron/slack-channel-fomo-bot",
                         "https://github.com/project-digital/slackbot_onboard", "https://github.com/cowie/scrub-sfdc-slackbot",
                         "https://github.com/jumbosushi/Go-Outside", "https://github.com/doublea1186/slackbot",
                         "https://github.com/RodrigoBP99/SlackBot","https://github.com/Semior001/mtdbot",
                         "https://github.com/tbremm/slack_foaas","https://github.com/ferrari3000/thanos_slackbot",
                         "https://github.com/kris927b/Stan-SlackBot","https://github.com/akshayjoyinfo/dx-tracking-slackbot",
                         "https://github.com/didinj/nodejs-slackbot-karmabot-example","https://github.com/marcusbass323/slackjokebot",
                         "https://github.com/delacruz1/Drizzy-Bot","https://github.com/thyrlian/Doraemon",
                         "https://github.com/kmaida/speakerbot","https://github.com/didinj/nodejs-mongodb-slackbot-example",
                         "https://github.com/prav10194/botkit-slackbot","https://github.com/nobanusa/Airport-Slackbot"]
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

        # new_urls = self._get_new_urls(page_url, soup)
        res_data = self.get_new_data(soup)
        print(res_data)
        return res_data
