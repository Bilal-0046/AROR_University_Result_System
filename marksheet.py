import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime

class MarksheetWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Generate Marksheet")
        self.root.geometry("600x650")
        self.root.configure(bg="#f5f5f5")

        # Title
        title = tk.Label(self.root, text="Generate Student Marksheet", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
        title.pack(fill="x", pady=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg="#f5f5f5")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter Roll No.", font=("Arial", 12), bg="#f5f5f5").pack(side="left", padx=5)
        self.roll_no_var = tk.StringVar()
        self.roll_no_entry = ttk.Entry(search_frame, textvariable=self.roll_no_var, width=20)
        self.roll_no_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Generate", command=self.generate_marksheet).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Clear", command=self.clear_form).pack(side="left", padx=5)

        # Marksheet Display Frame
        self.display_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.display_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Marksheet Content
        self.student_label = tk.Label(self.display_frame, text="", font=("Arial", 12), bg="white", justify="left")
        self.student_label.pack(pady=10, anchor="w", padx=10)

        self.course_label = tk.Label(self.display_frame, text="", font=("Arial", 12), bg="white", justify="left")
        self.course_label.pack(pady=5, anchor="w", padx=10)

        # Table for marks
        self.table_frame = tk.Frame(self.display_frame, bg="white")
        self.table_frame.pack(pady=10, fill="x", padx=10)

        columns = ("S.No", "Course Code", "Course Title", "Max Marks", "Marks Obtained", "Grade", "GPA", "Credit Hours")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=70, anchor="center")

        self.tree.pack(fill="x", expand=True)

        self.gpa_label = tk.Label(self.display_frame, text="", font=("Arial", 12), bg="white", justify="left")
        self.gpa_label.pack(pady=5, anchor="w", padx=10)

        # Download Button
        ttk.Button(self.root, text="Download as PDF", command=self.download_pdf).pack(pady=10)

    def calculate_grade_and_gpa(self, percentage):
        """Calculate grade and GPA based on percentage."""
        if percentage >= 85:
            return "A", 4.00
        elif percentage >= 80:
            return "A-", 3.67
        elif percentage >= 75:
            return "B+", 3.33
        elif percentage >= 70:
            return "B", 3.00
        elif percentage >= 65:
            return "C+", 2.67
        elif percentage >= 60:
            return "C", 2.50
        elif percentage >= 50:
            return "D", 2.00
        else:
            return "F", 0.00

    def generate_marksheet(self):
        roll_no = self.roll_no_var.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Please enter a roll number!")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()

            # Fetch student details
            cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
            student = cursor.fetchone()

            # Fetch result details
            cursor.execute("SELECT * FROM results WHERE student_roll = ?", (roll_no,))
            results = cursor.fetchall()

            if not student or not results:
                messagebox.showerror("Error", "No student or results found for this roll number!")
                return

            # Prepare student info
            student_info = (
                f"Student Name: {student['name']}\n"
                f"Father's Name: {student['father_name']}\n"
                f"Reg. No.: {student['roll_no']}\n"
                f"Enrollment No.: {student['enrollment']}\n"
                f"Exam Month/Year: {student['exam_month_year']}\n"
                f"Year/Semester: {student['year_semester']}"
            )

            course_info = f"Department of Artificial Intelligence and Multimedia Gaming\nBS Artificial Intelligence"

            # Populate table with actual results
            self.tree.delete(*self.tree.get_children())
            table_data = []
            total_gpa = 0
            total_credit_hours = 0
            for i, result in enumerate(results, 1):
                percentage = result['percentage']
                grade, gpa = self.calculate_grade_and_gpa(percentage)
                credit_hours = 3 if "Th" in result['course'] else 1  # Example: Theory = 3 credits, Practical = 1 credit
                course_code = f"AI{i:03d}"  # Generate a simple course code
                table_data.append((
                    i,
                    course_code,
                    result['course'],
                    result['total_marks'],
                    result['marks_obtained'],
                    grade,
                    gpa,
                    credit_hours
                ))
                total_gpa += gpa * credit_hours
                total_credit_hours += credit_hours

            # Calculate overall GPA
            overall_gpa = total_gpa / total_credit_hours if total_credit_hours > 0 else 0

            for row in table_data:
                self.tree.insert("", "end", values=row)

            gpa_info = f"GPA: {overall_gpa:.2f}"

            # Update labels
            self.student_label.config(text=student_info)
            self.course_label.config(text=course_info)
            self.gpa_label.config(text=gpa_info)

            # Store data for PDF generation
            self.marksheet_data = {
                "roll_no": student['roll_no'],
                "name": student['name'],
                "father_name": student['father_name'],
                "enrollment": student['enrollment'],
                "exam_month_year": student['exam_month_year'],
                "year_semester": student['year_semester'],
                "course": "BS Artificial Intelligence",
                "table_data": table_data,
                "gpa": overall_gpa
            }
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def download_pdf(self):
        if not hasattr(self, 'marksheet_data'):
            messagebox.showwarning("Warning", "Please generate a marksheet first!")
            return

        roll_no = self.marksheet_data['roll_no']
        filename = f"marksheet_{roll_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 50, "AROR UNIVERSITY OF ART, ARCHITECTURE,")
        c.drawCentredString(width / 2, height - 70, "DESIGN & HERITAGE SUKKUR SINDH")
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 90, "MARKS SHEET")
        c.setFont("Helvetica", 12)
        c.drawRightString(width - 50, height - 90, f"Issue Date: {datetime.now().strftime('%d-%b-%y')}")

        # Course Info
        c.setFont("Helvetica", 12)
        y_position = height - 120
        c.drawString(50, y_position, "Department of Artificial Intelligence and Multimedia Gaming")
        c.drawString(50, y_position - 20, self.marksheet_data['course'])

        # Student Details
        y_position -= 50
        c.drawString(50, y_position, f"Student Name: {self.marksheet_data['name']}")
        c.drawString(300, y_position, f"Father's Name: {self.marksheet_data['father_name']}")
        y_position -= 20
        c.drawString(50, y_position, f"Reg. No.: {self.marksheet_data['roll_no']}")
        c.drawString(300, y_position, f"Enrollment No.: {self.marksheet_data['enrollment']}")
        y_position -= 20
        c.drawString(50, y_position, f"Exam Month/Year: {self.marksheet_data['exam_month_year']}")
        c.drawString(300, y_position, f"Year/Semester: {self.marksheet_data['year_semester']}")

        # Table
        y_position -= 40
        data = [["S.No", "C.Code", "Course Title(s)", "Max. Marks", "Marks Obt.", "Grade", "GPA", "Cr. Hrs."]]
        for row in self.marksheet_data['table_data']:
            data.append([str(row[0]), row[1], row[2], str(row[3]), str(row[4]), row[5], f"{row[6]:.2f}", str(row[7])])

        col_widths = [40, 60, 150, 60, 60, 40, 40, 50]
        row_height = 20
        c.setFont("Helvetica", 10)
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                x = 50 + sum(col_widths[:j])
                y = y_position - i * row_height
                c.rect(x, y, col_widths[j], row_height, stroke=1, fill=0)
                c.drawCentredString(x + col_widths[j] / 2, y + 5, item)

        # GPA
        y_position -= (len(data) * row_height + 20)
        c.setFont("Helvetica", 12)
        c.drawString(50, y_position, f"GPA: {self.marksheet_data['gpa']:.2f}")

        # Footer
        y_position -= 40
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y_position, "* This document is not valid without Signature and Seal.")
        y_position -= 20
        c.drawString(50, y_position, "* University reserves the right to correct any errors and omissions, if any.")
        c.drawCentredString(width / 2, 50, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        c.showPage()
        c.save()

        messagebox.showinfo("Success", f"Marksheet saved as {filename}")

    def clear_form(self):
        self.roll_no_var.set("")
        self.student_label.config(text="")
        self.course_label.config(text="")
        self.tree.delete(*self.tree.get_children())
        self.gpa_label.config(text="")
        if hasattr(self, 'marksheet_data'):
            del self.marksheet_data