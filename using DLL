__author__ = "Nadav"
""" calc that using functions inside a DLL file. gui by AI"""
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

# Load the DLL
mydll = ctypes.CDLL("./myDLL.dll")

# Define argument type and return types
mydll.add.argtypes = [ctypes.c_int, ctypes.c_int]
mydll.add.restype = ctypes.c_int

mydll.sub.argtypes = [ctypes.c_int, ctypes.c_int]
mydll.sub.restype = ctypes.c_int

mydll.mult.argtypes = [ctypes.c_int, ctypes.c_int]
mydll.mult.restype = ctypes.c_int

mydll.divide.argtypes = [ctypes.c_int, ctypes.c_int]
mydll.divide.restype = ctypes.c_float

mydll.isPrime.argtypes = [ctypes.c_int]
mydll.isPrime.restype = ctypes.c_bool

mydll.sqrtOfNum.argtypes = [ctypes.c_int]
mydll.sqrtOfNum.restype = ctypes.c_float


# --- Calculator Logic ---
def calculate():
    try:
        operation = combo_operation.get()

        # Special single-number operations
        if operation in ["√ (sqrt)", "Prime?"]:
            num = int(entry_num1.get().strip())

            if operation == "√ (sqrt)":
                result = mydll.sqrtOfNum(num)
                label_result.config(text=f"{result:.4f}")
            else:  # Prime?
                result = mydll.isPrime(num)
                label_result.config(text="Yes" if result else "No")
            return

        # Two-number operations
        a = int(entry_num1.get().strip())
        b = int(entry_num2.get().strip())

        if operation == "+":
            result = mydll.add(a, b)
        elif operation == "-":
            result = mydll.sub(a, b)
        elif operation == "×":
            result = mydll.mult(a, b)
        elif operation == "÷":
            if b == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                return
            result = mydll.divide(a, b)
        else:
            messagebox.showerror("Error", "Please select an operation")
            return

        label_result.config(text=str(result)[:7])

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_operation_change(event):
    """Show/hide second number field based on operation"""
    operation = combo_operation.get()
    if operation in ["√ (sqrt)", "Prime?"]:
        entry_num2.config(state="disabled")
        entry_num2.delete(0, tk.END)
    else:
        entry_num2.config(state="normal")



root = tk.Tk()
root.title("Calculator Using DLL")
root.geometry("800x300")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# Main frame
frame = tk.Frame(root, padx=30, pady=30, bg="#f0f0f0")
frame.pack(expand=True)

# Title
title_label = tk.Label(frame, text="Calculator", font=("Arial", 20, "bold"),
                       bg="#f0f0f0", fg="#333")
title_label.grid(row=0, column=0, columnspan=5, pady=(0, 20))

# Calculator row
# First number
entry_num1 = tk.Entry(frame, width=12, font=("Arial", 16), justify="center",
                      relief="solid", borderwidth=1)
entry_num1.grid(row=1, column=0, padx=5)

# Operation dropdown
combo_operation = ttk.Combobox(frame, width=10, font=("Arial", 14),
                               state="readonly", justify="center")
combo_operation['values'] = ('+', '-', '×', '÷', '√ (sqrt)', 'Prime?')
combo_operation.current(0)
combo_operation.grid(row=1, column=1, padx=5)
combo_operation.bind('<<ComboboxSelected>>', on_operation_change)

# Second number
entry_num2 = tk.Entry(frame, width=12, font=("Arial", 16), justify="center",
                      relief="solid", borderwidth=1)
entry_num2.grid(row=1, column=2, padx=5)

# Equals sign
label_equals = tk.Label(frame, text="=", font=("Arial", 20, "bold"),
                        bg="#f0f0f0", fg="#333")
label_equals.grid(row=1, column=3, padx=5)

# Result
label_result = tk.Label(frame, text="?", font=("Arial", 18, "bold"),
                        bg="white", fg="#2196F3", width=12, height=1,
                        relief="solid", borderwidth=1)
label_result.grid(row=1, column=4, padx=5)

# Calculate button
btn_calculate = tk.Button(frame, text="Calculate", command=calculate,
                          font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                          padx=20, pady=10, relief="raised", borderwidth=2,
                          cursor="hand2", activebackground="#45a049")
btn_calculate.grid(row=2, column=0, columnspan=5, pady=(30, 0))

# Instructions
instructions = tk.Label(frame,
                        text="Enter numbers, select operation, and click Calculate\n"
                             "√ and Prime? only use the first number",
                        font=("Arial", 9), bg="#f0f0f0", fg="#666")
instructions.grid(row=3, column=0, columnspan=5, pady=(15, 0))

# Focus on first entry
entry_num1.focus()

# Bind Enter key to calculate
root.bind('<Return>', lambda e: calculate())

# Run
root.mainloop()
