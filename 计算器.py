import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

def calculate():
    try:
        expression = entry.get("1.0", tk.END).strip()
        result = eval(expression)
        result_entry.config(state=tk.NORMAL)
        result_entry.delete("1.0", tk.END)
        result_entry.insert(tk.END, str(result))
        result_entry.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("错误", "无效的表达式")

def add_char(char):
    entry.insert(tk.END, char)

def clear_entry():
    entry.delete("1.0", tk.END)
    entry.insert(tk.END, "")  # 重新设置光标位置

def clear_everything():
    entry.delete("1.0", tk.END)
    result_entry.config(state=tk.NORMAL)
    result_entry.delete("1.0", tk.END)
    result_entry.insert(tk.END, "0")
    result_entry.config(state=tk.DISABLED)

def delete_last_char():
    entry.delete('end-2c', tk.END)

def toggle_sign():
    entry.delete("1.0", tk.END)
    try:
        num = float(result_entry.get("1.0", tk.END))
        num = -num
        entry.insert(tk.END, str(num))
    except:
        entry.insert(tk.END, "")

def memory_clear():
    memory.clear()

memory = []

# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("400x600")
root.configure(bg='#ffffff')

# 创建结果显示框
result_entry = tk.Text(root, height=1, width=15, font=('Arial', 40, 'bold'), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0, state=tk.DISABLED, wrap=tk.NONE)
result_entry.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky='e', ipadx=20)

# 创建输入框
entry = tk.Text(root, height=1, width=15, font=('Arial', 24), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
entry.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky='we')

# 创建按钮样式
style = ttk.Style()
style.configure('Rounded.TButton', relief=tk.FLAT, background="#f0f0f0", font=('Arial', 16), borderwidth=1, bd=1, padding=10)
style.configure('Blue.TButton', relief=tk.FLAT, background="#007acc", font=('Arial', 16), borderwidth=1, bd=1, padding=10)
style.map('Rounded.TButton', background=[('active', "#e0e0e0")])
style.map('Blue.TButton', background=[('active', "#005c99")])

# 定义按钮布局
buttons = [
    # 第一排
    ('MC', 2, 0), ('MR', 2, 1), ('M+', 2, 2), ('M-', 2, 3), ('MS', 2, 4), ('M-', 2, 5),
    
    # 第二排
    ('%', 3, 0), ('CE', 3, 1), ('C', 3, 2), ('1/x', 3, 3), ('x²', 3, 4), ('√x', 3, 5), ('÷', 3, 6),
    
    # 第三排
    ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('×', 4, 3),
    
    # 第四排
    ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),
    
    # 第五排
    ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3),
    
    # 第六排
    ('+/-', 7, 0), ('0', 7, 1), ('.', 7, 2), ('=', 7, 3)
]

# 创建按钮
for (text_button, row, col) in buttons:
    if text_button == '=':
        command = calculate
    elif text_button == 'C':
        command = clear_entry
    elif text_button == 'CE':
        command = clear_everything
    elif text_button == 'DEL':
        command = delete_last_char
    elif text_button == '+/-':
        command = toggle_sign
    elif text_button == 'MC':
        command = memory_clear
    else:
        command = lambda t=text_button: add_char(t)
    if text_button == '=':
        btn = ttk.Button(root, text=text_button, style='Blue.TButton', command=command)
    else:
        btn = ttk.Button(root, text=text_button, style='Rounded.TButton', command=command)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

# 设置网格的权重
for i in range(8):
    root.grid_rowconfigure(i, weight=1)
for i in range(6):
    root.grid_columnconfigure(i, weight=1)

# 设置输入区域和结果显示区域的背景透明
result_entry.config(state=tk.NORMAL)
result_entry.insert(tk.END, "0")
result_entry.config(state=tk.DISABLED)

# 设置光标初始位置在输入框
entry.insert(tk.END, "")
entry.focus_set()

root.mainloop()
