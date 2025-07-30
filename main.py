import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from other import *

def resize_font(event):
    # 使用更平滑的字体大小调整逻辑
    new_size = min(max(int(event.height / 10), 16), 24)  # 确保字体大小在16到24之间
    style.configure('Rounded.TButton', font=('Arial', new_size))
    style.configure('Blue.TButton', font=('Arial', new_size))
    result_entry.config(font=('Arial', new_size * 2, 'bold'))  # 调整结果标签的字体大小

# 定义按钮命令映射
button_commands = {
    '=': calculate,
    'C': clear_entry,
    'CE': clear_everything,
    'DEL': delete_last_char
}

# 创建按钮样式
style = ttk.Style()
style.configure('Rounded.TButton', relief=tk.FLAT, background="#f0f0f0", font=('Arial', 16), borderwidth=1, padding=10, highlightbackground="#d3d3d3", highlightthickness=1)
style.configure('Blue.TButton', relief=tk.FLAT, background="#007acc", font=('Arial', 16), borderwidth=1, padding=10, highlightbackground="#d3d3d3", highlightthickness=1)
style.map('Rounded.TButton', background=[('active', "#e0e0e0")])
style.map('Blue.TButton', background=[('active', "#005c99")])

# 定义按钮布局
buttons = [
    # 第一排
    ('CE', 2, 0), ('C', 2, 1), ('DEL', 2, 2), ('+', 2, 3),
    
    # 第二排
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3),
    
    # 第三排
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3),
    
    # 第四排
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('÷', 5, 3),
    
    # 第五排
    ('0', 6, 0), ('.', 6, 1), ('=', 6, 2)
]

# 创建按钮
for text_button, row, col in buttons:
    command = button_commands.get(text_button, lambda t=text_button: add_char(t))
    btn_style = 'Blue.TButton' if text_button == '=' else 'Rounded.TButton'
    btn = ttk.Button(root, text=text_button, style=btn_style, command=command)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew', ipadx=20, ipady=20)

# 设置网格的权重
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):  # 只需要设置到第4列
    root.grid_columnconfigure(i, weight=1)

# 防抖动机制
resize_timer = None

def resize_debounced(event):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    resize_timer = root.after(100, lambda: resize_font(event))

# 监听窗口大小变化事件
root.bind('<Configure>', resize_debounced)

root.mainloop()
