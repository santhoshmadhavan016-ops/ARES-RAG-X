import sqlite3
from pathlib import Path


class Text2SQL:

    def __init__(self, db_path=None):

        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "database"
                / "nova_corp.db"
            )

        self.db_path = str(db_path)

    # ======================================================
    # GET DATABASE SCHEMA
    # ======================================================

    def get_schema(self):

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = cursor.fetchall()

        schema = {}

        for table in tables:

            table_name = table[0]

            cursor.execute(
                f"PRAGMA table_info({table_name})"
            )

            columns = cursor.fetchall()

            schema[table_name] = [
                column[1]
                for column in columns
            ]

        connection.close()

        return schema

    # ======================================================
    # GET DEPARTMENT NAMES
    # ======================================================

    def get_departments(self):

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT department_name
            FROM departments
        """)

        departments = [
            row[0]
            for row in cursor.fetchall()
        ]

        connection.close()

        return departments

    # ======================================================
    # FIND DEPARTMENT FROM USER QUERY
    # ======================================================

    def find_department(self, query):

        query_lower = query.lower()

        departments = self.get_departments()

        # Normal department names
        for department in departments:

            if department.lower() in query_lower:
                return department

        # HR abbreviation
        if "hr" in query_lower:

            for department in departments:

                if department.lower() == "human resources":
                    return department

        return None

    # ======================================================
    # GENERATE SQL
    # ======================================================

    def generate_sql(self, query):

        query_lower = query.lower()

        # ==================================================
        # LEAVE-RELATED QUESTIONS
        # ==================================================
        # IMPORTANT:
        # This section comes BEFORE the general
        # "how many employees" condition.
        #
        # Otherwise:
        #
        # "How many employees are on leave?"
        #
        # would incorrectly become:
        #
        # SELECT COUNT(*) FROM employees
        # ==================================================

        leave_keywords = [
            "leave",
            "on leave",
            "leave records",
            "leave status",
            "employees on leave",
            "employee on leave",
            "vacation"
        ]

        has_leave_keyword = any(
            keyword in query_lower
            for keyword in leave_keywords
        )

        # --------------------------------------------------
        # COUNT EMPLOYEES ON LEAVE
        # --------------------------------------------------

        if (
            has_leave_keyword
            and (
                "how many" in query_lower
                or "number of" in query_lower
                or "count" in query_lower
                or "employees on leave" in query_lower
                or "employee on leave" in query_lower
            )
        ):

            return """
                SELECT COUNT(DISTINCT employee_id)
                AS employees_on_leave
                FROM leave_records
                WHERE LOWER(status) = 'approved';
            """

        # --------------------------------------------------
        # LIST LEAVE RECORDS
        # --------------------------------------------------

        if (
            has_leave_keyword
            and (
                "list" in query_lower
                or "show" in query_lower
                or "records" in query_lower
            )
        ):

            return """
                SELECT
                    leave_id,
                    employee_id,
                    leave_type,
                    start_date,
                    end_date,
                    status
                FROM leave_records
                ORDER BY start_date;
            """

        # ==================================================
        # EMPLOYEE COUNT
        # ==================================================

        if "how many employees" in query_lower:

            return """
                SELECT COUNT(*) AS employee_count
                FROM employees;
            """

        # ==================================================
        # AVERAGE SALARY IN A DEPARTMENT
        # ==================================================

        department = self.find_department(query)

        if (
            "average salary" in query_lower
            and department is not None
        ):

            safe_department = department.replace(
                "'",
                "''"
            )

            return f"""
                SELECT AVG(e.salary) AS average_salary
                FROM employees e
                JOIN departments d
                ON e.department_id = d.department_id
                WHERE d.department_name =
                '{safe_department}';
            """

        # ==================================================
        # GENERAL AVERAGE SALARY
        # ==================================================

        if "average salary" in query_lower:

            return """
                SELECT AVG(salary) AS average_salary
                FROM employees;
            """

        # ==================================================
        # HIGHEST SALARY
        # ==================================================

        if (
            "highest salary" in query_lower
            or "highest paid" in query_lower
        ):

            return """
                SELECT name, salary
                FROM employees
                ORDER BY salary DESC
                LIMIT 5;
            """

        # ==================================================
        # LOWEST SALARY
        # ==================================================

        if (
            "lowest salary" in query_lower
            or "lowest paid" in query_lower
        ):

            return """
                SELECT name, salary
                FROM employees
                ORDER BY salary ASC
                LIMIT 5;
            """

        # ==================================================
        # TOTAL REVENUE
        # ==================================================

        if "total revenue" in query_lower:

            return """
                SELECT SUM(revenue) AS total_revenue
                FROM sales;
            """

        # ==================================================
        # AVERAGE REVENUE
        # ==================================================

        if "average revenue" in query_lower:

            return """
                SELECT AVG(revenue) AS average_revenue
                FROM sales;
            """

        # ==================================================
        # NUMBER OF DEPARTMENTS
        # ==================================================

        if "how many departments" in query_lower:

            return """
                SELECT COUNT(*) AS department_count
                FROM departments;
            """

        # ==================================================
        # SALES EMPLOYEE COUNT
        # ==================================================

        if "sales employees" in query_lower:

            return """
                SELECT COUNT(*) AS employee_count
                FROM employees e
                JOIN departments d
                ON e.department_id = d.department_id
                WHERE d.department_name = 'Sales';
            """

        # ==================================================
        # DEPARTMENT WITH MOST EMPLOYEES
        # ==================================================

        if (
            "most employees" in query_lower
            or "highest number of employees"
            in query_lower
            or "largest department" in query_lower
        ):

            return """
                SELECT
                    d.department_name,
                    COUNT(e.employee_id)
                    AS employee_count
                FROM departments d
                LEFT JOIN employees e
                ON d.department_id = e.department_id
                GROUP BY d.department_name
                ORDER BY employee_count DESC
                LIMIT 1;
            """

        # ==================================================
        # EMPLOYEES IN EACH DEPARTMENT
        # ==================================================

        if "employees in each department" in query_lower:

            return """
                SELECT
                    d.department_name,
                    COUNT(e.employee_id)
                    AS employee_count
                FROM departments d
                LEFT JOIN employees e
                ON d.department_id = e.department_id
                GROUP BY d.department_name
                ORDER BY employee_count DESC;
            """

        # ==================================================
        # DYNAMIC DEPARTMENT EMPLOYEE SEARCH
        # ==================================================

        if department is not None:

            employee_search_phrases = [

                "employees in",
                "employees of",
                "show me all employees",
                "show all employees",
                "list employees"

            ]

            if any(
                phrase in query_lower
                for phrase in employee_search_phrases
            ):

                safe_department = department.replace(
                    "'",
                    "''"
                )

                return f"""
                    SELECT
                        e.employee_id,
                        e.name,
                        e.salary
                    FROM employees e
                    JOIN departments d
                    ON e.department_id =
                       d.department_id
                    WHERE d.department_name =
                    '{safe_department}'
                    ORDER BY e.name;
                """

        # ==================================================
        # GENERAL EMPLOYEE LIST
        # ==================================================

        if "list employees" in query_lower:

            return """
                SELECT
                    employee_id,
                    name,
                    salary
                FROM employees
                ORDER BY employee_id;
            """

        # ==================================================
        # IT DEPARTMENT SALARY
        # ==================================================

        if (
            "it department" in query_lower
            and "salary" in query_lower
        ):

            return """
                SELECT
                    e.employee_id,
                    e.name,
                    e.salary
                FROM employees e
                JOIN departments d
                ON e.department_id =
                   d.department_id
                WHERE d.department_name = 'IT';
            """

        # ==================================================
        # NO MATCH
        # ==================================================

        return None

    # ======================================================
    # EXECUTE SQL
    # ======================================================

    def execute_query(self, sql):

        if sql is None:
            return None

        connection = sqlite3.connect(
            self.db_path
        )

        cursor = connection.cursor()

        try:

            cursor.execute(sql)

            rows = cursor.fetchall()

            columns = [
                description[0]
                for description in cursor.description
            ]

            return {
                "columns": columns,
                "results": rows
            }

        except Exception as error:

            return {
                "error": str(error)
            }

        finally:

            connection.close()

