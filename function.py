import tkinter as tk
from tkinter import messagebox
import math

def create_root_window():
    root = tk.Tk()
    root.title("科学计算器")
    root.geometry("600x650")
    root.configure(bg='#ffffff')
    return root

def create_text_entry(root):
    entry = tk.Text(root, height=1, font=('Arial', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
    entry.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='we')
    entry.focus_set()
    return entry

def create_result_label(root, result_var):
    result_label = tk.Label(root, height=1, font=('Arial', 40, 'bold'), bg='#ffffff', fg='#000000', anchor='e', textvariable=result_var)
    result_label.grid(row=1, column=0, columnspan=5, padx=20, pady=(10, 20), sticky='we')
    return result_label

def calculate(expression, result_var):
    try:
        result = eval(expression.strip().replace('×', '*').replace('÷', '/').replace('^', '**'))
        result_var.set(str(result))
    except (SyntaxError, ZeroDivisionError):
        messagebox.showerror("错误", "无效的表达式或除以零")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def add_char(entry, char):
    entry.insert(tk.END, char)

def clear_entry(entry):
    entry.delete("1.0", tk.END)

def clear_everything(entry, result_var):
    clear_entry(entry)
    result_var.set("0")
    
def delete_last_char(entry):
    entry.delete('end-2c', tk.END)

def sqrt(entry, result_var):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.sqrt(value)
        result_var.set(str(result))
    except ValueError:
        messagebox.showerror("错误", "无效的输入")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def power(entry, result_var):
    entry.insert(tk.END, '**')
    
def sin(entry, result_var):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.sin(math.radians(value))
        result_var.set(str(result))
    except ValueError:
        messagebox.showerror("错误", "无效的输入")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def cos(entry, result_var):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.cos(math.radians(value))
        result_var.set(str(result))
    except ValueError:
        messagebox.showerror("错误", "无效的输入")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def tan(entry, result_var):
    try:
        value = float(entry.get("1.0", tk.END).strip())
        result = math.tan(math.radians(value))
        result_var.set(str(result))
    except ValueError:
        messagebox.showerror("错误", "无效的输入")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")
