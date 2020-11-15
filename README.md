# ChatBot Demo
Welcome!<br>
This repository is currently consists of a git crawler and a python code inspector.<br>
## crawler
If you want to start the crawler, please run **crawler/spider_man.py**.<br>
The cralwer has function of auto logging, it will log the history of code crawling and save the .log file to folder **./Log/** (auto created if doesnt exist)<br>
## inspector
If you want to start the inspector, please run **Inspection.py** and make sure you have some files in folder **./temp/** (auto created if doesnt exist).<br>
## cfg
**cfg.ini** is the config file for crawler, **page** refers to the page number of github that you want to search for.<br>
**num_of_branch_in_current** refers to how many repositories you want to get from single page (maximum = 10)<br>
**num_page** is currently useless, it refers to how many pages do you want crawler to search in a row. But if you search too many pages at once, there will be timeout or anti-crawling issue which will force the program to terminate. Hence I decide to search it one by one.<br>


