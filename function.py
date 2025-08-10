import tkinter as tk
from tkinter import messagebox
import math
from functools import partial

def create_root_window():
    root = tk.Tk()
    root.title("科学计算器")
    root.geometry("600x650")
    root.configure(bg='#ffffff')
    return root

def create_text_entry(root):
    entry = tk.Entry(root, font=('Segoe UI', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
    entry.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='we')
    entry.focus_set()
    return entry

def create_result_label(root, result_var):
    result_label = tk.Label(root, height=1, font=('Segoe UI', 40, 'bold'), bg='#ffffff', fg='#000000', anchor='e', textvariable=result_var)
    result_label.grid(row=1, column=0, columnspan=5, padx=20, pady=(10, 20), sticky='we')
    return result_label

def calculate(expression, result_var):
    try:
        result = eval(expression.replace('×', '*').replace('÷', '/').replace('^', '**'))
        result_var.set(str(result))
    except Exception as e:
        handle_error(e)

def handle_error(e):
    if isinstance(e, SyntaxError) or isinstance(e, ZeroDivisionError):
        messagebox.showerror("错误", "无效的表达式或除以零")
    else:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def add_char(entry, char):
    entry.insert(tk.END, char)

def clear_entry(entry):
    entry.delete(0, tk.END)

def clear_everything(entry, result_var):
    clear_entry(entry)
    result_var.set("0")

def delete_last_char(entry):
    entry.delete(len(entry.get()) - 1)

def sqrt(entry, result_var):
    try:
        value = float(entry.get())
        result = math.sqrt(value)
        result_var.set(str(result))
    except Exception as e:
        handle_error(e)

def power(entry, result_var):
    entry.insert(tk.END, '**')

def sin(entry, result_var):
    try:
        value = float(entry.get())
        result = math.sin(math.radians(value))
        result_var.set(str(result))
    except Exception as e:
        handle_error(e)

def cos(entry, result_var):
    try:
        value = float(entry.get())
        result = math.cos(math.radians(value))
        result_var.set(str(result))
    except Exception as e:
        handle_error(e)

def tan(entry, result_var):
    try:
        value = float(entry.get())
        result = math.tan(math.radians(value))
        result_var.set(str(result))
    except Exception as e:
        handle_error(e)
