import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

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
root.geometry("400x600")
root.configure(bg='#202124')

# 创建输入框
entry = tk.Text(root, height=1, width=25, font=('Segoe UI', 24), bg='#202124', fg='#ffffff', relief=tk.FLAT, bd=0)
entry.grid(row=0, column=0, columnspan=4, padx=20, pady=20, sticky='we')

# 创建结果显示框
result_entry = tk.Text(root, height=1, width=25, font=('Segoe UI', 24, 'bold'), bg='#202124', fg='#ffffff', relief=tk.FLAT, bd=0, state=tk.DISABLED)
result_entry.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky='we')

# 使用 ttk.Style 创建自定义样式
style = ttk.Style()
style.theme_use('clam')
style.configure('Rounded.TButton', relief=tk.FLAT, background="#41424d", foreground="#ffffff", font=('Segoe UI', 18),
                borderwidth=0, padding=10)
style.map('Rounded.TButton', background=[('active', "#60616b")])

# 按钮布局
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
    ('C', 6, 0), ('DEL', 6, 1)
]

# 创建按钮
for (text_button, row, col) in buttons:
    command = calculate if text_button == '=' else clear if text_button == 'C' else lambda t=text_button: add_char(t)
    btn = ttk.Button(root, text=text_button, style='Rounded.TButton', command=command)
    btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')

# 设置网格的权重
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
