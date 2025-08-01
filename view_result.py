import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection

class ViewStudentResultWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("View Student Result")
        self.root.geometry("700x400")
        self.root.configure(bg="#f5f5f5")

        # Title
        title = tk.Label(self.root, text="View Student Result", font=("Arial", 18, "bold"), bg="#FFA500", fg="black")
        title.pack(fill="x", pady=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="#f5f5f5")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search By Roll No.", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=5)
        self.roll_no_var = tk.StringVar()
        self.roll_no_entry = ttk.Entry(search_frame, textvariable=self.roll_no_var, width=20)
        self.roll_no_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_result).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)

        # Table Frame
        table_frame = tk.Frame(self.root, bg="#f5f5f5")
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview for displaying results
        columns = ("Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Delete Button
        ttk.Button(self.root, text="Delete", command=self.delete_result, style="Delete.TButton").pack(pady=10)

        # Style for Delete button
        style = ttk.Style()
        style.configure("Delete.TButton", foreground="white", background="red")
        style.map("Delete.TButton", background=[("active", "darkred")])

        self.load_results()

    def load_results(self):
        self.tree.delete(*self.tree.get_children())
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM results")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    row["student_roll"],
                    row["name"],
                    row["course"],
                    row["marks_obtained"],
                    row["total_marks"],
                    f"{row['percentage']:.2f}%"
                ))
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def search_result(self):
        roll_no = self.roll_no_var.get().strip()
        self.tree.delete(*self.tree.get_children())

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            if roll_no:
                cursor.execute("SELECT * FROM results WHERE student_roll = ?", (roll_no,))
            else:
                cursor.execute("SELECT * FROM results")

            for row in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    row["student_roll"],
                    row["name"],
                    row["course"],
                    row["marks_obtained"],
                    row["total_marks"],
                    f"{row['percentage']:.2f}%"
                ))
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def clear_search(self):
        self.roll_no_var.set("")
        self.load_results()

    def delete_result(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a result to delete!")
            return

        roll_no = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete result for Roll No: {roll_no}?")
        if confirm:
            try:
                conn = get_db_connection()
                if conn is None:
                    messagebox.showerror("Error", "Failed to connect to the database!")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM results WHERE student_roll = ?", (roll_no,))
                conn.commit()
                self.load_results()
                messagebox.showinfo("Success", "Result deleted successfully!")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
            finally:
                if conn:
                    conn.close()
