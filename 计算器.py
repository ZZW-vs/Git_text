import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("错误", "无效的表达式")

def add_char(char):
    entry.insert(tk.END, char)

def clear():
    entry.delete(0, tk.END)

# 创建主窗口
root = tk.Tk()
root.title("计算器")

# 允许用户自定义窗口大小
root.resizable(True, True)

# 输入框
entry = tk.Entry(root, width=20, font=('Arial', 16), justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='we')

# 按钮布局
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# 创建按钮
for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(root, text=text, width=10, height=2, command=calculate)
    else:
        btn = tk.Button(root, text=text, width=10, height=2, command=lambda t=text: add_char(t))
    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

# 清除按钮
clear_btn = tk.Button(root, text='C', width=40, height=2, command=clear)
clear_btn.grid(row=5, column=0, columnspan=4, sticky="we", padx=5, pady=5)

# 设置网格的权重，使按钮和输入框在窗口大小改变时能够正确调整大小
for i in range(6):  # 0到5行
    root.grid_rowconfigure(i, weight=1)
for i in range(4):  # 0到3列
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
