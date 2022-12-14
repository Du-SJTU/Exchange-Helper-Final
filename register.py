# File: register.py
# Author: Du Jiajie
# Function: 注册界面

from tkinter import *
from tkinter import messagebox
import json

# 注册窗口类
class Register:
    # 初始化注册窗口控件
    def __init__(self, login):
        self.login = login
        self.master = Toplevel()
        # 变量
        self.new_account = StringVar() # 新账号
        self.password = StringVar() # 密码
        self.password_confirm = StringVar() # 确认密码
        self.name = StringVar() # 姓名
        self.address = StringVar() # 住址
        self.tel = StringVar() # 联系方式
        # 控件
        self.entry_new_account = Entry(self.master, textvariable=self.new_account, width=45) # 输入新用户名
        self.entry_password = Entry(self.master, textvariable=self.password, width=45, show='*') # 输入密码
        self.entry_password_confirm = Entry(self.master, textvariable=self.password_confirm, width=45, show='*') # 再次输入密码
        self.entry_name = Entry(self.master, textvariable=self.name, width=45) # 输入姓名
        self.entry_address = Entry(self.master, textvariable=self.address, width=45) # 输入地址
        self.entry_tel = Entry(self.master, textvariable=self.tel, width=45) # 输入联系电话 
        self.button_register = Button(self.master, text='注册', command=self.register) # 注册按钮
        self.button_back_to_login = Button(self.master, text='返回', command=self.back) # 返回登录界面
        # 初始化事件
        self.align_ui() # 排列UI控件
        self.function_bind() # 绑定控件功能
        self.master.protocol("WM_DELETE_WINDOW", lambda x=0: exit(x)) # 关闭此窗口退出程序

    # 排列UI中的控件
    def align_ui(self):
        self.master.title('新用户注册')
        self.master.geometry('390x260')
        self.master.resizable(0, 0)  # 禁止调节窗口大小

        Label(self.master, text='新用户注册', font=10).grid(row=0, column=0, columnspan=2, sticky=E)
        Label(self.master, text='新账号').grid(row=1, column=0, sticky=E)
        Label(self.master, text='密码').grid(row=2, column=0, sticky=E)
        Label(self.master, text='确认密码').grid(row=3, column=0, sticky=E)
        Label(self.master, text='个人基本信息', font=10).grid(row=4, column=0, columnspan=2, sticky=E)
        Label(self.master, text='姓名').grid(row=5, column=0, sticky=E)
        Label(self.master, text='住址').grid(row=6, column=0, sticky=E)
        Label(self.master, text='联系方式').grid(row=7, column=0, sticky=E)
        Label(self.master).grid(row=8, column=0)

        self.entry_new_account.grid(row=1, column=1, columnspan=4)
        self.entry_password.grid(row=2, column=1, columnspan=4)
        self.entry_password_confirm.grid(row=3, column=1, columnspan=4)
        self.entry_name.grid(row=5, column=1, columnspan=4)
        self.entry_address.grid(row=6, column=1, columnspan=4)
        self.entry_tel.grid(row=7, column=1, columnspan=4)
        self.button_register.grid(row=9, column=1)
        self.button_back_to_login.grid(row=9, column=3)

    # 控件功能绑定，此处通过回车实现各种输入框之间快速跳转
    def function_bind(self):
        self.entry_new_account.focus()
        self.entry_new_account.bind('<Return>', lambda x: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda x: self.entry_password_confirm.focus())
        self.entry_password_confirm.bind('<Return>', lambda x: self.entry_name.focus())
        self.entry_name.bind('<Return>', lambda x: self.entry_address.focus())
        self.entry_address.bind('<Return>', lambda x: self.entry_tel.focus())
        self.entry_tel.bind('<Return>', lambda x: self.register())

    # 进行新用户注册
    def register(self):
        new_account = self.new_account.get()
        password = self.password.get()
        password_confirm = self.password_confirm.get()
        name = self.name.get()
        address = self.address.get()
        tel = self.tel.get()

        self.get_userdata()

        if len(new_account) < 3 or len(new_account) > 16: # 检测用户名长度是否符合规范
            messagebox.showwarning('用户名不符合要求', '用户名请设置在3~16个字符之间。')
            self.entry_new_account.focus()
        elif new_account in list(self.user_dict.keys()): # 检测用户名是否被注册
            messagebox.showwarning('用户名不符合要求', '该用户名已被注册！')
            self.entry_new_account.focus()
        elif len(password) < 8 or len(password) > 16: # 检测密码长度是否符合规范
            messagebox.showwarning('密码不符合要求', '密码长度需要在8~16个字符之间')
            self.entry_password.focus()
        elif password != password_confirm: # 检测两次输入的密码是否相同
            messagebox.showwarning('密码不符合要求', '两次输入的密码不一致')
            self.entry_password.focus()
        else:
            new_user_info = {"password": password, "name":name, "address": address, "tel": tel, "formal_user": False}
            self.user_dict[new_account] = new_user_info # 将新的用户信息添加入字典
            self.save_userdata()
            messagebox.showinfo('注册成功！', '用户' + new_account + '注册成功！')
            self.back()

    # 读取用户信息并存储在字典中
    def get_userdata(self):
        with open('./account/user.json', 'r', encoding='utf-8') as f:
            self.user_dict = json.loads(f.readline())

    # 存储新的用户信息
    def save_userdata(self):
        with open('./account/user.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.user_dict)) # 将用户字典存入json文件中

    # 返回登录界面
    def back(self):
        self.master.destroy()
        self.login.deiconify()
