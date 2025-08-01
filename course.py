import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection

class CourseWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Course Details")
        self.root.geometry("800x500")
        self.root.config(bg="white")

        self.course_name = tk.StringVar()
        self.duration = tk.StringVar()
        self.charges = tk.StringVar()
        self.search_var = tk.StringVar()

        title = tk.Label(self.root, text="Manage Course Details", font=("Helvetica", 16, "bold"), bg="#004d4d", fg="white")
        title.pack(side="top", fill="x")

        # Left Panel
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(x=20, y=60, width=350, height=350)

        tk.Label(form_frame, text="Course Name", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.course_name, width=30).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Duration", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.duration, width=30).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Charges", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.charges, width=30).grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Description", font=("Arial", 12, "bold"), bg="white").grid(row=3, column=0, sticky="nw", pady=5)
        self.description_box = tk.Text(form_frame, width=23, height=5)
        self.description_box.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Save", width=8, bg="blue", fg="white", command=self.save_course).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=8, bg="green", fg="white", command=self.update_course).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=8, bg="red", fg="white", command=self.delete_course).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", width=8, bg="gray", fg="white", command=self.clear_form).grid(row=0, column=3, padx=5)

        # Right Panel
        search_frame = tk.Frame(self.root, bg="white")
        search_frame.place(x=400, y=60, width=380, height=50)

        tk.Label(search_frame, text="Course Name", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var, width=20).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", bg="#007acc", fg="white", width=10, command=self.search_course).grid(row=0, column=2, padx=5)

        # Table
        table_frame = tk.Frame(self.root, bg="white")
        table_frame.place(x=400, y=120, width=380, height=300)

        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.course_table = ttk.Treeview(table_frame, columns=("id", "name", "duration", "charges", "desc"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.course_table.xview)
        scroll_y.config(command=self.course_table.yview)

        self.course_table.heading("id", text="Course ID")
        self.course_table.heading("name", text="Course Name")
        self.course_table.heading("duration", text="Duration")
        self.course_table.heading("charges", text="Charges")
        self.course_table.heading("desc", text="Description")
        self.course_table["show"] = "headings"

        self.course_table.column("id", width=80)
        self.course_table.column("name", width=100)
        self.course_table.column("duration", width=80)
        self.course_table.column("charges", width=80)
        self.course_table.column("desc", width=120)

        self.course_table.pack(fill="both", expand=True)
        self.course_table.bind("<ButtonRelease-1>", self.select_course)

        self.load_courses()

    def save_course(self):
        name = self.course_name.get().strip()
        duration = self.duration.get().strip()
        charges = self.charges.get().strip()
        description = self.description_box.get("1.0", tk.END).strip()

        if not all([name, duration, charges]):
            messagebox.showerror("Error", "Please fill all required fields!")
            return

        try:
            charges = float(charges)
            if charges < 0:
                messagebox.showerror("Error", "Charges cannot be negative!")
                return
        except ValueError:
            messagebox.showerror("Error", "Charges must be a valid number!")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                           (name, duration, charges, description))
            conn.commit()
            self.load_courses()
            self.clear_form()
            messagebox.showinfo("Success", "Course added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Course name already exists!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def update_course(self):
        selected = self.course_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to update!")
            return

        course_id = self.course_table.item(selected)["values"][0]
        name = self.course_name.get().strip()
        duration = self.duration.get().strip()
        charges = self.charges.get().strip()
        description = self.description_box.get("1.0", tk.END).strip()

        if not all([name, duration, charges]):
            messagebox.showerror("Error", "Please fill all required fields!")
            return

        try:
            charges = float(charges)
            if charges < 0:
                messagebox.showerror("Error", "Charges cannot be negative!")
                return
        except ValueError:
            messagebox.showerror("Error", "Charges must be a valid number!")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("UPDATE courses SET name = ?, duration = ?, charges = ?, description = ? WHERE course_id = ?",
                           (name, duration, charges, description, course_id))
            conn.commit()
            self.load_courses()
            self.clear_form()
            messagebox.showinfo("Success", "Course updated successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Course name already exists!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def delete_course(self):
        selected = self.course_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to delete!")
            return

        course_id = self.course_table.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this course?")
        if confirm:
            try:
                conn = get_db_connection()
                if conn is None:
                    messagebox.showerror("Error", "Failed to connect to the database!")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
                conn.commit()
                self.load_courses()
                self.clear_form()
                messagebox.showinfo("Success", "Course deleted successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
            finally:
                if conn:
                    conn.close()

    def search_course(self):
        search_term = self.search_var.get().strip()
        self.course_table.delete(*self.course_table.get_children())

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            if search_term:
                cursor.execute("SELECT * FROM courses WHERE name LIKE ?", ('%' + search_term + '%',))
            else:
                cursor.execute("SELECT * FROM courses")

            for row in cursor.fetchall():
                self.course_table.insert("", "end", values=(
                    row["course_id"], row["name"], row["duration"], row["charges"], row["description"]))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def load_courses(self):
        self.course_table.delete(*self.course_table.get_children())
        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            for row in cursor.fetchall():
                self.course_table.insert("", "end", values=(
                    row["course_id"], row["name"], row["duration"], row["charges"], row["description"]))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def select_course(self, event):
        selected = self.course_table.selection()
        if selected:
            values = self.course_table.item(selected)["values"]
            self.course_name.set(values[1])
            self.duration.set(values[2])
            self.charges.set(str(values[3]))
            self.description_box.delete("1.0", tk.END)
            self.description_box.insert("1.0", values[4] if values[4] else "")

    def clear_form(self):
        self.course_name.set("")
        self.duration.set("")
        self.charges.set("")
        self.description_box.delete("1.0", tk.END)
        self.search_var.set("")
        self.load_courses()

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseWindow(root)
    root.mainloop()