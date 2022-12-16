# File: accept_formal.py
# Author: Du Jiajie
# Function: 通过正式用户批准界面

from tkinter import *
from tkinter import messagebox
import json
from admin_interface import *

# 通过正式用户批准界面类
class Accept:
    def __init__(self, master, admin_interface):
        self.master = master
        self.admin_interface = admin_interface
        # 控件
        self.scroll_informal = Scrollbar(self.master) # 用于显示非正式用户
        self.list_informal = Listbox(self.master, width=40, height=4, yscrollcommand=self.scroll_informal.set)
        self.scroll_informal.config(command=self.list_informal.yview)
        self.button_accept = Button(self.master, text='通过申请', command=self.accept)
        self.button_back = Button(self.master, text='返回管理员界面', command=self.back)
        # 初始化事件
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.back())  # 关闭此窗口返回管理员界面
        self.align_ui() # 排列UI组件
        self.get_userdata() # 获取用户信息
        self.load_inforaml_user() # 加载非正式用户列表

    # 排列UI组件
    def align_ui(self):
        self.master.title('批准正式用户申请')
        self.master.geometry('300x180')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='选择批准的用户：').grid(row=0, column=0)
        self.scroll_informal.grid(row=1, column=1, rowspan=3)
        self.list_informal.grid(row=1, column=0, rowspan=3)
        self.button_accept.grid(row=4, column=0)
        self.button_back.grid(row=5, column=0)

    # 获取用户信息，以获取用户是否为正式用户
    def get_userdata(self):
        with open('./account/user.json', 'r', encoding='utf-8') as f:
            self.user_dict = json.loads(f.readline())

    # 存储新的用户信息
    def save_userdata(self):
        with open('./account/user.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.user_dict))  # 将用户字典存入json文件中

    # 加载非正式用户列表
    def load_inforaml_user(self):
        self.list_informal.delete(0, END)
        for user in self.user_dict.keys():
            if not self.user_dict[user]['formal_user']:
                self.list_informal.insert(END, user)

    def accept(self):
        # 获取选择的用户
        try:
            selected_user = self.list_informal.get(self.list_informal.curselection())
        except: # 如果没有选择用户则报错
            messagebox.showwarning('错误', '请选择要批准的用户！')
            return
        if messagebox.askyesno('确认批准', '确定要批准' + selected_user + '为正式用户吗？'):
            self.user_dict[selected_user]['formal_user'] = True
        self.save_userdata() # 将变更的用户信息重新存储
        self.load_inforaml_user() # 重新加载非正式用户列表

    # 返回管理员界面
    def back(self):
        self.master.withdraw()
        self.admin_interface.deiconify()
