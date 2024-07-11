from openai import OpenAI
from extract import *
import jieba
client = OpenAI(
    api_key="sk-4901efb79ee2dd26fbe4c5c3b1052bb4",
    base_url="https://api.atomecho.cn/v1",
)

def check(tokens):
  flag = 0
  for i in range(len(tokens)):
    if("走" in tokens[i]):
      flag += 1
      return flag
    if("转" in tokens[i]):
      flag += 1
      return flag
  return flag

def llm(input_text):
  # input_text = input("请输入：")
  # if(input_text == "0"):
  #   break
  tokens = jieba.lcut(input_text)
  flag = check(tokens)
  if(flag == 0):
    store_list = gene(tokens)
    return store_list
  else:
    content1 = "我需要你进行格式化输出，案例如下：当我输入“向前走五秒”时，请输出[0.6,“向前走”,5];当我输入“以0.6m/s的速度向前走3秒 ”时，输出[0.6,“向前走”,3]；输入为:请向前走3秒,输出为:[0.6,向前走,3]。如果输入为：请以一米每秒的速度向后走三秒，输出为：[1,向后走,3]。当我输入向左转2秒的时候,输出应该是:[0.6,向左转,2]. \
    当我输入为以2米每秒的速度向右转2秒的时候,输出为[2,向右转,2],当输入为向右转4秒的时候,输出为[0.6,向右转,4]。当输入为以0.3米每秒的速度向左转，输出为[0.3,向左转,3],当我的输入为以0.3米每秒的速度向右转0.4秒时，输出为[0.3,向右转,0.4]。当我的输入为向左转，输出为:[0.6,向左转,3].如果我的方向中含有向前的意思，则输出的运动状态（第二个元素）应该为向前走。"
    content2 = "你的输出应该是一个包含了三个元素的列表(list),其中第一个元素代表速度,如果未给出,则默认为0.6;第二个元素代表运动的方向,例如'向前走'或是'向后走';第三个元素代表运动的时间,如果未给出,则默认为3秒。"
    content3 = "那么当我输入为："
    content4 = "你的输出应该是什么?"
    content = content1 + content2 + content3 + input_text + content4

    completion = client.chat.completions.create(
      model="Atom-13B-Chat",
      messages=[
        {"role": "user", "content": content}
      ],
      temperature=0.3,
    )
    # print(completion.choices[0].message.content)
    pos_l = completion.choices[0].message.content.find("[")
    pos_r = completion.choices[0].message.content.find("]")
    # print(completion.choices[0].message.content.find("["))
    # print("  ")
    store_infor = completion.choices[0].message.content[pos_l + 1 : pos_r]
    store_list = store_infor.split(",")
    store_list[1] = store_list[1][1:-1]

    store_list[0] = float(store_list[0])
    store_list[2] = float(store_list[2])
    # print(store_list)
    if("前走" in store_list[1]):
        store_list[1] = 1
    elif("后走" in store_list[1]):
        store_list[1] = 2
    elif("左走" in store_list[1]):
        store_list[1] = 3
    elif("右走" in store_list[1]):
        store_list[1] = 4
    elif("左转" in store_list[1]):
        store_list[1] = 5
    elif("右转" in store_list[1]):
        store_list[1] = 6

    return store_list
