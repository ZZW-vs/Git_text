import tkinter as tk
from tkinter import messagebox
import math

class CalculatorFunctions:
    def create_text_entry(self, root):
        entry = tk.Text(root, 
                        height=1, 
                        font=('Arial', 26), 
                        bg='white', 
                        fg='#333333', 
                        relief=tk.FLAT, 
                        bd=0,
                        highlightthickness=1,
                        highlightbackground="#e0e0e0",
                        highlightcolor="#4285F4",
                        padx=10,
                        pady=5)
        entry.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='we')
        entry.focus_set()
        return entry

    def create_result_label(self, root, result_var):
        result_label = tk.Label(root, 
                                height=1, 
                                font=('Arial', 40, 'bold'), 
                                bg='#f8f9fa', 
                                fg='#4285F4',
                                anchor='e', 
                                textvariable=result_var,
                                padx=10)
        result_label.grid(row=1, column=0, columnspan=5, padx=20, pady=(10, 20), sticky='we')
        return result_label

    def configure_styles(self, style):
        style.configure('Rounded.TButton', 
                        relief=tk.FLAT, 
                        background="#f5f5f5", 
                        font=('Arial', 16, 'bold'), 
                        borderwidth=0, 
                        padding=12, 
                        foreground="#333333")
        style.configure('Blue.TButton', 
                        relief=tk.FLAT, 
                        background="#4285F4", 
                        font=('Arial', 16, 'bold'), 
                        borderwidth=0, 
                        padding=12, 
                        foreground="white")
        style.configure('Orange.TButton', 
                        relief=tk.FLAT, 
                        background="#FBBC05", 
                        font=('Arial', 16, 'bold'), 
                        borderwidth=0, 
                        padding=12, 
                        foreground="#333333")
                        
        style.map('Rounded.TButton', 
                  background=[('active', "#e8e8e8")],
                  foreground=[('active', "#000000")])
        style.map('Blue.TButton', 
                  background=[('active', "#3367D6")],
                  foreground=[('active', "white")])
        style.map('Orange.TButton', 
                  background=[('active', "#F4B400")],
                  foreground=[('active', "#333333")])

    def calculate(self, expression, result_var):
        try:
            expression = expression.strip().replace('×', '*').replace('÷', '/').replace('^', '**')
            result = eval(expression)
            result_var.set(str(result))
        except (SyntaxError, ZeroDivisionError):
            messagebox.showerror("错误", "无效的表达式或除以零")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def add_char(self, entry, char):
        entry.insert(tk.END, char)

    def clear_entry(self, entry):
        entry.delete("1.0", tk.END)

    def clear_everything(self, entry, result_var):
        self.clear_entry(entry)
        result_var.set("0")
        
    def delete_last_char(self, entry):
        entry.delete('end-2c', tk.END)

    def sqrt(self, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result = math.sqrt(value)
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def power(self, entry):
        self.add_char(entry, '**')
    
    def sin(self, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result = math.sin(math.radians(value))
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def cos(self, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result = math.cos(math.radians(value))
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def tan(self, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result = math.tan(math.radians(value))
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def log(self, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result = math.log10(value)
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def factorial(self, entry, result_var):
        try:
            value = int(entry.get("1.0", tk.END).strip())
            if value < 0:
                messagebox.showerror("错误", "阶乘不能为负数")
                return
            result = math.factorial(value)
            result_var.set(str(result))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def resize_font(self, style, new_size):
        style.configure('Rounded.TButton', font=('Arial', new_size, 'bold'))
        style.configure('Blue.TButton', font=('Arial', new_size, 'bold'))
        style.configure('Orange.TButton', font=('Arial', new_size, 'bold'))
