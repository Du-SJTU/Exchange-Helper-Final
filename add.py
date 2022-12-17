# File: add.py
# Author: Du Jiajie
# Function: 添加物品界面

from tkinter import *
from tkinter import ttk
import json
from user_interface import *
from tkinter import messagebox
import time

# 添加物品控制窗口类
class Add:
    def __init__(self, master, user_name, user_interface):
        self.master = master
        self.user_interface = user_interface
        self.user_name = user_name
        self.input_value = StringVar()
        self.add_item_info = {} # 存储添加的物品信息
        self.add_item_attribution= {} # 存储添加物品的类型属性
        self.remain_to_input = [] # 剩余需要输入的属性值
        # 控件
        self.combo_type =ttk.Combobox(self.master)
        self.button_start = Button(self.master, text='开始添加物品', command=self.begin_adding)
        self.button_reset = Button(self.master, text='重新选择', command=self.reset)
        self.label_tip = Label(self.master) # 提示输入内容
        self.entry_input = Entry(self.master, textvariable=self.input_value) # 属性值输入文本框
        self.entry_input.bind('<Return>', lambda x:self.confirm())
        self.button_confirm = Button(self.master, text='确认输入', command=self.confirm)
        self.button_back = Button(self.master, text='返回用户界面', command=self.back)
        # 初始化事件
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.back())  # 关闭此窗口返回用户界面
        self.align_ui() # 排列UI控件
        self.get_type() # 获取物品类型
        self.load_type() # 加载物品类型选择
        self.get_item() # 获取物品列表

    # 排列UI控件
    def align_ui(self):
        self.master.title("添加物品")
        self.master.geometry('400x130')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        self.combo_type.grid(row=0, column=1)
        Label(self.master, text='选择物品类型：').grid(row=0, column=0)
        Label(self.master, text='输入属性值：').grid(row=2, column=0)
        self.button_start.grid(row=0, column=2)
        self.button_reset.grid(row=0, column=3)
        self.button_reset['state'] = DISABLED
        self.entry_input['state'] = DISABLED
        self.label_tip.grid(row=1,column=1)
        self.entry_input.grid(row=2,column=1)
        self.button_confirm.grid(row=2, column=2)
        self.button_confirm['state'] = DISABLED
        self.button_back.grid(row=3, column=2)

    # 获取物品类型
    def get_type(self):
        with open('./data/type.json', 'r', encoding='utf-8') as f:
            self.type_dict = json.loads(f.readline())

    # 加载类型选项
    def load_type(self):
        typelist = []
        for typename in self.type_dict.keys():
            typelist.append(typename)
        self.combo_type['value'] = tuple(typelist)

    # 开始添加物品
    def begin_adding(self):
        self.selected_type = self.combo_type.get()
        try:
            self.remain_to_input = self.type_dict[self.selected_type]
        except:
            messagebox.showwarning('错误', '请选择物品类型！')
            return
        # 变更按钮和输入框状态
        self.combo_type['state'] = DISABLED
        self.button_reset['state'] = NORMAL
        self.button_start['state'] = DISABLED
        self.entry_input['state'] = NORMAL
        self.button_confirm['state'] = NORMAL

        self.remain_to_input.append('简介')
        self.remain_to_input.append('名称')
        self.new_attr_info = self.remain_to_input.pop()
        self.label_tip['text'] = '请输入' + self.new_attr_info + '信息'


    # 重新选择物品类型
    def reset(self):
        self.combo_type['state'] = NORMAL
        self.button_reset['state'] = DISABLED
        self.button_start['state'] = NORMAL
        self.entry_input['state'] = DISABLED
        self.button_confirm['state'] = DISABLED
        self.add_item_info = {} # 重置添加物品信息

    # 获取物品列表
    def get_item(self):
        with open('./data/item.json', 'r', encoding='utf-8') as f:
            self.item_dict = json.loads(f.readline())

    # 保存物品列表
    def save_item(self):
        with open('./data/item.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.item_dict))

    # 确认输入的物品信息
    def confirm(self):
        info = self.input_value.get()
        self.input_value.set('')  # 清空输入方便下一次输入
        if self.new_attr_info == '名称':
            self.add_item_info['name'] = info
        elif self.new_attr_info == '简介':
            self.add_item_info['intro'] = info
        else:
            self.add_item_attribution[self.new_attr_info] = info
        self.add_item_info['attributions'] = self.add_item_attribution
        try:
            self.new_attr_info = self.remain_to_input.pop()
            self.label_tip['text'] = '请输入' + self.new_attr_info + '信息'
        except:
            # 不能pop说明信息已经完全可以完成添加
            index = time.strftime("%Y%m%d%H%M%S", time.localtime())
            self.add_item_info['owner'] = self.user_name
            self.add_item_info['type'] = self.selected_type
            self.item_dict[index] = self.add_item_info
            self.save_item()
            messagebox.showinfo('添加物品成功', '物品' + self.add_item_info['name'] + '添加成功！')
            self.reset()


    # 返回用户界面
    def back(self):
        self.master.withdraw()
        self.user_interface.deiconify()

