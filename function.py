import tkinter as tk
from tkinter import messagebox
import math
import subprocess
import os

class CalculatorFunctions:
    ENTRY_FONT = ('Arial', 26)
    RESULT_FONT = ('Arial', 40, 'bold')
    BUTTON_FONT = ('Arial', 16, 'bold')
    
    ENTRY_BG = 'white'
    ENTRY_FG = '#333333'
    RESULT_BG = '#f8f9fa'
    RESULT_FG = '#4285F4'
    
    SCIENTIFIC_THRESHOLD_HIGH = 1e6
    SCIENTIFIC_THRESHOLD_LOW = 1e-6

    def create_text_entry(self, root):
        entry = tk.Text(
            root, height=1, font=self.ENTRY_FONT,
            bg=self.ENTRY_BG, fg=self.ENTRY_FG, relief=tk.FLAT, bd=0,
            highlightthickness=1, highlightbackground="#e0e0e0",
            highlightcolor="#4285F4", padx=10, pady=5
        )
        entry.grid(row=0, column=0, columnspan=5, padx=20, pady=(20, 10), sticky='we')
        entry.focus_set()
        return entry

    def create_result_label(self, root, result_var):
        label = tk.Label(
            root, height=1, font=self.RESULT_FONT,
            bg=self.RESULT_BG, fg=self.RESULT_FG, anchor='e',
            textvariable=result_var, padx=10
        )
        label.grid(row=1, column=0, columnspan=5, padx=20, pady=(10, 20), sticky='we')
        return label

    def configure_styles(self, style):
        style.configure('Rounded.TButton', 
            relief=tk.FLAT, background='#f5f5f5', font=self.BUTTON_FONT,
            borderwidth=0, padding=12, foreground="black"
        )
        style.configure('Blue.TButton', 
            relief=tk.FLAT, background='#4285F4', font=self.BUTTON_FONT,
            borderwidth=0, padding=12, foreground="black"
        )
        style.configure('Orange.TButton', 
            relief=tk.FLAT, background='#FBBC05', font=self.BUTTON_FONT,
            borderwidth=0, padding=12, foreground="black"
        )
        
        style.map('Rounded.TButton',
            background=[('active', '#e8e8e8')],
            foreground=[('active', "black")]
        )
        style.map('Blue.TButton',
            background=[('active', '#3367D6')],
            foreground=[('active', "black")]
        )
        style.map('Orange.TButton',
            background=[('active', '#F4B400')],
            foreground=[('active', "black")]
        )

    def calculate(self, expression, result_var):
        try:
            expr = expression.strip()
            
            # 彩蛋检测
            if expr.lower() == 'tetris':
                tetris_path = os.path.join(os.path.dirname(__file__), 'Tetris.py')
                subprocess.Popen(['python', tetris_path])
                result_var.set("启动俄罗斯方块!")
                return
                
            expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
            result = eval(expr)
            
            if '/' not in expr.replace(' ', '') and (
                abs(result) >= self.SCIENTIFIC_THRESHOLD_HIGH or 
                0 < abs(result) <= self.SCIENTIFIC_THRESHOLD_LOW
            ):
                result_var.set("{:.6e}".format(result))
            else:
                result_var.set(str(result))
                
        except (SyntaxError, ZeroDivisionError):
            messagebox.showerror("错误", "无效的表达式或除以零")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

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
        self._calculate_math_func(math.sqrt, entry, result_var)
    
    def power(self, entry):
        self.add_char(entry, '**')

    def sin(self, entry, result_var):
        self._calculate_trig_func(math.sin, entry, result_var)

    def cos(self, entry, result_var):
        self._calculate_trig_func(math.cos, entry, result_var)

    def tan(self, entry, result_var):
        self._calculate_trig_func(math.tan, entry, result_var)

    def log(self, entry, result_var):
        self._calculate_math_func(math.log10, entry, result_var)

    def factorial(self, entry, result_var):
        try:
            value = int(entry.get("1.0", tk.END).strip())
            if value < 0:
                messagebox.showerror("错误", "阶乘不能为负数")
                return
            result_var.set(str(math.factorial(value)))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def _calculate_math_func(self, func, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result_var.set(str(func(value)))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def _calculate_trig_func(self, func, entry, result_var):
        try:
            value = float(entry.get("1.0", tk.END).strip())
            result_var.set(str(func(math.radians(value))))
        except ValueError:
            messagebox.showerror("错误", "无效的输入")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def resize_font(self, style, new_size):
        style.configure('Rounded.TButton', font=('Arial', new_size, 'bold'))
        style.configure('Blue.TButton', font=('Arial', new_size, 'bold'))
        style.configure('Orange.TButton', font=('Arial', new_size, 'bold'))
