import os
import configparser
from util_methods import cap, find_index
from util_methods import scope_dict as gen_scopes
import pandas as pd
from Plotter import Plot
from inspec_Logger import get_log


# read config file
config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
TEMP_path = config.get("path", "temp_path_JavaScript")
TARGET_path = config.get("path", "target_path")
XLSX_path = config.get("path", "name_xlsx")
logger = get_log()

# init temp dictionaries for code checker

file_dict = {}
output_dict = {}
scope_dict = {}

# statistical data
Find = False
Total_Files = 0
Total_Lines = 0
Total_Repo = 0
Empty_Repo = 0
No_Result_Repo = 0

# create folder if doesnt exist
if not os.path.exists(TEMP_path):
    os.mkdir(config.get("path", "temp_path"))

'''
This file is the main module of the CodeChecker, it search code files recursively to find the malicious scopes.
It also generates the statistical diagram to reveal the overall condition of the scopes usage.
author: ZHAN YICHENG 03/04/2021
'''


class CodeChecker(object):

    # This method is the core method.
    # the whole searching process is separated to two parts:
    # the first one is searching for the first subname of the scope,
    # the second is searching for the rest part of the scopes.
    # this method is the former one.
    def inspect_keyword(self, scope_dict):
        global Find, No_Result_Repo, Total_Repo, Empty_Repo, Total_Files, Total_Lines
        data = pd.read_excel(str(XLSX_path))
        scopes = list(scope_dict.keys())
        pages = os.listdir(TEMP_path)
        # search page by page, branch by branch, page by page, line by line
        for page in pages:
            print("-------------------------------------------------------------page: " + page)
            branch_path = TEMP_path+page
            repositories = os.listdir(branch_path)
            for repo in repositories:
                temp_dict = {repo: []}
                output_dict.update(temp_dict)
                print("【branch】: " + repo)
                # create a empty folder for current repository
                files_path = TEMP_path+page+"/"+repo
                files = os.listdir(files_path)
                if len(files) == 0:
                    Empty_Repo += 1
                for file in files:
                    Total_Files += 1
                    Count_lines = 0
                    for line in open(TEMP_path+page+"/"+repo+"/"+file, encoding="utf-8"):
                        Total_Lines += 1
                        Count_lines += 1
                        # first, searching for the first subname of the method.
                        # For example: for 'chat.postMessage', the first subname is 'chat'.
                        for scope in scopes:
                            if (scope in line) or (cap(scope) in line)or (scope.upper() in line)or (scope.lower() in line):

                                sc, sc_cap, sc_upp, sc_low = find_index(scope, line)

                                scope_sorted_list = [sc, sc_cap, sc_upp, sc_low]
                                scope_sorted_list.sort(reverse=True)
                                scope_string_index = scope_sorted_list[0]
                                scope_string_end_index = scope_string_index + len(scope)

                                # check the xlsx database to see if this name exists.
                                sub_scopes = scope_dict[scope]

                                # calculate where does the current subname end.
                                temp = line[scope_string_index:]
                                before_scope_string_end_index = scope_string_end_index-scope_string_index

                                # Match the method one by one.
                                # if locates the first subname, starting searching for the rest.
                                for sub_scope in sub_scopes:
                                    for sub_scope_part in sub_scope:
                                        # record the index of current scope, renew the parameter for next recursion.
                                        cur_temp, \
                                        cur_scope_string_index, \
                                        cur_scope_string_end_index \
                                            = self.inspect_sub_scope(repo, data, scope, sub_scope, sub_scope_part, temp,
                                                                before_scope_string_end_index, output_dict, [file, Count_lines])

                                        if cur_temp and cur_scope_string_index and cur_scope_string_end_index:
                                            # If all three vars are not None,
                                            # replace the previous params by current ones.
                                            # It starts another round of recursion
                                            before_scope_string_end_index = cur_scope_string_end_index
                                            temp = cur_temp
                                        else:
                                            # Does not find current method in this line of code, break the loop.
                                            # Search for the next method
                                            break
                if not Find and len(files) != 0: No_Result_Repo += 1
                Total_Repo += 1
                Find = False

    # This method is the component of the method [inspect_keyword]
    # the whole searching process is separated to two parts:
    # the first one is searching for the first subname of the scope,
    # the second is searching for the rest part of the scopes.
    # this method is the latter one.
    def inspect_sub_scope(self, repo, data, scope, sub_scope, sub_scope_part,
                          temp, before_scope_string_end_index, output_dict, zipped):
        global Find
        if (sub_scope_part in temp) or (cap(sub_scope_part) in temp) or (sub_scope_part.upper() in temp)or (sub_scope_part.lower() in temp):
            tp, tp_cap, tp_upp, tp_low = find_index(sub_scope_part, temp)

            # sort the list, take the smallest value.
            method_sorted_list = [tp, tp_cap, tp_upp, tp_low]

            method_sorted_list.sort(reverse=True)
            method_string_index = method_sorted_list[0]

            sub_temp = temp[method_string_index:]
            size = len(sub_scope)
            # calculate current scope subname`s end index
            method_string_end_index = method_string_index + len(sub_scope_part)
            # check the distance
            distance = (method_string_index - before_scope_string_end_index) >= 0 and (
                        method_string_index - before_scope_string_end_index) <= 1

            if size == 1 and distance:
                # if size == 1, that means we find the entire API method, now we can print it out.
                scopes_requirement = data[data.name == str(scope + "." + sub_scope[0])].scope
                scope_full_name = scope + "." + sub_scope[0]
                self.output_scope(repo, scope_full_name, scopes_requirement, output_dict, zipped)
                Find = True
            elif size > 1 and distance:
                # if size > 1, that means we find the partial API method, we combine the strings and keep going.
                count = 1
                scope_full_name = scope + "." + sub_scope[0]
                for sub_method_name in sub_scope[1:]:
                    if (sub_method_name in sub_temp) or (sub_method_name.capitalize() in sub_temp) or (
                            sub_method_name.upper() in sub_temp or sub_method_name.lower() in sub_temp):
                        scope_full_name = scope_full_name + "." + sub_method_name
                        count = count + 1
                if count == size:
                    scopes_requirement = data[data.name == str(scope_full_name)].scope
                    self.output_scope(repo, scope_full_name, scopes_requirement, output_dict, zipped)
                    Find = True
                else:
                    # if this method returns 3 None, which means it failed finding a sub method name of current method
                    return None, None, None
            else:
                return None, None, None
            return sub_temp, method_string_index, method_string_end_index
        else:
            return None, None, None

    # output the scope if finds one
    @staticmethod
    def output_scope(branch, scope_full_name, scopes_requirement, output_dict, zipped):
        file, count = str(zipped[0]), str(zipped[1])
        print("Found the scope from: "+file)
        print(scope_full_name + ": ")
        print(scopes_requirement.tolist())
        print()
        logger.info("["+branch +"] "+"find scope: "+scope_full_name + " => "+str(scopes_requirement.tolist())+" from: "+file+" line "+count)
        scope_list = output_dict[branch]
        requirement_list = scopes_requirement.tolist()

        if requirement_list:
            temp_dict = {scope_full_name: requirement_list[0]}
        else:
            temp_dict = {scope_full_name: []}
        found = False

        if not scope_list:
            scope_list.append(temp_dict)
            output_dict[branch] = scope_list
        else:
            for scope in scope_list:
                if temp_dict == scope:
                    found = True
            if not found:
                scope_list.append(temp_dict)
                output_dict[branch] = scope_list


if __name__ == "__main__":

    logger.info("-------------------------------start parsing-------------------------------")
    # scope list
    scope_dict = gen_scopes()
    # inspection method
    checker = CodeChecker()
    checker.inspect_keyword(scope_dict)
    if XLSX_path == '../cfg/slackname.xlsx':
        print("Current API: Events API")
    else:
        print("Current API: WEB API")
    print("Parsed " + str(Total_Repo) + " branches in total.\n")
    print("There are " + str(Total_Files) + " files "+ str(Total_Lines)+" lines in total.\n")
    print("There are " + str(Empty_Repo) + " empty branches.\n")
    print("There are "+str(No_Result_Repo)+" branches are not been detected.\n")
    # plot the diagram
    Plotter = Plot()
    count_dict = Plotter.manipulate_data(output_dict)
    Plotter.plot(count_dict)

