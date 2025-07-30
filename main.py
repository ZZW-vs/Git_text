import tkinter as tk
from tkinter import ttk
from other import *

def resize_font(event, result_entry, style):
    new_size = min(max(int(event.height / 10), 16), 24)
    style.configure('Rounded.TButton', font=('Arial', new_size))
    style.configure('Blue.TButton', font=('Arial', new_size))
    style.configure('Orange.TButton', font=('Arial', new_size))  # 添加新的样式配置
    result_entry.config(font=('Arial', new_size * 2, 'bold'))

def resize_debounced(event, result_entry, style):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    # 只在窗口大小改变时调整字体大小
    if event.width != root.winfo_width() or event.height != root.winfo_height():
        resize_timer = root.after(100, lambda: resize_font(event, result_entry, style))

root = create_root_window()
entry = create_text_entry(root)
result_var = tk.StringVar(value="0")
result_entry = create_result_label(root, result_var)

# 定义按钮命令映射
button_commands = {
    '=': lambda: calculate(entry, result_var),
    'C': lambda: clear_entry(entry),
    'CE': lambda: clear_everything(entry, result_var),
    'DEL': lambda: delete_last_char(entry)
}

# 创建按钮样式
style = ttk.Style()
style.configure(
    'Rounded.TButton',
    relief=tk.FLAT,
    background="#f0f0f0",
    font=('Arial', 16),
    borderwidth=1,
    padding=10,
    highlightbackground="#d3d3d3",
    highlightthickness=1
)

style.configure(
    'Blue.TButton', 
    relief=tk.FLAT, 
    background="#007acc", 
    font=('Arial', 16), 
    borderwidth=1, 
    padding=10, 
    highlightbackground="#d3d3d3", 
    highlightthickness=1
)

style.configure(
    'Orange.TButton', 
    relief=tk.FLAT, 
    background="#FFA07A", 
    font=('Arial', 16), 
    borderwidth=1, 
    padding=10, 
    highlightbackground="#d3d3d3", 
    highlightthickness=1
)

style.map('Rounded.TButton', background=[('active', "#e0e0e0")])
style.map('Blue.TButton', background=[('active', "#005c99")])
style.map('Orange.TButton', background=[('active', "#FF8C69")])  # 淡橙色激活背景

# 定义按钮布局
buttons = [
    ('CE', 2, 0), ('C', 2, 1), ('DEL', 2, 2), ('+', 2, 3),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('÷', 5, 3),
    ('0', 6, 0), ('.', 6, 1), ('=', 6, 2, 2)  # 增加列跨度
]

# 创建按钮
for btn in buttons:
    if len(btn) == 4:  # 检查是否有列跨度信息
        text_button, row, col, colspan = btn
    else:
        text_button, row, col = btn
        colspan = 1  # 默认列跨度为1
    command = button_commands.get(text_button, lambda t=text_button: add_char(entry, t))
    btn_style = 'Orange.TButton' if text_button == '=' else 'Rounded.TButton'
    
    btn = ttk.Button(
        root, 
        text=text_button, 
        style=btn_style, 
        command=command
    )
    
    btn.grid(
        row=row, 
        column=col, 
        padx=5, 
        pady=5, 
        sticky='nsew', 
        ipadx=20, 
        ipady=20, 
        columnspan=colspan
    )

# 设置网格的权重
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# 防抖动机制
resize_timer = None

def configure_event_handler(event):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    # 只在窗口大小改变时调整字体大小
    if event.width != root.winfo_width() or event.height != root.winfo_height():
        resize_timer = root.after(100, lambda: resize_font(event, result_entry, style))

root.bind('<Configure>', configure_event_handler)

root.mainloop()
