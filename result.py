import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection

class ResultWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Student Results (Multiple Subjects)")
        self.root.geometry("700x800")
        self.root.configure(bg="#f5f5f5")

        # Title
        title = tk.Label(root, text="Add Student Results", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
        title.pack(fill="x", pady=10)

        # Form Frame
        form_frame = tk.Frame(root, bg="white", padx=20, pady=20, bd=1, relief="solid")
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Select Student
        tk.Label(form_frame, text="Select Student", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.student_var = tk.StringVar()
        self.student_cb = ttk.Combobox(form_frame, textvariable=self.student_var, state="readonly", width=30)
        self.student_cb.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(form_frame, text="Search", command=self.search_student).grid(row=0, column=2, padx=5, pady=5)
        self.load_students()

        # Name
        tk.Label(form_frame, text="Name", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.name_entry = ttk.Entry(form_frame, width=35)
        self.name_entry.grid(row=1, column=1, columnspan=2, pady=10)

        # Father's Name
        tk.Label(form_frame, text="Father's Name", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.father_name_entry = ttk.Entry(form_frame, width=35, state="readonly")
        self.father_name_entry.grid(row=2, column=1, columnspan=2, pady=10)

        # Subjects Frame
        subjects_frame = tk.LabelFrame(form_frame, text="Subjects and Marks", font=("Arial", 12), bg="white", padx=10, pady=10)
        subjects_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

        # Subject Entries
        self.subject_entries = []
        self.marks_entries = []
        self.total_marks_entries = []
        tk.Label(subjects_frame, text="Subject", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=5)
        tk.Label(subjects_frame, text="Marks Obtained", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=1, padx=5)
        tk.Label(subjects_frame, text="Total Marks", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=2, padx=5)

        for i in range(8):  # Create fields for 8 subjects
            subject_var = tk.StringVar()
            subject_cb = ttk.Combobox(subjects_frame, textvariable=subject_var, state="readonly", width=20)
            subject_cb.grid(row=i+1, column=0, pady=5, padx=5)
            self.load_courses(subject_cb)
            marks_entry = ttk.Entry(subjects_frame, width=12)
            marks_entry.grid(row=i+1, column=1, pady=5, padx=5)
            total_marks_entry = ttk.Entry(subjects_frame, width=12)
            total_marks_entry.grid(row=i+1, column=2, pady=5, padx=5)
            self.subject_entries.append(subject_cb)
            self.marks_entries.append(marks_entry)
            self.total_marks_entries.append(total_marks_entry)

        # Buttons
        btn_frame = tk.Frame(root, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Submit", command=self.submit_results).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side="left", padx=10)

    def load_students(self):
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT roll_no, name FROM students")
            students = [(f"{row['roll_no']} - {row['name']}") for row in cursor.fetchall()]
            self.student_cb["values"] = ["Select Student"] + students
            self.student_cb.current(0)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def load_courses(self, combobox):
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM courses")
            courses = [row["name"] for row in cursor.fetchall()]
            combobox["values"] = ["Select Course"] + courses
            combobox.current(0)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def search_student(self):
        selected_student = self.student_var.get()
        if selected_student == "Select Student":
            messagebox.showwarning("Warning", "Please select a student!")
            return

        roll_no, name = selected_student.split(" - ", 1)
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT father_name FROM students WHERE roll_no = ?", (roll_no,))
            student = cursor.fetchone()
            self.father_name_entry.delete(0, tk.END)
            self.father_name_entry.insert(0, student["father_name"])
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

        messagebox.showinfo("Search Result", f"Found student: {name}")

    def submit_results(self):
        student = self.student_var.get()
        if student == "Select Student":
            messagebox.showerror("Error", "Please select a student!")
            return

        roll_no, name = student.split(" - ", 1)
        valid_results = []

        for i in range(8):
            course = self.subject_entries[i].get()
            marks = self.marks_entries[i].get()
            total_marks = self.total_marks_entries[i].get()

            if course == "Select Course" or not marks or not total_marks:
                continue  # Skip empty or unselected fields

            try:
                marks = float(marks)
                total_marks = float(total_marks)
                if marks > total_marks:
                    messagebox.showerror("Error", f"Marks obtained cannot exceed total marks for {course}!")
                    return
                if marks < 0 or total_marks <= 0:
                    messagebox.showerror("Error", f"Invalid marks values for {course}!")
                    return
                percentage = (marks / total_marks) * 100
                valid_results.append((roll_no, name, course, marks, total_marks, percentage))
            except ValueError:
                messagebox.showerror("Error", f"Marks and Total Marks must be numbers for {course}!")
                return

        if not valid_results:
            messagebox.showerror("Error", "At least one subject with valid marks is required!")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            for result in valid_results:
                cursor.execute(
                    "INSERT INTO results (student_roll, name, course, marks_obtained, total_marks, percentage) VALUES (?, ?, ?, ?, ?, ?)",
                    result
                )
            conn.commit()
            messagebox.showinfo("Success", f"Results for {name} submitted successfully for {len(valid_results)} subject(s)!")
            self.clear_form()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {str(e)}. Check if student or course exists!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def clear_form(self):
        self.student_var.set("Select Student")
        self.name_entry.delete(0, tk.END)
        self.father_name_entry.delete(0, tk.END)
        for i in range(8):
            self.subject_entries[i].set("Select Course")
            self.marks_entries[i].delete(0, tk.END)
            self.total_marks_entries[i].delete(0, tk.END)