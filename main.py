# File: login.py
# Author: Du Jiajie
# Function: 主程序
from tkinter import *
from login import *

def main():
    root = Tk()
    login = Login(root)
    root.protocol('WM_DELETE', lambda: exit())
    root.mainloop()
    

if __name__ == '__main__':
    main()