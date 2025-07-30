import tkinter as tk
from tkinter import messagebox

def create_root_window():
    root = tk.Tk()
    root.title("计算器")
    root.geometry("600x650")
    root.configure(bg='#ffffff')
    return root

def create_text_entry(root):
    entry = tk.Text(root, height=1, font=('Arial', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
    entry.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky='we')
    entry.focus_set()
    return entry

def create_result_label(root, result_var):
    result_entry = tk.Label(root, height=1, font=('Arial', 40, 'bold'), bg='#ffffff', fg='#000000', anchor='e', textvariable=result_var)
    result_entry.grid(row=1, column=0, columnspan=4, padx=20, pady=(10, 20), sticky='we')
    return result_entry

def calculate(entry, result_var):
    try:
        expression = entry.get("1.0", tk.END).strip()
        result = eval(expression)
        result_var.set(str(result))
    except (SyntaxError, ZeroDivisionError) as e:
        messagebox.showerror("错误", f"无效的表达式或除以零: {str(e)}")
        clear_entry(entry)
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")
        clear_entry(entry)

def add_char(entry, char):
    entry.insert(tk.END, char.replace('×', '*').replace('÷', '/'))

def clear_entry(entry):
    entry.delete("1.0", tk.END)

def clear_everything(entry, result_var):
    clear_entry(entry)
    result_var.set("0")

def delete_last_char(entry):
    entry.delete('end-2c', tk.END)
