import os
import configparser
import shutil
import re
from openpyxl import load_workbook
import pandas as pd

# read config file
config = configparser.RawConfigParser()
config.read("./cfg/cfg.ini")
TEMP_path = config.get("path", "temp_path")
TARGET_path = config.get("path", "target_path")
XLSX_path = config.get("path", "name_xlsx")

type_list = [".py"]
file_dict = {}

# create folder if doesnt exist
if not os.path.exists(TEMP_path):
    os.mkdir(config.get("path", "temp_path"))


# looking for scope
def inspection(scope_dict):
    data = pd.read_excel(str(XLSX_path))
    scopes = list(scope_dict.keys())
    files = os.listdir(TEMP_path)
    for file in files:
        for line in open(TEMP_path+file):
            # search for scope category first
            for scope in scopes:
                if (scope in line) or (cap(scope) in line)or (scope.upper() in line):

                    sc = 0
                    sc_cap = 0
                    sc_upp = 0

                    if scope in line:
                        sc = line.find(scope)
                    if cap(scope) in line:
                        sc_cap = line.find(cap(scope))
                    if scope.upper() in line:
                        sc_upp = line.find(scope.upper())

                    scope_sorted_list = [sc, sc_cap, sc_upp]
                    scope_sorted_list.sort(reverse=True)
                    scope_string_index = scope_sorted_list[0]
                    scope_string_end_index = scope_string_index + len(scope)

                    # once locate category, looking for method of it
                    methods = scope_dict[scope]
                    # rest of the line of code after the location of scope.
                    temp = line[scope_string_index:]

                    before_scope_string_index = 0
                    before_scope_string_end_index = scope_string_end_index-scope_string_index
                    # print("总权限名: " + str(before_scope_string_index))
                    # print("总权限名截至: " + str(before_scope_string_end_index))
                    first = True
                    for method in methods:
                        for sub_method in method:
                            # print("当前搜索权限名: "+sub_method)
                            cur_temp, cur_scope_string_index, cur_scope_string_end_index = inspect_method(data, scope, method, sub_method, temp, before_scope_string_index, before_scope_string_end_index)
                            first = False
                            if (cur_temp and cur_scope_string_index and cur_scope_string_end_index):
                                # print("----------------next_________")
                                # print(sub_method)
                                # print("temp: " + str(temp))
                                # print("curtemp: "+ str(cur_temp))
                                # print("cur_scope_string_index: "+str(cur_scope_string_index))
                                # print("cur_scope_string_end_index: " + str(cur_scope_string_end_index))
                                before_scope_string_index = cur_scope_string_index
                                before_scope_string_end_index = cur_scope_string_end_index
                                temp = cur_temp
                            else:
                                # print("[未找到] break the loop")
                                # doesnt find the target method
                                break


def inspect_method( data, scope, method, first_method_name, temp, before_scope_string_index, before_scope_string_end_index):
    if (first_method_name in temp) or (cap(first_method_name) in temp) or (first_method_name.upper() in temp):
        tp = 0
        tp_cap = 0
        tp_upp = 0

        # print("当前文本: " + temp)
        if first_method_name in temp:
            tp = temp.find(first_method_name)
            # print("普通权限名: " + str(tp))
        if cap(first_method_name) in temp:
            tp_cap = temp.find(cap(first_method_name))
            # print("首字母大写权限名: " + str(tp_cap))
        if first_method_name.upper() in temp:
            tp_upp = temp.find(first_method_name.upper())
            # print("全大写权限名: " + str(tp_upp))

        method_sorted_list = [tp, tp_cap, tp_upp]

        method_sorted_list.sort(reverse=True)
        method_string_index = method_sorted_list[0]

        sub_temp = temp[method_string_index:]
        size = len(method)
        # print("当前遍历权限列表: "+str(method))
        # print("切分后文本: " + sub_temp)
        # method_string_end_index = method_string_index + before_scope_string_index + len(first_method_name)
        method_string_end_index = method_string_index + len(first_method_name)
        # print("method_string_end_index = "+str(method_string_end_index)+" = "+str(method_string_index)+" + "+str(len(first_method_name)))
        # print("before_scope_string_end_index: "+str(before_scope_string_end_index))
        # print("current method_string_index: "+str(method_string_index))

        distance = (method_string_index - before_scope_string_end_index) >= 0 and (
                    method_string_index - before_scope_string_end_index) <= 1
        # print("size: "+str(size))
        # print("distance: "+ str(distance))
        if size == 1 and distance:
            scopes_requirement = data[data.name == str(scope + "." + method[0])].scope
            scope_full_name = scope + "." + method[0]
            print("Found the scope: ")
            print(scope_full_name + ": ")
            print(scopes_requirement)
            print("\n")
        elif size > 1 and distance:
            count = 1
            scope_full_name = scope + "." + method[0]
            for sub_method_name in method[1:]:
                # print("sub_method_name: "+sub_method_name)
                # print("sub_temp: "+sub_temp)
                if (sub_method_name in sub_temp) or (sub_method_name.capitalize() in sub_temp) or (
                        sub_method_name.upper() in sub_temp):
                    scope_full_name = scope_full_name + "." + sub_method_name
                    count = count + 1
            if count == size:
                scopes_requirement = data[data.name == str(scope_full_name)].scope
                print("Found the scope: ")
                print(scope_full_name + ": ")
                print(scopes_requirement)
                print("\n")
            else:
                # print("[没找到]")
                return None, None, None
        else:
            return None, None, None
        return sub_temp, method_string_index, method_string_end_index
    else:
        return None, None, None


# build a binary tree according to list
def scope_dict() -> dict:
    method_dict = {}
    workbook = load_workbook(str(XLSX_path))
    booksheet = workbook.active
    for i in range(2, booksheet.max_row+1):
        method = booksheet.cell(i, 1).value
        key = method.split(".")[0]
        if key in method_dict.keys():
            methods_list = list(method.split(".")[1:])
            methods_list = reconstruct_list(methods_list)
            method_dict[key].append(methods_list)
        else:
            methods_list = list(method.split(".")[1:])
            methods_list = reconstruct_list(methods_list)
            temp_dict = {str(key): [methods_list]}
            method_dict.update(temp_dict)
    return method_dict


def reconstruct_list(litarable_list):
    if_split = False
    count = True
    for element_key in litarable_list:
        if count:
            words, valid = find_cap(element_key)
            if valid:
                remove_index = litarable_list.index(element_key)
                litarable_list.pop(remove_index)
                index = remove_index
                for word in words:
                    litarable_list.insert(index, word)
                    index = index + 1
                count = False

    return litarable_list


def copy(file_dict):
    # copy files
    for key,value in zip(file_dict.keys(), file_dict.values()):
        shutil.copy(value, TEMP_path+key)
    print("Finished search and copy")


def search(path, file_dict):
    # search for .py(currently)files
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            search(file_path, file_dict)
        else:
            #
            if not has_key(file, file_dict):
                continue
            else:
                temp_dict = {str(has_key(file, file_dict)): str(file_path)}
                file_dict.update(temp_dict)
    return file_dict


def has_key(key, file_dict):
    (filename, extension) = os.path.splitext(key)
    if not extension in type_list:
        return
    new_key = filename + ".txt"
    count = 0
    while new_key in file_dict.keys():
        count = count+1
        new_key = filename+str(count)+".txt"
    return new_key



def cap(text):
    text = text[0].upper()+text[1:]
    return text


def find_cap(text):
    # find if theres capital letter
    cap_num = re.findall(r'[A-Z]', text)
    if len(cap_num) > 0:
        first_cap_index = text.find(cap_num[0])
        lower_case_word = text[0:first_cap_index]
        caplist = re.findall(r'[A-Z](?:[A-Z]*(?![a-z])|[a-z]*)', text)
        caplist.insert(0, lower_case_word)
        return caplist, True
    return None, False


if __name__ == "__main__":
    print()
    scope_dict = scope_dict()
    inspection(scope_dict)
    # file_dict = search(TARGET_path, file_dict)
    # copy(file_dict)
