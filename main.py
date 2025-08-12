import tkinter as tk
from tkinter import ttk
from function import CalculatorFunctions

class Calculator:
    def __init__(self, root):
        self.root = root
        self.functions = CalculatorFunctions()  # 将所有功能封装到一个类中
        self.entry = self.functions.create_text_entry(root)
        self.result_var = tk.StringVar(value="0")
        self.result_label = self.functions.create_result_label(root, self.result_var)
        self.style = ttk.Style()
        self.configure_styles()
        self.buttons = self.define_buttons()
        self.create_buttons()
        self.set_grid_weights()
        self.resize_timer = None
        self.bind_events()

    def configure_styles(self):
        self.functions.configure_styles(self.style)

    def define_buttons(self):
        return [
            ('CE', 2, 0), ('C', 2, 1), ('DEL', 2, 2), ('+', 2, 3), ('^', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3), ('√', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3), ('sin', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('÷', 5, 3), ('cos', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), 
            ('log', 6, 3), ('n!', 6, 4)
        ]

    def create_buttons(self):
        commands = {
            '=': lambda: self.functions.calculate(self.entry.get("1.0", tk.END), self.result_var),
            'C': lambda: self.functions.clear_entry(self.entry),
            'CE': lambda: self.functions.clear_everything(self.entry, self.result_var),
            'DEL': lambda: self.functions.delete_last_char(self.entry),
            '^': lambda: self.functions.add_char(self.entry, '**'),
            '√': lambda: self.functions.sqrt(self.entry, self.result_var),
            'sin': lambda: self.functions.sin(self.entry, self.result_var),
            'cos': lambda: self.functions.cos(self.entry, self.result_var),
            'tan': lambda: self.functions.tan(self.entry, self.result_var),
            'log': lambda: self.functions.log(self.entry, self.result_var),
            'n!': lambda: self.functions.factorial(self.entry, self.result_var)
        }
        for btn in self.buttons:
            text_button, row, col, *colspan = btn
            colspan = colspan[0] if colspan else 1
            button = ttk.Button(self.root, 
                                text=text_button, 
                                style=self.get_button_style(text_button), 
                                command=commands.get(text_button, lambda: self.functions.add_char(self.entry, text_button)))
            button.grid(row=row, 
                        column=col, 
                        padx=8, 
                        pady=8, 
                        sticky='nsew', 
                        ipadx=10, 
                        ipady=15, 
                        columnspan=colspan)

    def get_button_style(self, button_text):
        if button_text == '=':
            return 'Orange.TButton'
        elif button_text in ['+', '-', '×', '÷', '^', '√', 'sin', 'cos', 'tan', 'log', 'n!']:
            return 'Blue.TButton'
        else:
            return 'Rounded.TButton'

    def set_grid_weights(self):
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

    def resize_font(self, event):
        new_size = min(max(int(event.height / 10), 16), 24)
        self.functions.resize_font(self.style, new_size)
        self.result_label.config(font=('Arial', new_size * 2, 'bold'))

    def resize_debounced(self, event):
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        if event.width != self.root.winfo_width() or event.height != self.root.winfo_height():
            self.resize_timer = self.root.after(100, lambda: self.resize_font(event))

    def bind_events(self):
        self.root.bind('<Configure>', self.resize_debounced)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("科学计算器")
    root.geometry("600x650")
    root.configure(bg='#f8f9fa')
    calculator = Calculator(root)
    root.mainloop()
