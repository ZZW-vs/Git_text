import tkinter as tk
from tkinter import ttk
from function import CalculatorFunctions

class Calculator:
    MIN_WIDTH = 520
    MIN_HEIGHT = 650
    INITIAL_SIZE = "600x650"
    BG_COLOR = '#f8f9fa'
    
    BUTTON_STYLES = {
        '=': 'Orange.TButton',
        'operators': 'Blue.TButton',
        'default': 'Rounded.TButton'
    }
    
    OPERATORS = ['+', '-', '×', '÷', '^', '√', 'sin', 'cos', 'tan', 'log', 'n!']
    
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self.functions = CalculatorFunctions()
        self._init_ui()
        self._bind_events()
        
    def _setup_window(self):
        self.root.title("科学计算器")
        self.root.geometry(self.INITIAL_SIZE)
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.configure(bg=self.BG_COLOR)
        
    def _init_ui(self):
        self.entry = self.functions.create_text_entry(self.root)
        self.result_var = tk.StringVar(value="0")
        self.result_label = self.functions.create_result_label(self.root, self.result_var)
        self.style = ttk.Style()
        self.functions.configure_styles(self.style)
        self._setup_grid()
        self._create_buttons()
        
    def _setup_grid(self):
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
    
    def _get_button_style(self, button_text):
        if button_text == '=':
            return self.BUTTON_STYLES['=']
        return self.BUTTON_STYLES['operators'] if button_text in self.OPERATORS else self.BUTTON_STYLES['default']
    
    def _define_buttons(self):
        return [
            ('CE', 2, 0), ('C', 2, 1), ('DEL', 2, 2), ('+', 2, 3), ('^', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('-', 3, 3), ('√', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('×', 4, 3), ('sin', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('÷', 5, 3), ('cos', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('log', 6, 3), ('n!', 6, 4)
        ]
    
    def _create_buttons(self):
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
        
        for text, row, col, *colspan in self._define_buttons():
            colspan = colspan[0] if colspan else 1
            ttk.Button(
                self.root,
                text=text,
                style=self._get_button_style(text),
                command=commands.get(text, lambda t=text: self.functions.add_char(self.entry, t))
            ).grid(
                row=row, column=col, columnspan=colspan,
                padx=8, pady=8, sticky='nsew', ipadx=10, ipady=15
            )
    
    def _resize_font(self, event):
        new_size = min(max(int(event.height / 10), 16), 24)
        self.functions.resize_font(self.style, new_size)
        self.result_label.config(font=('Arial', new_size * 2, 'bold'))
    
    def _resize_debounced(self, event):
        if hasattr(self, 'resize_timer') and self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        if event.width != self.root.winfo_width() or event.height != self.root.winfo_height():
            self.resize_timer = self.root.after(100, lambda: self._resize_font(event))
    
    def _bind_events(self):
        self.root.bind('<Configure>', self._resize_debounced)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
