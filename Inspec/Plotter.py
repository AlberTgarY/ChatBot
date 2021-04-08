import matplotlib.pyplot as plt
import numpy as np
import json
'''
This file is the Plotter of code checker.
It counts the number of the scopes usage and generates statistical diagrams.
author: ZHAN YICHENG 03/04/2021
'''

# 'conversation.history' will be translate to:
# 'channels:history', 'groups:history', 'im:history', 'mpim:history' as well.
very_dangerous = ['channels:history', 'groups:history', 'im:history', 'mpim:history']

# search for the dangerous scopes
def search_dangerous(branch_method):
    result = []
    temp = branch_method[1:len(branch_method)-1]
    if not ',' in temp:
        list = [temp]
    else:
        list = temp.split(',')
        n = 1
        for temp in list[1:len(list)]:
            list[n] = temp[1:len(temp)]
            n = n+1
    for name in list:
        temp_name = name[1:len(name)-1]
        if temp_name in very_dangerous:
            result.append(temp_name)
    return result


# sort the dict in descending order
def sort(count_dict):
    temp_list = []
    key_list =[]
    for key in count_dict.keys():
        num = count_dict[key]
        if num <= 7:
            temp = {key: count_dict[key]}
            key_list.append(key)
            temp_list.append(temp)
    for key in key_list:
        count_dict.pop(key)
    return count_dict, temp_list

# add text for the scope
def auto_text(rects, plt):
    for rect in rects:
        plt.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')

# Plot the bar diagram
class Plot(object):

    @staticmethod
    def manipulate_data(output_dict):
        count_dict = {}
        danger_dict = {}
        for key in output_dict.keys():
            for branch in output_dict[key]:
                for method in branch.keys():
                    result = search_dangerous(branch[method])
                    if result:
                        if not method in danger_dict.keys():
                            temp_dict = {key: result}
                            danger_dict.update(temp_dict)
                        else:
                            if len(result) > len(danger_dict[method]):
                                danger_dict[method] = result

                    if not method in count_dict.keys():
                        temp_dict = {method: 1}
                        count_dict.update(temp_dict)
                    else:
                        count_dict[method] = count_dict[method] + 1
        print("Danger branches: "+str(len(danger_dict))+"\n")
        print(danger_dict)
        print("\n")
        return count_dict


    @staticmethod
    def plot(count_dict):
        count_dict, temp_dict = sort(count_dict)
        count_dict = dict(sorted(count_dict.items(), key=lambda l: (l[1], l[0]),reverse=True))
        # print(dict(count_dict))
        print("\n")
        print(temp_dict)

        # Bar plot
        plt.figure(figsize=(50, 10), dpi=80)
        N = len(count_dict)

        values = list(count_dict.values())
        index = np.arange(N)
        width = 0.3
        rects = plt.bar(index, values, width, label="occur times", color="#87CEFA")
        auto_text(rects, plt)
        plt.xlabel('method')
        plt.ylabel('number of appearance')
        plt.title('Frequency of method')
        plt.xticks(index ,list(count_dict.keys()), rotation= 60)

        plt.legend(loc="upper right")
        plt.show()
