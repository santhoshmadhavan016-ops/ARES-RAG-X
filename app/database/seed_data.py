
import sqlite3
import random
from datetime import datetime, timedelta


DATABASE_PATH = "data/database/nova_corp.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

random.seed(42)


# =========================================================
# 1. DEPARTMENTS
# =========================================================

departments = [
    (1, "AI & Data Science", "Arun Kumar", "Chennai"),
    (2, "Sales", "Priya Sharma", "Bangalore"),
    (3, "Finance", "Rahul Menon", "Mumbai"),
    (4, "Human Resources", "Divya Raj", "Chennai"),
    (5, "Engineering", "Karthik Rao", "Hyderabad"),
    (6, "Marketing", "Sneha Iyer", "Bangalore")
]

cursor.executemany("""
INSERT OR IGNORE INTO departments
(department_id, department_name, manager, location)
VALUES (?, ?, ?, ?)
""", departments)


# =========================================================
# 2. EMPLOYEES
# =========================================================

first_names = [
    "Arun", "Rahul", "Karthik", "Vijay", "Suresh",
    "Priya", "Divya", "Sneha", "Anjali", "Meena",
    "Ravi", "Ajay", "Naveen", "Deepak", "Harish"
]

last_names = [
    "Kumar", "Sharma", "Rao", "Menon", "Iyer",
    "Raj", "Nair", "Reddy", "Singh", "Das"
]

roles = [
    "Data Scientist",
    "Software Engineer",
    "ML Engineer",
    "Data Analyst",
    "Sales Executive",
    "Financial Analyst",
    "HR Executive",
    "Marketing Executive",
    "Project Manager"
]

employees = []

for employee_id in range(1, 101):

    name = random.choice(first_names) + " " + random.choice(last_names)

    department_id = random.randint(1, 6)

    role = random.choice(roles)

    joining_date = datetime(
        random.randint(2018, 2025),
        random.randint(1, 12),
        random.randint(1, 28)
    ).strftime("%Y-%m-%d")

    salary = random.randint(30000, 150000)

    experience_years = round(random.uniform(0.5, 10), 1)

    performance_score = round(random.uniform(5, 10), 2)

    employees.append((
        employee_id,
        name,
        department_id,
        role,
        joining_date,
        salary,
        experience_years,
        performance_score
    ))

cursor.executemany("""
INSERT OR IGNORE INTO employees
(
    employee_id,
    name,
    department_id,
    role,
    joining_date,
    salary,
    experience_years,
    performance_score
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", employees)


# =========================================================
# 3. CUSTOMERS
# =========================================================

industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Retail",
    "Manufacturing",
    "Education",
    "Telecommunications",
    "Automotive"
]

regions = [
    "North",
    "South",
    "East",
    "West"
]

customers = []

for customer_id in range(1, 101):

    customer_name = f"Customer Company {customer_id}"

    industry = random.choice(industries)

    region = random.choice(regions)

    customer_value = round(
        random.uniform(10000, 500000),
        2
    )

    customers.append((
        customer_id,
        customer_name,
        industry,
        region,
        customer_value
    ))

cursor.executemany("""
INSERT OR IGNORE INTO customers
(
    customer_id,
    customer_name,
    industry,
    region,
    customer_value
)
VALUES (?, ?, ?, ?, ?)
""", customers)


# =========================================================
# 4. PROJECTS
# =========================================================

project_names = [
    "AI Analytics Platform",
    "Customer Intelligence System",
    "Sales Forecasting System",
    "Enterprise Data Warehouse",
    "Employee Performance Platform",
    "Fraud Detection System",
    "Marketing Automation",
    "Cloud Migration",
    "Recommendation Engine",
    "Business Intelligence Dashboard"
]

statuses = [
    "Planning",
    "In Progress",
    "Completed",
    "On Hold"
]

projects = []

for project_id in range(1, 31):

    project_name = random.choice(project_names) + f" {project_id}"

    department_id = random.randint(1, 6)

    start_date = datetime(
        random.randint(2023, 2026),
        random.randint(1, 12),
        random.randint(1, 28)
    )

    end_date = start_date + timedelta(
        days=random.randint(60, 700)
    )

    budget = round(
        random.uniform(100000, 5000000),
        2
    )

    status = random.choice(statuses)

    projects.append((
        project_id,
        project_name,
        department_id,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        budget,
        status
    ))

cursor.executemany("""
INSERT OR IGNORE INTO projects
(
    project_id,
    project_name,
    department_id,
    start_date,
    end_date,
    budget,
    status
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", projects)


# =========================================================
# 5. SALES
# =========================================================

products = [
    "AI Platform",
    "Cloud Services",
    "Data Analytics",
    "Cybersecurity",
    "Enterprise Software",
    "Consulting",
    "Machine Learning Solution",
    "Business Intelligence"
]

sales = []

for sale_id in range(1, 1001):

    employee_id = random.randint(1, 100)

    cursor.execute("""
    SELECT department_id
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))

    department_id = cursor.fetchone()[0]

    customer_id = random.randint(1, 100)

    sale_date = datetime(
        random.randint(2024, 2026),
        random.randint(1, 12),
        random.randint(1, 28)
    ).strftime("%Y-%m-%d")

    product = random.choice(products)

    quantity = random.randint(1, 20)

    revenue = round(
        random.uniform(5000, 200000),
        2
    )

    profit = round(
        revenue * random.uniform(0.10, 0.40),
        2
    )

    sales.append((
        sale_id,
        employee_id,
        department_id,
        customer_id,
        sale_date,
        product,
        quantity,
        revenue,
        profit
    ))

cursor.executemany("""
INSERT OR IGNORE INTO sales
(
    sale_id,
    employee_id,
    department_id,
    customer_id,
    sale_date,
    product,
    quantity,
    revenue,
    profit
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sales)


# =========================================================
# 6. ATTENDANCE
# =========================================================

attendance = []

attendance_id = 1

start_date = datetime(2025, 1, 1)

for employee_id in range(1, 101):

    for day in range(100):

        current_date = start_date + timedelta(days=day)

        status = random.choices(
            ["Present", "Absent", "Work From Home", "Half Day"],
            weights=[80, 5, 10, 5]
        )[0]

        if status == "Present":
            working_hours = round(random.uniform(7.5, 9.5), 1)

        elif status == "Work From Home":
            working_hours = round(random.uniform(7, 9), 1)

        elif status == "Half Day":
            working_hours = round(random.uniform(3.5, 5), 1)

        else:
            working_hours = 0

        attendance.append((
            attendance_id,
            employee_id,
            current_date.strftime("%Y-%m-%d"),
            status,
            working_hours
        ))

        attendance_id += 1

cursor.executemany("""
INSERT OR IGNORE INTO attendance
(
    attendance_id,
    employee_id,
    date,
    status,
    working_hours
)
VALUES (?, ?, ?, ?, ?)
""", attendance)


# =========================================================
# 7. LEAVE RECORDS
# =========================================================

leave_types = [
    "Casual Leave",
    "Sick Leave",
    "Annual Leave",
    "Emergency Leave",
    "Maternity/Paternity Leave"
]

leave_statuses = [
    "Approved",
    "Pending",
    "Rejected"
]

leave_records = []

for leave_id in range(1, 501):

    employee_id = random.randint(1, 100)

    leave_type = random.choice(leave_types)

    start = datetime(
        random.randint(2025, 2026),
        random.randint(1, 12),
        random.randint(1, 25)
    )

    duration = random.randint(1, 7)

    end = start + timedelta(days=duration)

    status = random.choices(
        leave_statuses,
        weights=[75, 15, 10]
    )[0]

    leave_records.append((
        leave_id,
        employee_id,
        leave_type,
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        status
    ))

cursor.executemany("""
INSERT OR IGNORE INTO leave_records
(
    leave_id,
    employee_id,
    leave_type,
    start_date,
    end_date,
    status
)
VALUES (?, ?, ?, ?, ?, ?)
""", leave_records)


# =========================================================
# 8. PERFORMANCE
# =========================================================

performance = []

review_periods = [
    "2024-Q1",
    "2024-Q2",
    "2024-Q3",
    "2024-Q4",
    "2025-Q1",
    "2025-Q2",
    "2025-Q3",
    "2025-Q4"
]

for performance_id in range(1, 501):

    employee_id = random.randint(1, 100)

    review_period = random.choice(review_periods)

    productivity_score = round(
        random.uniform(5, 10),
        2
    )

    quality_score = round(
        random.uniform(5, 10),
        2
    )

    rating = round(
        (productivity_score + quality_score) / 2,
        2
    )

    performance.append((
        performance_id,
        employee_id,
        review_period,
        productivity_score,
        quality_score,
        rating
    ))

cursor.executemany("""
INSERT OR IGNORE INTO performance
(
    performance_id,
    employee_id,
    review_period,
    productivity_score,
    quality_score,
    rating
)
VALUES (?, ?, ?, ?, ?, ?)
""", performance)


# =========================================================
# SAVE
# =========================================================

connection.commit()
connection.close()


print()
print("==========================================")
print("   NOVA CORP DATABASE POPULATED")
print("==========================================")
print("Departments    : 6")
print("Employees      : 100")
print("Customers      : 100")
print("Projects       : 30")
print("Sales          : 1000")
print("Attendance     : 10000")
print("Leave Records  : 500")
print("Performance    : 500")
print("==========================================")
print("All enterprise records generated!")
print("==========================================")

