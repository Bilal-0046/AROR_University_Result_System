import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection

class StudentWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Student Details")
        self.root.geometry("1000x500")
        self.root.config(bg="white")

        # Variables
        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.admission_var = tk.StringVar()
        self.father_name_var = tk.StringVar()
        self.exam_month_year_var = tk.StringVar()
        self.enrollment_var = tk.StringVar()
        self.year_semester_var = tk.StringVar()
        self.search_roll_var = tk.StringVar()

        # Title
        title = tk.Label(self.root, text="Manage Student Details", font=("Helvetica", 16, "bold"),
                         bg="#004d4d", fg="white")
        title.pack(side="top", fill="x")

        # Left Form
        form_frame = tk.Frame(self.root, bg="lightyellow", bd=2, relief=tk.RIDGE)
        form_frame.place(x=10, y=50, width=580, height=400)

        # Row 1
        tk.Label(form_frame, text="Roll No.", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.roll_var, width=20).grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="D.O.B (dd-mm-yyyy)", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.dob_var, width=20).grid(row=0, column=3, padx=10)

        # Row 2
        tk.Label(form_frame, text="Name", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.name_var, width=20).grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Contact No.", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.contact_var, width=20).grid(row=1, column=3, padx=10)

        # Row 3
        tk.Label(form_frame, text="Email", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.email_var, width=20).grid(row=2, column=1, padx=10)

        tk.Label(form_frame, text="Select Course", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.course_combo = ttk.Combobox(form_frame, textvariable=self.course_var, state="readonly", width=18)
        self.course_combo.grid(row=2, column=3, padx=10)
        self.load_courses()

        # Row 4
        tk.Label(form_frame, text="Gender", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly", width=18)
        gender_combo.grid(row=3, column=1, padx=10)

        tk.Label(form_frame, text="Admission Date", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.admission_var, width=20).grid(row=3, column=3, padx=10)

        # Row 5
        tk.Label(form_frame, text="Father's Name", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(form_frame, textvariable=self.father_name_var, width=20).grid(row=4, column=1, padx=10)

        tk.Label(form_frame, text="Exam Month/Year", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=4, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.exam_month_year_var, width=20).grid(row=4, column=3, padx=10)

        # Row 6
        tk.Label(form_frame, text="Enrollment", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.enrollment_var, width=20).grid(row=5, column=1, padx=10)

        tk.Label(form_frame, text="Year/Semester", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=5, column=2, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.year_semester_var, width=20).grid(row=5, column=3, padx=10)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=6, column=0, columnspan=4, pady=10)
        tk.Button(btn_frame, text="Save", width=10, bg="blue", fg="white", command=self.save_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=10, bg="green", fg="white", command=self.update_student).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=10, bg="red", fg="white", command=self.delete_student).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", width=10, bg="gray", fg="white", command=self.clear_form).grid(row=0, column=3, padx=5)

        # Right Search Panel
        search_frame = tk.Frame(self.root, bg="white")
        search_frame.place(x=600, y=50, width=380, height=50)

        tk.Label(search_frame, text="Search | Roll No.", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(search_frame, textvariable=self.search_roll_var, width=20).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", bg="#007acc", fg="white", width=10, command=self.search_student).grid(row=0, column=2, padx=5)

        # Table
        table_frame = tk.Frame(self.root, bg="white")
        table_frame.place(x=600, y=110, width=380, height=340)

        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.student_table = ttk.Treeview(table_frame, columns=("roll", "name", "email", "gender", "dob"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll No.")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="D.O.B")
        self.student_table["show"] = "headings"

        self.student_table.column("roll", width=80)
        self.student_table.column("name", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("gender", width=60)
        self.student_table.column("dob", width=80)

        self.student_table.pack(fill="both", expand=True)
        self.student_table.bind("<ButtonRelease-1>", self.select_student)

        self.load_students()

    def load_courses(self):
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM courses")
            courses = ["Select Course"] + [row["name"] for row in cursor.fetchall()]
            self.course_combo["values"] = courses
            self.course_combo.current(0)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error loading courses: {str(e)}")
        finally:
            if conn:
                conn.close()

    def save_student(self):
        roll_no = self.roll_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        dob = self.dob_var.get()
        contact = self.contact_var.get()
        course = self.course_var.get()
        admission_date = self.admission_var.get()
        father_name = self.father_name_var.get()
        exam_month_year = self.exam_month_year_var.get()
        enrollment = self.enrollment_var.get()
        year_semester = self.year_semester_var.get()

        if not all([roll_no, name, email, gender, dob, contact, course, admission_date, father_name, exam_month_year, enrollment, year_semester]):
            messagebox.showerror("Error", "Please fill all required fields!")
            return
        if course == "Select Course":
            messagebox.showerror("Error", "Please select a valid course!")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (roll_no, name, email, gender, dob, contact, course, admission_date, father_name, exam_month_year, enrollment, year_semester) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (roll_no, name, email, gender, dob, contact, course, admission_date, father_name, exam_month_year, enrollment, year_semester))
            conn.commit()
            self.load_students()
            self.clear_form()
            messagebox.showinfo("Success", "Student added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {str(e)}. Roll number or email may already exist!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def update_student(self):
        selected = self.student_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to update!")
            return

        roll_no = self.roll_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        dob = self.dob_var.get()
        contact = self.contact_var.get()
        course = self.course_var.get()
        admission_date = self.admission_var.get()
        father_name = self.father_name_var.get()
        exam_month_year = self.exam_month_year_var.get()
        enrollment = self.enrollment_var.get()
        year_semester = self.year_semester_var.get()

        if not all([roll_no, name, email, gender, dob, contact, course, admission_date, father_name, exam_month_year, enrollment, year_semester]):
            messagebox.showerror("Error", "Please fill all required fields!")
            return
        if course == "Select Course":
            messagebox.showerror("Error", "Please select a valid course!")
            return

        old_roll_no = self.student_table.item(selected)["values"][0]
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET roll_no = ?, name = ?, email = ?, gender = ?, dob = ?, contact = ?, course = ?, admission_date = ?, father_name = ?, exam_month_year = ?, enrollment = ?, year_semester = ? WHERE roll_no = ?",
                (roll_no, name, email, gender, dob, contact, course, admission_date, father_name, exam_month_year, enrollment, year_semester, old_roll_no))
            conn.commit()
            self.load_students()
            self.clear_form()
            messagebox.showinfo("Success", "Student updated successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Error: {str(e)}. Roll number or email may already exist!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def delete_student(self):
        selected = self.student_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return

        roll_no = self.student_table.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
        if confirm:
            try:
                conn = get_db_connection()
                if conn is None:
                    messagebox.showerror("Error", "Failed to connect to the database!")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
                conn.commit()
                self.load_students()
                self.clear_form()
                messagebox.showinfo("Success", "Student deleted successfully!")
            except sqlite3.OperationalError as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
            finally:
                if conn:
                    conn.close()

    def search_student(self):
        roll_no = self.search_roll_var.get().strip()
        self.student_table.delete(*self.student_table.get_children())

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            if roll_no:
                cursor.execute("SELECT roll_no, name, email, gender, dob FROM students WHERE roll_no = ?", (roll_no,))
            else:
                cursor.execute("SELECT roll_no, name, email, gender, dob FROM students")

            for row in cursor.fetchall():
                self.student_table.insert("", "end",
                                         values=(row["roll_no"], row["name"], row["email"], row["gender"], row["dob"]))
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def load_students(self):
        self.student_table.delete(*self.student_table.get_children())
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT roll_no, name, email, gender, dob FROM students")
            for row in cursor.fetchall():
                self.student_table.insert("", "end",
                                         values=(row["roll_no"], row["name"], row["email"], row["gender"], row["dob"]))
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def select_student(self, event):
        selected = self.student_table.selection()
        if selected:
            values = self.student_table.item(selected)["values"]
            self.roll_var.set(values[0])
            self.name_var.set(values[1])
            self.email_var.set(values[2])
            self.gender_var.set(values[3])
            self.dob_var.set(values[4])

            try:
                conn = get_db_connection()
                if conn is None:
                    messagebox.showerror("Error", "Failed to connect to the database!")
                    return
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM students WHERE roll_no = ?", (values[0],))
                student = cursor.fetchone()
                self.contact_var.set(student["contact"])
                self.course_var.set(student["course"])
                self.admission_var.set(student["admission_date"])
                self.father_name_var.set(student["father_name"])
                self.exam_month_year_var.set(student["exam_month_year"])
                self.enrollment_var.set(student["enrollment"])
                self.year_semester_var.set(student["year_semester"])
            except sqlite3.OperationalError as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
            finally:
                if conn:
                    conn.close()

    def clear_form(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.dob_var.set("")
        self.contact_var.set("")
        self.course_var.set("Select Course")
        self.admission_var.set("")
        self.father_name_var.set("")
        self.exam_month_year_var.set("")
        self.enrollment_var.set("")
        self.year_semester_var.set("")
        self.search_roll_var.set("")
        self.load_students()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentWindow(root)
    root.mainloop()