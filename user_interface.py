# File: user_interface.py
# Author: Du Jiajie
# Function: 用户操作界面

import json
from tkinter import *
from login import *
from search import *
from add import *
from delete import *

# 用户操作界面类
class UserInterface:
    # 初始化用户操作界面
    def __init__(self, master, user_name, user_dict):
        # 控件
        self.master = master
        self.user_dict = user_dict
        self.user_name = user_name
        self.button_add = Button(self.master, text='添加物品', command=self.add_item)
        self.button_search = Button(self.master, text='查找物品', command=self.search_item)
        self.button_delete = Button(self.master, text='删除物品', command=self.delete_item)
        self.button_back = Button(self.master, text='退出登录', command=self.quit)

        # 初始化事件
        self.align_ui() # 排列UI控件
        self.master.protocol("WM_DELETE_WINDOW", lambda: exit(0)) # 关闭此窗口退出程序

    # 排列UI中的控件
    def align_ui(self):
        self.master.title("用户界面")
        self.master.geometry('340x150')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='姓名：' + self.user_dict['name']).grid(row=0, column=0, sticky=W, columnspan=4)
        Label(self.master, text='住址：' + self.user_dict['address']).grid(row=1, column=0, sticky=W, columnspan=4)
        Label(self.master, text='联系方式：' + self.user_dict['tel']).grid(row=2, column=0, sticky=W, columnspan=4)
        Label(self.master, text='正式用户：' + ('是' if self.user_dict['formal_user'] else '否')).grid(row=3, column=0, sticky=W, columnspan=4)
        self.button_add.grid(row=5, column=1)
        self.button_search.grid(row=5, column=2)
        self.button_delete.grid(row=5, column=3)
        self.button_back.grid(row=5, column=4)

    # 添加物品
    def add_item(self):
        self.master.withdraw()
        Add(Toplevel(), self.user_dict, self.master)

    # 查找物品
    def search_item(self):
        self.master.withdraw()
        Search(Toplevel(), self.master)

    # 删除物品
    def delete_item(self):
        self.master.withdraw()
        
        Delete(Toplevel(), self.user_name, self.master)

    # 获取物品字典
    def get_item_dict(self):
        with open('./data/item.json', 'r', encoding='utf-8') as f:
            self.item_dict = json.loads(f.readline())

    #退出登录
    def quit(self):
        exit(0)

        