# File: login.py
# Author: Du Jiajie
# Function: 登录界面

from tkinter import *
from register import *
from user_interface import *
from admin_interface import *
from tkinter import messagebox
import json

# 登录窗口类
class Login:
    # 初始化登录窗口控件
    def __init__(self, master):
        # 变量
        self.user_name = StringVar() # 存储用户名
        self.password = StringVar() # 存储密码
        self.is_admin = BooleanVar()
        # 控件
        self.master = master
        self.button_login = Button(master, text='登录', command=self.login) # 登录按钮
        self.button_register = Button(master, text='注册', command=self.register) # 注册按钮
        self.check_is_admin = Checkbutton(master, text='管理员登录', variable=self.is_admin) # 管理员登录选择框
        self.entry_user = Entry(master, textvariable=self.user_name, width=35) # 输入用户名
        self.entry_password = Entry(master, textvariable=self.password, show='*', width=35) # 输入密码
        # 初始化事件
        self.entry_user.focus() # 将焦点默认转移到用户名输入框
        self.align_ui() # 排列UI控件
        self.function_bind() # 绑定控件功能
        self.master.protocol("WM_DELETE_WINDOW", lambda x=0: exit(x)) # 关闭此窗口退出程序

        
    # 排列UI中的控件
    def align_ui(self):
        self.master.title("用户登录")
        self.master.geometry('340x150')
        self.master.resizable(0, 0)  # 禁止调节窗口大小

        Label(self.master, text='“你帮我助”物品交换系统登录', font=10).grid(row=0, column=0, columnspan=8, sticky=E)
        Label(self.master, text='账号', font=10).grid(row=1, column=0, sticky=E)
        Label(self.master, text='密码', font=10).grid(row=2, column=0, sticky=E)
        self.entry_user.grid(row=1, column=1, columnspan=4)
        self.entry_password.grid(row=2,column=1, columnspan=4)
        self.check_is_admin.grid(row=3, column=1)
        self.button_login.grid(row=4, column=1)
        self.button_register.grid(row=4, column=3)
    
    # 给各个控件绑定事件
    def function_bind(self):
        # 在用户名输入框按下回车焦点转移至密码输入框，在密码输入框按下回车相当于点击登录
        self.entry_user.bind('<Return>', lambda x: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda x: self.login())

    # 登录事件
    def login(self):
        if self.is_admin.get():
            self.admin_login()
        else:
            self.user_login()

    # 获取用户的信息
    def get_userdata(self):
        with open('./account/user.json', 'r', encoding='utf-8') as f:
            self.user_dict = json.loads(f.readline())
            ################### Code for TEST
            #print(self.user_dict)
            ###################

    # 获取管理员的信息
    def get_admindata(self):
        with open('./account/admin.json', 'r', encoding='utf-8') as f:
            self.admin_dict = json.loads(f.readline())
            ################### Code for TEST
            #print(self.admin_dict)
            ###################

    def user_login(self):
        self.get_userdata() # 读取用户信息
        account = self.user_name.get()
        password = self.password.get()
        try:
            if self.user_dict[account]['password'] == password:
                if self.user_dict[account]['formal_user']:
                    self.goto_user_interface() # 进入用户界面
                else:
                    messagebox.showwarning('用户登录失败', '请等待管理员批准为正式用户！')
            else:
                messagebox.showwarning('用户登录失败', '用户名或密码错误！')
        # 如果用户名不在字典中，则进行同样的弹窗处理
        except KeyError:
            messagebox.showwarning('用户登录失败', '用户名或密码错误！')


    def admin_login(self):
        self.get_admindata() # 读取管理员信息
        account = self.user_name.get()
        password = self.password.get()
        try:
            if self.admin_dict[account]['password'] == password:
                self.goto_admin_interface()  # 进入管理员界面
            else:
                messagebox.showwarning('用户登录失败', '用户名或密码错误！')
        # 如果用户名不在字典中，则进行同样的弹窗处理
        except KeyError:
            messagebox.showwarning('用户登录失败', '用户名或密码错误！')

    # 进入用户界面
    def goto_user_interface(self):
        self.master.withdraw()
        UserInterface(Toplevel(), self.user_name.get(), self.user_dict[self.user_name.get()])

    # 进入管理员界面
    def goto_admin_interface(self):
        self.master.withdraw()
        AdminInterface(Toplevel(), self.admin_dict[self.user_name.get()])

    # 进行注册操作
    def register(self):
        self.master.withdraw()
        Register(self.master)
        