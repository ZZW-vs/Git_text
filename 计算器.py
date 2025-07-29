import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def calculate():
    try:
        expression = entry.get("1.0", tk.END).strip()
        result = eval(expression)
        result_entry.config(text=str(result))
    except SyntaxError:
        messagebox.showerror("语法错误", "无效的表达式")
    except ZeroDivisionError:
        messagebox.showerror("零除错误", "不能除以零")
    except Exception as e:
        messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

def add_char(char):
    # 将“×”和“÷”替换为“*”和“/”
    entry.insert(tk.END, char.replace('×', '*').replace('÷', '/'))

def clear_entry():
    entry.delete("1.0", tk.END)

def clear_everything():
    clear_entry()
    result_entry.config(text="0")

def delete_last_char():
    entry.delete('end-2c', tk.END)

# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("600x650")
root.configure(bg='#ffffff')

# 创建算式输入框
entry = tk.Text(root, height=1, width=15, font=('Arial', 26), bg='#ffffff', fg='#000000', relief=tk.FLAT, bd=0)
entry.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky='we')
entry.focus_set()

# 创建结果显示框
result_entry = tk.Label(root, height=1, width=15, font=('Arial', 40, 'bold'), bg='#ffffff', fg='#000000', anchor='e')
result_entry.grid(row=1, column=0, columnspan=4, padx=20, pady=(10, 20), sticky='we', ipadx=20)
result_entry.config(text="0")

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
for (text_button, row, col) in buttons:
    command = button_commands.get(text_button, lambda t=text_button: add_char(t))
    btn_style = 'Blue.TButton' if text_button == '=' else 'Rounded.TButton'
    btn = ttk.Button(root, text=text_button, style=btn_style, command=command)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew', ipadx=20, ipady=20)

# 设置网格的权重
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):  # 只需要设置到第4列
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
