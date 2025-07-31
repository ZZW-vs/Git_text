import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from other import create_root_window, create_text_entry, create_result_label, add_char, clear_entry, clear_everything, delete_last_char

class Calculator:
    def __init__(self, root):
        self.root = root
        self.entry = create_text_entry(root)
        self.result_var = tk.StringVar(value="0")
        self.result_label = create_result_label(root, self.result_var)
        self.style = ttk.Style()
        self.configure_styles()
        self.buttons = self.define_buttons()
        self.create_buttons()
        self.set_grid_weights()
        self.resize_timer = None
        self.bind_events()

    def configure_styles(self):
        self.style.configure('Rounded.TButton', relief=tk.FLAT, background="#f0f0f0", font=('Arial', 16), borderwidth=1, padding=10, highlightbackground="#d3d3d3", highlightthickness=1)
        self.style.configure('Blue.TButton', relief=tk.FLAT, background="#007acc", font=('Arial', 16), borderwidth=1, padding=10, highlightbackground="#d3d3d3", highlightthickness=1)
        self.style.configure('Orange.TButton', relief=tk.FLAT, background="#FFA07A", font=('Arial', 16), borderwidth=1, padding=10, highlightbackground="#d3d3d3", highlightthickness=1)
        self.style.map('Rounded.TButton', background=[('active', "#e0e0e0")])
        self.style.map('Blue.TButton', background=[('active', "#005c99")])
        self.style.map('Orange.TButton', background=[('active', "#FF8C69")])

    def define_buttons(self):
        return [
            ('CE', 2, 0), ('C', 2, 1), ('DEL', 2, 2), ('+', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('÷', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2, 2)
        ]

    def create_buttons(self):
        for btn in self.buttons:
            text_button, row, col, colspan = btn if len(btn) == 4 else (*btn, 1)
            command = self.get_button_command(text_button)
            btn_style = 'Orange.TButton' if text_button == '=' else 'Rounded.TButton'
            button = ttk.Button(self.root, text=text_button, style=btn_style, command=command)
            button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew', ipadx=20, ipady=20, columnspan=colspan)

    def get_button_command(self, button_text):
        commands = {
            '=': lambda: self.calculate(self.entry.get("1.0", tk.END)),
            'C': lambda: clear_entry(self.entry),
            'CE': lambda: clear_everything(self.entry, self.result_var),
            'DEL': lambda: delete_last_char(self.entry)
        }
        return commands.get(button_text, lambda: add_char(self.entry, button_text))

    def calculate(self, expression):
        try:
            result = eval(expression.strip().replace('×', '*').replace('÷', '/'))
            self.result_var.set(str(result))
        except (SyntaxError, ZeroDivisionError):
            messagebox.showerror("错误", "无效的表达式或除以零")
        except Exception as e:
            messagebox.showerror("错误", f"发生了一个错误: {str(e)}")

    def set_grid_weights(self):
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def resize_font(self, event):
        new_size = min(max(int(event.height / 10), 16), 24)
        self.style.configure('Rounded.TButton', font=('Arial', new_size))
        self.style.configure('Blue.TButton', font=('Arial', new_size))
        self.style.configure('Orange.TButton', font=('Arial', new_size))
        self.result_label.config(font=('Arial', new_size * 2, 'bold'))

    def resize_debounced(self, event):
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        if event.width != self.root.winfo_width() or event.height != self.root.winfo_height():
            self.resize_timer = self.root.after(100, lambda: self.resize_font(event))

    def bind_events(self):
        self.root.bind('<Configure>', self.resize_debounced)

if __name__ == "__main__":
    root = create_root_window()
    calculator = Calculator(root)
    root.mainloop()
