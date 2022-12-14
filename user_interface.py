# File: user_interface.py
# Author: Du Jiajie
# Function: 用户操作界面

import json
from tkinter import *

# 用户操作界面类
class UserInterface:
    # 初始化用户操作界面
    def __init__(self, master, user_dict):
        # 控件
        self.master = master
        self.user_dict = user_dict
        self.button_add = Button(self.master, text='添加物品')
        

        # 初始化事件
        self.align_ui() # 排列UI控件
        self.function_bind() # 绑定控件功能
        # 注意修改！
        self.master.protocol("WM_DELETE_WINDOW", lambda x=0: exit(x)) # 关闭此窗口退出程序

    # 排列UI中的控件
    def align_ui(self):
        self.master.title("用户界面")
        self.master.geometry('340x150')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='姓名：' + self.user_dict['name']).grid(row=0, column=0, sticky=W)
        Label(self.master, text='住址：' + self.user_dict['address']).grid(row=1, column=0, sticky=W)
        Label(self.master, text='联系方式：' + self.user_dict['tel']).grid(row=2, column=0, sticky=W)
        Label(self.master, text='正式用户：' + ('是' if self.user_dict['formal_user'] else '否')).grid(row=3, column=0, sticky=W)
        


    # 给各个控件绑定事件
    def function_bind(self):
        pass