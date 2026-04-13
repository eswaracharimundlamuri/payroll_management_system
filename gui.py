import tkinter as tk
from tkinter import messagebox

# import your existing class
from payroll import PayrollManagementSystem   # <-- save your backend as payroll.py


class PayrollGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")
        self.root.geometry("1000x450")

        # Initialize backend system (first load)

        self.system = PayrollManagementSystem()
        self.system.connect_oracle()
        self.system.load_s3_data()
        self.system.load_global_rules()

        # ---------------- UI ----------------
        self.label = tk.Label(root, text="Enter Employee Name", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Calculate Salary",fg="black",bg="green", command=self.calculate)
        self.button.pack(pady=10)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", fg="black",bg="yellow",command=self.reset_fields)
        self.reset_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit",fg="black",bg="red", command=root.quit)
        self.exit_button.pack(pady=5)

        self.result = tk.Text(root, height=15, width=60)
        self.result.pack(pady=10)

    # ---------------- BUTTON ACTION ----------------

    def calculate(self):
        emp_name = self.entry.get()

        if not emp_name:
            messagebox.showwarning("Input Error", "Please enter employee name")
            return

        try:
            #  Reset backend system each time (important fix)
            self.system = PayrollManagementSystem()
            self.system.connect_oracle()
            self.system.load_s3_data()
            self.system.load_global_rules()

            # Clear previous output
            self.result.delete(1.0, tk.END)

            # Process employee
            self.system.process_employee(emp_name)

            self.system.commit()

            # Show results
            output = f"""
Employee: {self.system.emp_name}
Designation: {self.system.designation}

Basic Salary: {self.system.basic_salary}
HRA: {round(self.system.hra, 2)}
DA: {round(self.system.da, 2)}
Special: {round(self.system.special, 2)}

Gross Salary: {round(self.system.gross, 2)}

PF: {round(self.system.pf, 2)}
Tax: {round(self.system.tax, 2)}
Cess: {round(self.system.cess, 2)}

Net Salary: {round(self.system.net, 2)}
"""

            self.result.insert(tk.END, output)

            #  Clear input for next entry
            self.entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- RESET FUNCTION ----------------
    def reset_fields(self):
        self.entry.delete(0, tk.END)
        self.result.delete(1.0, tk.END)



if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollGUI(root)
    root.mainloop()