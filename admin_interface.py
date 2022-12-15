# File: login.py
# Author: Du Jiajie
# Function: 管理员界面

from tkinter import *

# 管理员操作界面类
class AdminInterface:
    def __init__(self, master, admin_dict):
        pass
    # 控件
        self.master = master
        self.admin_dict = admin_dict
        self.button_accept = Button(self.master, text='批准正式用户申请', command=self.accept)
        self.button_change = Button(self.master, text='修改或删除物品类型', command=self.change_type)
        self.button_back = Button(self.master, text='退出登录', command=self.back)
        # 初始化事件
        self.align_ui()  # 排列UI控件
        # 注意修改！
        self.master.protocol("WM_DELETE_WINDOW", lambda x=0: exit(x))  # 关闭此窗口退出程序

    # 排列UI中的控件
    def align_ui(self):
        self.master.title("管理员界面")
        self.master.geometry('300x100')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='管理操作菜单', font=10).grid(row=0, column=0, sticky=W, columnspan=2)
        self.button_accept.grid(row=1, column=0)
        self.button_change.grid(row=1, column=1)
        self.button_back.grid(row=1, column=2)

    def accept(self):
        pass

    def change_type(self):
        pass

    #退出登录，返回登录界面
    def back(self):
        self.master.destroy()
