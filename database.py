import sqlite3

def get_db_connection():
    conn = sqlite3.connect('AROR_University_Result_System.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')

    # Create students table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            gender TEXT NOT NULL,
            dob TEXT NOT NULL,
            contact TEXT NOT NULL,
            course TEXT NOT NULL,
            admission_date TEXT NOT NULL,
            father_name TEXT NOT NULL,
            exam_month_year TEXT NOT NULL,
            enrollment TEXT NOT NULL,
            year_semester TEXT NOT NULL
        )
    ''')

    # Check if enrollment column exists, and add it if it doesn't
    cursor.execute("PRAGMA table_info(students)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'enrollment' not in columns:
        cursor.execute('ALTER TABLE students ADD COLUMN enrollment TEXT NOT NULL DEFAULT ""')

    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            duration TEXT NOT NULL,
            charges REAL NOT NULL,
            description TEXT
        )
    ''')

    # Create results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_roll TEXT NOT NULL,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            marks_obtained REAL NOT NULL,
            total_marks REAL NOT NULL,
            percentage REAL NOT NULL,
            FOREIGN KEY (student_roll) REFERENCES students (roll_no),
            FOREIGN KEY (course) REFERENCES courses (name)
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
if __name__ == "__main__":
    init_db()