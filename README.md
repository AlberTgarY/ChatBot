# ChatBot Demo
Welcome!<br>
This repository is currently consists of a git crawler and a python code inspector.<br>
## crawler
If you want to start the crawler, please run **crawler/crawler.py**.<br>
For python, please create folder **./ChatBot/py**. For JavaScript, please create folder **./ChatBot/js**.<br> 
Otherwise the crawler will have no location to save its data. You can always change the name of these folders in cfg.ini.<br>
The cralwer has auto logging module, it will log the history of code crawling and save the .log file to folder **./Log/** (auto created if doesnt exist)<br>
## code checker
If you want to start the code checker, please run **code_checker.py** and make sure you have some files in folder **./js/**  or  **./py/**.<br>
The code checker has auto logging module, it will log the history of the scan and save the .log file to folder **./Inspec_Log/** (auto created if doesnt exist).<br>
## cfg
**cfg.ini** is the config file for crawler, **page** refers to the page number of github that you want to search for.<br>
**num_of_branch_in_current** refers to how many repositories you want to get from single page (maximum = 10)<br>
**num_page** is currently useless, it refers to how many pages do you want crawler to search in a row. If you search too many pages at once, there will be timeout or anti-crawling issue which will force the program to terminate. Hence I recommand you to search the page one by one, or you can run crawler.craw for many times.<br>


