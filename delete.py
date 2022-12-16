# File: search.py
# Author: Du Jiajie
# Function: 删除物品界面

from tkinter import *
from tkinter import messagebox
import json
from user_interface import *

# 输入窗口类，用于查找和添加物品


class Delete:
    def __init__(self, master, user_name, user_interface):
        # master: 窗体 input_info: 需要输入的信息名称
        # 变量
        self.user_interface = user_interface
        self.user_name = user_name
        self.result_cnt = 0  # 找到的结果数
        # 控件
        self.master = master
        # 选择类型 滚动条
        self.button_delete = Button(self.master, text='删除', command=self.delete)
        self.button_back = Button(
            self.master, text='返回用户界面', command=self.back)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.back())  # 关闭此窗口返回用户界面
        self.scroll_result = Scrollbar(self.master)
        self.list_result = Listbox(
            self.master, width=40, height=4, yscrollcommand=self.scroll_result.set)
        self.scroll_result.config(command=self.list_result.yview)
        self.list_result.bind('<Double-Button-1>', lambda x=0: self.show_detail())
        self.label_detail = Label(self.master, text='', wraplength=300)
        # 排列UI控件
        self.align_ui()
        # 获取用户和物品的信息
        self.get_userdata()
        self.get_item()
        self.get_type()
        self.load() # 加载可删除列表

    def align_ui(self):
        self.master.title("查找物品")
        self.master.geometry('340x400')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='选择要删除的物品：').grid(row=0, column=0)
        
        self.button_delete.grid(row=3, column=2)
        self.button_back.grid(row=3, column=3)
        self.scroll_result.grid(row=5, column=5, rowspan=3)
        self.list_result.grid(row=5, column=0, rowspan=3, columnspan=5)
        self.label_detail.grid(row=9, column=0, rowspan=5, columnspan=10)

    # 获取物品类型
    def get_type(self):
        with open('./data/type.json', 'r', encoding='utf-8') as f:
            self.type_dict = json.loads(f.readline())

    # 获取物品列表
    def get_item(self):
        with open('./data/item.json', 'r', encoding='utf-8') as f:
            self.item_dict = json.loads(f.readline())

    def load(self):
        self.list_result.delete(0, END)  # 清空搜索结果列表

        for item in self.item_dict.keys():
            if self.user_name == self.item_dict[item]['owner']:
                self.list_result.insert(END, item + ':' + self.item_dict[item]['name'])
        

    # 获取用户信息，以获取物品所有者的联系方式和姓名
    def get_userdata(self):
        with open('./account/user.json', 'r', encoding='utf-8') as f:
            self.user_dict = json.loads(f.readline())

    # 获取物品类型
    def get_type(self):
        with open('./data/type.json', 'r', encoding='utf-8') as f:
            self.type_dict = json.loads(f.readline())

    # 显示物品的详细信息
    def show_detail(self):
        text = ''
        item_result = self.list_result.get(self.list_result.curselection())  # 获得当前选中的记录
        index = item_result.split(':')[0]
        # 显示物品简介
        text = item_result.split(':')[1] + '\n' +\
            '类型：' + self.item_dict[index]['type'] + '\n' +\
            '简介：' + self.item_dict[index]['intro'] + '\n'
        self.item_dict[index]

        attribution_dict = self.item_dict[index]['attributions']  # 不同种类物品特有属性
        # 显示物品特有属性
        for attribution in self.type_dict[self.item_dict[index]['type']]:
            text = text + attribution + "："
            try:
                text = text + attribution_dict[attribution] + '\n'
            except:
                text = text + '\n'
        owner_account = self.item_dict[index]['owner']
        # 显示物主信息
        text = text + '物主姓名：' + self.user_dict[owner_account]['name'] + '（用户名：' + owner_account + '）\n' +\
            '地址：' + self.user_dict[owner_account]['address'] + '\n' +\
            '联系方式：' + self.user_dict[owner_account]['tel']
        self.label_detail.config(text=text)

    def delete(self):
        try:
            item_delete = self.list_result.get(
                self.list_result.curselection())  # 获得当前选中的类型
        except:
            messagebox.showwarning('错误', '请选择要删除的物品！')
            return
        index = item_delete.split(':')[0]
        del self.item_dict[index]
        self.save_item()
        self.load()

    # 保存物品信息
    def save_item(self):
        with open('./data/item.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.user_dict))

    # 返回用户界面
    def back(self):
        self.master.withdraw()
        self.user_interface.deiconify()

