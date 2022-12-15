# File: search.py
# Author: Du Jiajie
# Function: 查找物品界面

from tkinter import *
from tkinter import messagebox
import json
from user_interface import *

# 输入窗口类，用于查找和添加物品
class Search:
    def __init__(self, master, user_interface):
        # master: 窗体 input_info: 需要输入的信息名称
        # 变量
        self.keyword = StringVar() # 输入的关键字
        self.select_type = StringVar() # 选择的物品类型
        self.is_owner = BooleanVar() # 关键字是否为用户名称
        self.is_intro = BooleanVar() # 关键字是否为物品介绍
        self.user_interface = user_interface
        self.result_cnt = 0 # 找到的结果数
        # 控件
        self.master = master
            # 选择类型 滚动条
        self.scroll_type = Scrollbar(self.master)
        self.list_type = Listbox(self.master, width=20, height=4, yscrollcommand=self.scroll_type.set)
        self.scroll_type.config(command=self.list_type.yview)
        self.entry_keyword = Entry(self.master, textvariable=self.keyword, width=20)
        self.check_is_owner = Checkbutton(self.master, variable=self.is_owner, text='用户名')
        self.check_is_intro = Checkbutton(self.master, variable=self.is_intro, text='物品简介')
        self.button_search = Button(self.master, text='查找', command=self.find)
        self.button_back = Button(self.master, text='返回用户界面', command=self.back)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.back()) # 关闭此窗口返回用户界面
        self.scroll_result = Scrollbar(self.master)
        self.list_result = Listbox(self.master, width=40, height=4, yscrollcommand=self.scroll_result.set)
        self.scroll_result.config(command=self.list_result.yview)
        self.list_result.bind('<Double-Button-1>', lambda x=0: self.show_detail())
        self.label_detail = Label(self.master, text='', wraplength=300)
        # 排列UI控件
        self.align_ui()
        # 获取用户和物品的信息
        self.get_userdata()
        self.get_item()

    def align_ui(self):
        self.master.title("查找物品")
        self.master.geometry('340x400')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='选择物品类型：').grid(row=0, column=0)
        self.load_type() # 加载物品类型
        self.scroll_type.grid(row=1, column=1, rowspan=3)
        self.list_type.grid(row=1, column=0, rowspan=3)
        Label(self.master, text='输入关键字：').grid(row=0, column=2, columnspan=3, sticky=W)
        self.entry_keyword.grid(row=1, column=2, columnspan=3)
        self.check_is_owner.grid(row=2, column=2)
        self.check_is_intro.grid(row=2, column=3)
        self.button_search.grid(row=3, column=2)
        self.button_back.grid(row=3, column=3)
        self.show_result = Label(self.master, text='找到' + str(self.result_cnt) + '条结果')
        self.show_result.grid(row=4, column=0)
        self.scroll_result.grid(row=5, column=5, rowspan=3)
        self.list_result.grid(row=5, column=0, rowspan=3, columnspan=5)
        self.label_detail.grid(row=9, column=0, rowspan=5, columnspan=10)

    # 获取物品类型
    def get_type(self):
        with open('./data/type.json', 'r', encoding='utf-8') as f:
            self.type_dict = json.loads(f.readline())

    # 将物品类型加载入滚动条
    def load_type(self):
        self.get_type() # 获取物品列表
        for type in self.type_dict.keys():
            self.list_type.insert(END, type)

    # 获取物品列表
    def get_item(self):
        with open('./data/item.json', 'r', encoding='utf-8') as f:
            self.item_dict = json.loads(f.readline())

    def find(self):
        self.result_cnt = 0 # 计数器归零
        self.list_result.delete(0, END) # 清空搜索结果列表
        try:
            item_type = self.list_type.get(self.list_type.curselection()) # 获得当前选中的类型
        except:
            messagebox.showwarning('错误', '请选择物品类型！')
            return
        keyword = self.keyword.get()
        is_owner = self.is_owner.get()
        is_intro = self.is_intro.get()
        
        for item in self.item_dict.keys():
            if not is_owner and not is_intro:
                messagebox.showwarning('错误', '请选择要匹配的关键字类型！')
                return
            else:
                if self.item_dict[item]['type'] == item_type:
                    if is_owner and not is_intro:
                        # 匹配物品所有者
                        if self.item_dict[item]['owner'] == keyword:
                            self.list_result.insert(END, item + ':' + self.item_dict[item]['name'])
                            self.result_cnt += 1
                    elif not is_owner and is_intro:
                        # 匹配物品说明
                        if keyword in self.item_dict[item]['intro']:
                            self.list_result.insert(END, item + ':' + self.item_dict[item]['name'])
                            self.result_cnt += 1
                    elif is_owner and is_intro:
                        if self.item_dict[item]['owner'] == keyword or keyword in self.item_dict[item]['intro']:
                            self.list_result.insert(END, item + ':' + self.item_dict[item]['name'])
                            self.result_cnt += 1
        self.show_result.configure(text='找到' + str(self.result_cnt) + '条结果，双击以查看。')

    # 获取用户信息，以获取物品所有者的联系方式和姓名
    def get_userdata(self):
        with open('./account/user.json', 'r', encoding='utf-8') as f:
            self.user_dict = json.loads(f.readline())

    # 显示物品的详细信息
    def show_detail(self):
        text = ''
        item_result = self.list_result.get(self.list_result.curselection()) # 获得当前选中的记录
        index = item_result.split(':')[0]
        # 显示物品简介
        text = item_result.split(':')[1] + '\n' +\
            '类型：' + self.item_dict[index]['type'] + '\n' +\
            '简介：' + self.item_dict[index]['intro'] + '\n'
        self.item_dict[index]
        attribution_dict = self.item_dict[index]['attributions'] # 不同种类物品特有属性
        # 显示物品特有属性
        for attribution in attribution_dict.keys():
            text = text + attribution + "：" + attribution_dict[attribution] + '\n'
        owner_account = self.item_dict[index]['owner']
        # 显示物主信息
        text = text + '物主姓名：' + self.user_dict[owner_account]['name'] + '（用户名：' + owner_account + '）\n' +\
            '地址：' + self.user_dict[owner_account]['address'] + '\n' +\
            '联系方式：' + self.user_dict[owner_account]['tel']
        self.label_detail.config(text=text)

    # 返回用户界面
    def back(self):
        self.master.withdraw()
        self.user_interface.deiconify()
        
