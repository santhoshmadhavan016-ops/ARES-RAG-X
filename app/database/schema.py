import sqlite3

DATABASE_PATH = "data/database/nova_corp.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    manager TEXT,
    location TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER,
    role TEXT,
    joining_date TEXT,
    salary REAL,
    experience_years REAL,
    performance_score REAL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    department_id INTEGER,
    customer_id INTEGER,
    sale_date TEXT,
    product TEXT,
    quantity INTEGER,
    revenue REAL,
    profit REAL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    date TEXT,
    status TEXT,
    working_hours REAL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_records (
    leave_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    leave_type TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS performance (
    performance_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    review_period TEXT,
    productivity_score REAL,
    quality_score REAL,
    rating REAL,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    department_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    budget REAL,
    status TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    industry TEXT,
    region TEXT,
    customer_value REAL
)
""")

connection.commit()
connection.close()

print("All enterprise tables created successfully!")