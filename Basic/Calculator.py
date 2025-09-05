import tkinter as tk
import math
import ast
import re
from tkinter import messagebox
from fractions import Fraction

# --- Security & Evaluation Engine ---
allowed_nodes = {'Expression', 'BinOp', 'UnaryOp', 'Num', 'Add', 'Sub', 'Mult', 'Div', 'Pow', 'USub', 'UAdd', 'Constant', 'Call', 'Name', 'Load'}
# Add Fraction to the allowed names, remove pi and e as they are now pre-processed
allowed_names = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'log': math.log10, 
    'ln': math.log, 'sqrt': math.sqrt, 'factorial': math.factorial,
    'Fraction': Fraction
}

def safe_eval(expr):
    """Safely evaluates a mathematical expression string using an AST whitelist."""
    try:
        node = ast.parse(expr, mode='eval').body
        for sub_node in ast.walk(node):
            if type(sub_node).__name__ not in allowed_nodes:
                return f"Error: Operation '{type(sub_node).__name__}' is not allowed"
            if isinstance(sub_node, ast.Name) and sub_node.id not in allowed_names:
                return f"Error: Name '{sub_node.id}' is not allowed"
        return eval(compile(ast.Expression(body=node), '<string>', 'eval'), {"__builtins__": {}}, allowed_names)
    except Exception as e:
        return f"Error: {e}"

# --- Main Application ---
class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")
        master.configure(bg='#1c1c1c')

        self.display = tk.Entry(master, font=('Arial', 30), bd=0, justify='right', 
                                bg='#1c1c1c', fg='white', highlightthickness=0, insertbackground='white')
        self.display.grid(row=0, column=0, columnspan=5, pady=(10, 5), padx=10, sticky="nsew")

        # --- Mode Toggle ---
        self.output_mode = 'decimal' # 'decimal' or 'fraction'
        self.mode_button = tk.Button(master, text="Mode: Decimal", font=('Arial', 10), command=self.toggle_mode,
                                     bd=0, highlightthickness=0, fg='white', bg='#404040', 
                                     activebackground='#505050', activeforeground='white')
        self.mode_button.grid(row=1, column=0, columnspan=5, sticky='ew', padx=10, pady=(0, 10))

        self.display.bind("<Key>", self.on_key_press)
        self.display.focus_set()

        button_grid = [
            ['sin', 'cos', 'tan', 'log', 'ln'],
            ['(', ')', 'sqrt', '^', 'x!'],
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '<-'],
            ['1', '2', '3', '-', 'pi'],
            ['0', '.', '=', '+', 'e']
        ]

        for r_idx, row in enumerate(button_grid):
            for c_idx, text in enumerate(row):
                self.create_button(text, r_idx + 2, c_idx) # Shift buttons down

        for i in range(5): self.master.grid_columnconfigure(i, weight=1)
        for i in range(2, 8): self.master.grid_rowconfigure(i, weight=1) # Adjust for new row

    def on_key_press(self, event):
        """Handles all keyboard input, including special keys and scrolling."""
        key, char = event.keysym, event.char
        
        if key in ('Left', 'Right'):
            self.master.after_idle(self.display.xview, tk.INSERT)
            return

        action_map = {'Return': self.calculate_result, 'Escape': self.clear_display, 'BackSpace': self.backspace}
        if key in action_map:
            action_map[key]()
        elif char.isdigit() or char in '.()!+-*/':
            self.insert_text(char)
        elif char == '^':
            self.insert_text('**')
        
        if char.isprintable(): return "break"

    def insert_text(self, text):
        """Inserts text with validation against consecutive operators."""
        expression = self.display.get()
        op_set = {'+', '-', '*', '/', '.'}
        is_op = text in op_set or text == '**'

        if is_op and ((not expression and text != '-') or (expression and (expression.endswith(tuple(op_set)) or expression.endswith('**')))):
            return

        self.display.insert(tk.INSERT, text)
        self.master.after_idle(self.display.xview, tk.INSERT)

    def toggle_mode(self):
        """Toggles the output mode between decimal and fraction."""
        if self.output_mode == 'decimal':
            self.output_mode = 'fraction'
            self.mode_button.config(text="Mode: Fraction")
        else:
            self.output_mode = 'decimal'
            self.mode_button.config(text="Mode: Decimal")

    def create_button(self, text, row, col):
        """Creates a styled button with its corresponding action."""
        if text.isdigit() or text == '.': color = ('#333333', '#444444')
        elif text in ['/', '*', '-', '+', '=']: color = ('#ff9f0a', '#ffb03a')
        elif text in ['C', '<-']: color = ('#a5a5a5', '#b5b5b5')
        else: color = ('#606060', '#707070')
        
        action_map = {
            'C': self.clear_display, '<-': self.backspace, '=': self.calculate_result,
            'sin': lambda: self.insert_text('sin('), 'cos': lambda: self.insert_text('cos('),
            'tan': lambda: self.insert_text('tan('), 'log': lambda: self.insert_text('log('),
            'ln': lambda: self.insert_text('ln('), 'sqrt': lambda: self.insert_text('sqrt('),
            'x!': lambda: self.insert_text('!'), '^': lambda: self.insert_text('**')
        }
        action = action_map.get(text, lambda: self.insert_text(text))

        button = tk.Button(self.master, text=text, font=('Arial', 16), command=action,
                           bd=0, highlightthickness=0, fg='white', bg=color[0], 
                           activebackground=color[1], activeforeground='white')
        button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

    def clear_display(self):
        self.display.delete(0, tk.END)

    def backspace(self):
        if self.display.index(tk.INSERT) > 0:
            self.display.delete(self.display.index(tk.INSERT) - 1)
            self.master.after_idle(self.display.xview, tk.INSERT)

    def calculate_result(self):
        expression = self.display.get()
        if not expression: return

        try:
            # --- Pre-processing for Fraction Engine ---
            # 1. Substitute constants
            expression = expression.replace('pi', str(math.pi)).replace('e', str(math.e))
            
            # 2. Handle implicit multiplication and factorials
            subs = [
                (r'(\d+(?:\.\d+)?)\s*!', r'factorial(\1)'), (r'(\([^)]+\))\s*!', r'factorial(\1)'),
                (r'(\d)(\()', r'\1*('), (r'(\))(\d)', r'\1*\2'), (r'(\))(\()', r'\1*\2')
            ]
            for pattern, replacement in subs:
                expression = re.sub(pattern, replacement, expression)

            # 3. Wrap all numbers in Fraction()
            expression = re.sub(r'(\d+\.?\d*)', r'Fraction("\1")', expression)
            
            expression += ')' * (expression.count('(') - expression.count(')'))
            result = safe_eval(expression)
            
            if isinstance(result, str) and result.startswith("Error:"):
                messagebox.showerror("Error", result)
            else:
                # --- Format output based on mode ---
                if self.output_mode == 'decimal':
                    output_str = str(float(result))
                else: # fraction mode
                    # Limit denominator for readability if it's a long approximation
                    output_str = str(Fraction(result).limit_denominator(10000))

                self.display.delete(0, tk.END)
                self.display.insert(0, output_str)
                self.master.after_idle(self.display.xview, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()