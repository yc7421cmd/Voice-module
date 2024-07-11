import jieba
from transformers import BertTokenizer, BertModel
import torch
import re
chinese_number_map = {'零': 0, '一': 1, '二': 2,'两':2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
                     '百': 100, '千': 1000, '万': 10000, '亿': 100000000}

def chinese_to_int(chinese_number, l):
    result = 0
    tmp_num = 0
    if(l == 0):
        for i in range(len(chinese_number)):
            val = chinese_number_map.get(chinese_number[i], None)
            if(val >= 10):
                if(tmp_num == 0):
                    tmp_num = 1
                tmp_num *= val
                result += tmp_num
                tmp_num = 0
            else:
                tmp_num = val
            if(i == len(chinese_number) - 1):
                result += tmp_num
        # print(val,result)
    else:
        print(len(chinese_number))
        for i in range(len(chinese_number)):
            val = chinese_number_map.get(chinese_number[i], None)
            tmp_num *= 10
            tmp_num += val           
        result = tmp_num * 10**(-l)
    return result


def gene(tokens):
    store_list = [0.6, 0, 1]
    for i in range(len(tokens)):
        if("前走" in tokens[i]):
            store_list[1] = 1
            break
        elif("后走" in tokens[i]):
            store_list[1] = 2
            break
        elif("左走" in tokens[i]):
            store_list[1] = 3
            break
        elif("右走" in tokens[i]):
            store_list[1] = 4
            break
        elif("左转" in tokens[i]):
            store_list[1] = 5
            break
        elif("右转" in tokens[i]):
            store_list[1] = 6
            break
        elif("跳舞" in tokens[i]):
            store_list[1] = 7
            break
        elif("坐下" in tokens[i]):
            store_list[1] = 8
            break
        elif("站起" in tokens[i]):
            store_list[1] = 9
            break
        elif("比心" in tokens[i]):
            store_list[1] = 10
            break
        elif("趴下" in tokens[i]):
            store_list[1] = 11
            break
        elif("站立" in tokens[i]):
            store_list[1] = 12
            break
    return store_list

def extract_keywords(text):
    # 分词
    
    tokens = jieba.lcut(text)
    # print(tokens)
    store_list = gene(tokens)
    # 在token之间加入[CLS]和[SEP]标记
    # numbers = re.findall(r'\d+', sentence)数学数字
    chinese_numbers = re.findall("[零一二两三四五六七八九十百千万亿]+", text)
    l = 0
    tmp = []
    if(len(chinese_numbers) == 0):
        return store_list
    if(len(chinese_numbers) == 1):
        number = chinese_to_int(chinese_numbers[0], 0)
        store_list[2] = number
        return store_list
    # 获得速度和时间
    if(chinese_numbers[0] == '零'):
        l = len(chinese_numbers[1])
    for i in range(len(chinese_numbers)):
        if(l != 0 and i == 0):
            continue
        number = chinese_to_int(chinese_numbers[i], l)
        l = 0
        tmp.append(number)
    store_list[0] = tmp[0]
    store_list[2] = tmp[1]
    if(store_list[0] > 0.6): # 限制最大速度为0.6
        store_list[0] = 0.6
    

    return store_list

# # 示例文本
# text = "你好，趴下"


# # 提取关键信息
# keywords = extract_keywords(text)
# print(keywords)