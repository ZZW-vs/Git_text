import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def calculate():
    try:
        expression = entry.get("1.0", tk.END).strip()
        result = eval(expression)
        result_var.set(str(result))
    except (SyntaxError, ZeroDivisionError) as e:
        messagebox.showerror("错误", f"无效的表达式或除以零: {str(e)}")
        clear_entry()
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")
        clear_entry()

def add_char(char):
    entry.insert(tk.END, char.replace('×', '*').replace('÷', '/'))

def clear_entry():
    entry.delete("1.0", tk.END)

def clear_everything():
    clear_entry()
    result_var.set("0")

def delete_last_char():
    entry.delete('end-2c', tk.END)

def resize_font(event):
    # 使用更平滑的字体大小调整逻辑
    new_size = min(max(int(event.height / 10), 16), 24)  # 确保字体大小在16到24之间
    style.configure('Rounded.TButton', font=('Arial', new_size))
    style.configure('Blue.TButton', font=('Arial', new_size))
    result_entry.config(font=('Arial', new_size * 2, 'bold'))  # 调整结果标签的字体大小

# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("600x650")  # 设置初始窗口大小
root.configure(bg='#ffffff')

# 创建算式输入框
entry = tk.Text(root, height=1, font=('Arial', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
entry.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky='we')
entry.focus_set()

# 创建结果显示框
result_var = tk.StringVar(value="0")
result_entry = tk.Label(root, height=1, font=('Arial', 40, 'bold'), bg='#ffffff', fg='#000000', anchor='e', textvariable=result_var)
result_entry.grid(row=1, column=0, columnspan=4, padx=20, pady=(10, 20), sticky='we')

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
