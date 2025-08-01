import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, get_db_connection
from course import CourseWindow
from student import StudentWindow
from result import ResultWindow
from view_result import ViewStudentResultWindow
from marksheet import MarksheetWindow
from logout import UserApp

class StudentResultSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Aror Student Result Management System")
        self.root.geometry("1200x700")  # Slightly larger window for better layout
        self.root.configure(bg="#F7F9FC")  # Softer off-white background
        self.root.resizable(True, True)  # Allow resizing for responsiveness

        # Initialize database
        init_db()

        # Configure ttk styles for professional look
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TButton",
            font=("Roboto", 11, "bold"),
            padding=12,
            background="#1E88E5",  # Modern blue
            foreground="white",
            borderwidth=0,
            relief="flat"
        )
        self.style.map(
            "TButton",
            background=[("active", "#1565C0"), ("disabled", "#B0BEC5")],  # Hover and disabled states
            foreground=[("active", "white")]
        )
        self.style.configure(
            "Sidebar.TButton",
            font=("Roboto", 10, "bold"),
            padding=10,
            anchor="w"  # Left-align text
        )

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0D47A1", height=80)  # Deep blue header
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="Aror University Student Result Management System",
            font=("Roboto", 20, "bold"),
            bg="#0D47A1",
            fg="white",
            pady=20
        ).pack()

        # Main Content Frame with Sidebar and Dashboard
        main_frame = tk.Frame(self.root, bg="#F7F9FC")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sidebar
        sidebar = tk.Frame(main_frame, bg="#263238", width=250)  # Dark sidebar
        sidebar.pack(side="left", fill="y", pady=10)
        sidebar.pack_propagate(False)

        # Sidebar Title
        tk.Label(
            sidebar,
            text="Menu",
            font=("Roboto", 14, "bold"),
            bg="#263238",
            fg="white",
            pady=15
        ).pack(fill="x")

        # Menu Buttons with Icons (simulated with text for simplicity)
        buttons = [
            ("🏛 Course", self.open_course_window),
            ("👩‍🎓 Student", self.open_student_window),
            ("📊 Result", self.open_result_window),
            ("🔍 View Results", self.view_results),
            ("📄 Marksheet", self.open_marksheet_window),
            ("🚪 Logout", self.logout),
            ("❌ Exit", self.root.quit)
        ]

        for btn_text, cmd in buttons:
            btn = ttk.Button(
                sidebar,
                text=btn_text,
                style="Sidebar.TButton",
                command=cmd
            )
            btn.pack(fill="x", padx=15, pady=5)
            # Add hover effect with background color change
            btn.bind("<Enter>", lambda e, b=btn: b.configure(style="TButton"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(style="Sidebar.TButton"))

        # Dashboard Frame
        dashboard_frame = tk.Frame(main_frame, bg="#F7F9FC")
        dashboard_frame.pack(side="right", fill="both", expand=True, padx=20)

        # Dashboard Title
        tk.Label(
            dashboard_frame,
            text="Dashboard Overview",
            font=("Roboto", 16, "bold"),
            bg="#F7F9FC",
            fg="#263238"
        ).pack(anchor="w", pady=(0, 20))

        # Dashboard Cards (Responsive Grid)
        cards_frame = tk.Frame(dashboard_frame, bg="#F7F9FC")
        cards_frame.pack(fill="both", expand=True)
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="card")

        self.create_dashboard_card(cards_frame, "Total Students", self.get_student_count(), "#E53935", 0)
        self.create_dashboard_card(cards_frame, "Total Courses", self.get_course_count(), "#1E88E5", 1)
        self.create_dashboard_card(cards_frame, "Total Results", self.get_result_count(), "#43A047", 2)

    def get_student_count(self):
        conn = get_db_connection()
        if conn is None:
            return 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_course_count(self):
        conn = get_db_connection()
        if conn is None:
            return 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_result_count(self):
        conn = get_db_connection()
        if conn is None:
            return 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM results")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def open_course_window(self):
        new_window = tk.Toplevel(self.root)
        CourseWindow(new_window)

    def open_student_window(self):
        new_window = tk.Toplevel(self.root)
        StudentWindow(new_window)

    def open_result_window(self):
        new_window = tk.Toplevel(self.root)
        ResultWindow(new_window)

    def view_results(self):
        new_window = tk.Toplevel(self.root)
        ViewStudentResultWindow(new_window)

    def open_marksheet_window(self):
        new_window = tk.Toplevel(self.root)
        MarksheetWindow(new_window)

    def logout(self):
        confirm = messagebox.askyesno(
            "Confirm Logout",
            "Are you sure you want to logout?",
            icon="question"
        )
        if confirm:
            self.root.destroy()
            root = tk.Tk()
            app = UserApp(root)
            root.mainloop()

    def create_dashboard_card(self, parent, title, count, color, col):
        # Card with shadow and hover effect
        card = tk.Frame(parent, bg="white", bd=0, relief="flat")
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        card.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        # Add subtle animation on hover
        def on_enter(e):
            card.configure(highlightbackground=color, highlightthickness=2)
            card.lift()  # Raise card for depth effect

        def on_leave(e):
            card.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        # Card content
        tk.Frame(card, bg=color, height=5).pack(side="top", fill="x")  # Colored top bar
        tk.Label(
            card,
            text=title,
            font=("Roboto", 13, "bold"),
            bg="white",
            fg="#263238",
            pady=10
        ).pack()
        tk.Label(
            card,
            text=str(count),
            font=("Roboto", 24, "bold"),
            bg="white",
            fg=color
        ).pack(pady=5)
        tk.Label(
            card,
            text="Records",
            font=("Roboto", 10),
            bg="white",
            fg="#546E7A"
        ).pack(pady=(0, 10))

if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()