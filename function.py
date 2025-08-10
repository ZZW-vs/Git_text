import tkinter as tk
from tkinter import messagebox
import math
from ttkthemes import ThemedTk

def create_root_window():
    root = ThemedTk(theme="arc")
    root.title("科学计算器")
    root.geometry("600x650")
    root.configure(bg='#ffffff')
    return root

def create_text_entry(root):
    entry = tk.Text(root, font=('Segoe UI', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0, wrap='word')
    entry.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='we')
    entry.focus_set()
    return entry

def create_result_label(root, result_var):
    result_label = tk.Text(root, font=('Segoe UI', 40, 'bold'), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0, wrap='word', height=1)
    result_label.grid(row=1, column=0, columnspan=5, padx=20, pady=(10, 20), sticky='we')
    result_label.insert(tk.END, result_var.get())
    result_label.config(state='disabled')
    return result_label

def calculate(expression, result_label):
    try:
        result = eval(expression.replace('×', '*').replace('÷', '/').replace('^', '**'))
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

def update_result_text(result_label, new_result):
    result_label.config(state='normal')  # 临时设置为可编辑
    result_label.delete(1.0, tk.END)  # 清空内容
    result_label.insert(tk.END, new_result)  # 插入新结果
    result_label.config(state='disabled')  # 重新设置为不可编辑

def handle_error(e):
    if isinstance(e, SyntaxError) or isinstance(e, ZeroDivisionError):
        messagebox.showerror("错误", "无效的表达式或除以零")
    else:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def add_char(entry, char):
    entry.insert(tk.END, char)

def clear_entry(entry):
    entry.delete(1.0, tk.END)

def clear_everything(entry, result_label):
    clear_entry(entry)
    update_result_text(result_label, "0")

def delete_last_char(entry):
    entry.delete('end-2c', tk.END)

def sqrt(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.sqrt(value)
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

def power(entry, result_label):
    entry.insert(tk.END, '**')

def sin(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.sin(math.radians(value))
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

def cos(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.cos(math.radians(value))
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

def tan(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.tan(math.radians(value))
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

# 添加新的数学函数
def log(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.log(value)
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)

def exp(entry, result_label):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.exp(value)
        update_result_text(result_label, str(result))
    except Exception as e:
        handle_error(e)
