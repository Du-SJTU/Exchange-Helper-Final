# File: login.py
# Author: Du Jiajie
# Function: 类型修改界面

from tkinter import *
from admin_interface import *

# 类型修改界面类
class Change:
    def __init__(self, master, admin_interface):
        self.master = master
        self.admin_interface = admin_interface
        self.new_type = StringVar() # 存储新的类型名称
        self.new_attribution = StringVar() # 存储新的属性名称
        # 控件
            # 显示物品类型名
        self.scroll_typename = Scrollbar(self.master)
        self.list_typename = Listbox(self.master, width=20, height=6, yscrollcommand=self.scroll_typename.set)
        self.scroll_typename.config(command=self.list_typename.yview)
            # 显示物品类型属性
        self.scroll_attribution = Scrollbar(self.master)
        self.list_attribution = Listbox(self.master, width=20, height=6, yscrollcommand=self.scroll_attribution.set)
        self.scroll_attribution.config(command=self.list_attribution.yview)
        # 修改和增加类型
        self.button_change_type = Button(self.master, text='重命名类型', command=self.rename_type)
        self.button_new_type = Button(self.master, text='新增类型', command=self.create_type)
        # 修改和增加属性
        self.button_change_attribution = Button(self.master, text='重命名属性', command=self.rename_attribution)
        self.button_new_attribution = Button(self.master, text='新增属性', command=self.create_attribution)
        # 属性和类型数据
        self.entry_type = Entry(self.master, textvariable=self.new_type)
        self.entry_attribution = Entry(self.master, textvariable=self.new_attribution)
        # 初始化事件
        self.align_ui() # 排列UI控件
        self.load_type() # 显示类型数据
        self.function_bind() # 进行功能绑定

    # 功能绑定
    def function_bind(self):
        self.list_typename.bind('<Double-Button-1>', lambda x=0:self.load_attribution())

    # 获取类型数据
    def get_type_dict(self):
        with open('./data/type.json', 'r', encoding='utf-8') as f:
            self.type_dict = json.loads(f.readline())
    
    # 显示类型
    def load_type(self):
        self.get_type_dict()
        self.list_typename.delete(0, END)
        for type in self.type_dict.keys():
            self.list_typename.insert(END, type)
    
    # 显示属性
    def load_attribution(self):
        self.list_attribution.delete(0, END)
        try:
            self.selected_type = self.list_typename.get(self.list_typename.curselection())
            for attribution in self.type_dict[self.selected_type]:
                self.list_attribution.insert(END, attribution)
        except:
            for attribution in self.type_dict[self.changed_type]:
                self.list_attribution.insert(END, attribution)

    # 排列UI控件
    def align_ui(self):
        self.master.title("物品类型修改")
        self.master.geometry('350x250')
        self.master.resizable(0, 0)  # 禁止调节窗口大小
        Label(self.master, text='类型（双击以选择）').grid(row=0, column=0)
        Label(self.master, text='属性（双击以选择）').grid(row=0, column=2)
        self.list_typename.grid(row=1, column=0)
        self.scroll_typename.grid(row=1, column=1)
        self.list_attribution.grid(row=1, column=2)
        self.scroll_attribution.grid(row=1, column=3)
        Label(self.master, text='输入类型名称：').grid(row=2, column=0)
        Label(self.master, text='输入属性名称：').grid(row=2, column=2)
        self.entry_type.grid(row=3, column=0)
        self.entry_attribution.grid(row=3, column=2)
        self.button_new_type.grid(row=4, column=0)
        self.button_new_attribution.grid(row=4, column=2)
        self.button_change_type.grid(row=5, column=0)
        self.button_change_attribution.grid(row=5, column=2)

    # 重命名类型
    def rename_type(self):
        try:
            self.selected_type = self.list_typename.get(self.list_typename.curselection())
        except:
            messagebox.showwarning('错误', '请选择要修改的物品类型')
            return
        temp_attribution = self.type_dict[self.selected_type]
        new_typename = self.entry_type.get()
        if new_typename in self.type_dict.keys():
            messagebox.showwarning('错误', '该类型已存在！')
        else:
            if messagebox.askyesno('确认', '确认要将' + self.selected_type + '更名为' + new_typename + '吗？'):
                self.type_dict[new_typename] = temp_attribution
                del self.type_dict[self.selected_type]
        self.save_type()
        self.load_type() # 重新加载类型

    # 重命名属性
    def rename_attribution(self):
        try:
            self.selected_attribution = self.list_attribution.get(self.list_attribution.curselection())
        except:
            messagebox.showwarning('错误', '请选择要修改的物品属性')
            return
        new_attribution = self.entry_attribution.get()
        if new_attribution in self.type_dict[self.selected_type]:
            messagebox.showwarning('错误', '该属性已存在！')
        else:
            if messagebox.askyesno('确认', '确认要将' + self.selected_attribution + '更名为' + new_attribution + '吗？'):
                self.type_dict[self.selected_type].append(new_attribution)
                self.type_dict[self.selected_type].remove(self.selected_attribution)
                self.changed_type = self.selected_type
        self.save_type()
        self.load_attribution() # 重新加载属性

    # 新建类型
    def create_type(self):
        new_typename = self.entry_type.get()
        if new_typename in self.type_dict.keys():
            messagebox.showwarning('错误', '该类型已存在！')
        else:
            if messagebox.askyesno('确认', '确认要添加' + new_typename + '吗？'):
                self.type_dict[new_typename] = []
        self.save_type()
        self.load_type() # 重新加载类型

    # 新建属性
    def create_attribution(self):
        new_attribution = self.entry_attribution.get()
        if new_attribution in self.type_dict[self.selected_type]:
            messagebox.showwarning('错误', '该属性已存在！')
        else:
            if messagebox.askyesno('确认', '确认要添加' + new_attribution + '吗？'):
                self.type_dict[self.selected_type].append(new_attribution)
                self.changed_type = self.selected_type
        self.save_type()
        self.load_attribution() # 重新加载属性

    # 保存类型数据
    def save_type(self):
        with open('./data/type.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.type_dict))


root = Tk()
Change(root, {})
root.mainloop()