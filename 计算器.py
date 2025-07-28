import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        expression = entry.get("1.0", tk.END).strip()
        result = eval(expression)
        update_result(result)
    except Exception as e:
        messagebox.showerror("错误", "无效的表达式")

def add_char(char):
    entry.insert(tk.END, char)

def clear():
    entry.delete("1.0", tk.END)
    update_result('')

def update_result(result):
    result_entry.config(state=tk.NORMAL)
    result_entry.delete("1.0", tk.END)
    result_entry.insert(tk.END, str(result))
    result_entry.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("计算器")
root.geometry("300x400")
root.configure(bg='#F0F0F0')

# 创建输入框
entry = tk.Text(root, height=2, width=20, font=('Arial', 16), bg='#FFFFFF', relief=tk.SUNKEN, bd=2)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='we')

# 创建结果显示框
result_entry = tk.Text(root, height=2, width=20, font=('Arial', 16), bg='#FFFFE0', relief=tk.SUNKEN, bd=2, state=tk.DISABLED)
result_entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='we')

# 按钮布局
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3)
]

# 创建按钮
for (text_button, row, col) in buttons:
    command = calculate if text_button == '=' else lambda t=text_button: add_char(t)
    bg_color = "#FFE344" if text_button == '=' else "#FFBB3C" if text_button in ['+', '-', '*', '/'] else "#EDEBEB"
    btn = tk.Button(root, text=text_button, width=10, height=2, font=('Arial', 14), bg=bg_color, fg='#000000', relief=tk.RAISED, bd=2, command=command)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

# 清除按钮
clear_btn = tk.Button(root, text='C', width=40, height=2, font=('Arial', 14), bg="#FF8649", fg="#EDEBEB", relief=tk.RAISED, bd=2, command=clear)
clear_btn.grid(row=6, column=0, columnspan=4, sticky="we", padx=10, pady=5)

# 设置网格的权重
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
