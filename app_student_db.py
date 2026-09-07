import streamlit as st
import sqlite3
import pandas as pd

# ==========================================
# DATABASE SETUP
# ==========================================

DB_NAME = "university.db"


def create_database():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL,
                grade TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        st.error(f"Database error: {e}")


# Create database when application starts
create_database()


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Student Academic Records",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Academic Records & Report Studio")


# ==========================================
# GRADE CALCULATION
# ==========================================

def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    else:
        return "D"


# ==========================================
# TWO TABS
# ==========================================

tab1, tab2 = st.tabs([
    "🎓 Register Student",
    "📊 Academic Reports"
])


# ==========================================
# TAB 1 - REGISTER STUDENT
# ==========================================

with tab1:

    st.header("Register a New Student")

    with st.form("student_form"):

        roll_no = st.number_input(
            "Roll Number",
            min_value=1,
            step=1
        )

        name = st.text_input(
            "Full Name"
        )

        department = st.selectbox(
            "Department",
            [
                "Computer Science",
                "Data Science",
                "Electronics",
                "Mechanical"
            ]
        )

        course = st.text_input(
            "Course Name"
        )

        marks = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            step=0.5
        )

        submitted = st.form_submit_button(
            "Register Student"
        )

    if submitted:

        if name.strip() == "":
            st.error("Please enter the student's full name.")

        elif course.strip() == "":
            st.error("Please enter the course name.")

        else:

            grade = calculate_grade(marks)

            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO students
                    (roll_no, name, department, course, marks, grade)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    roll_no,
                    name,
                    department,
                    course,
                    marks,
                    grade
                ))

                conn.commit()
                conn.close()

                st.success(
                    f"Student {name} registered successfully! "
                    f"Grade: {grade}"
                )

            except sqlite3.IntegrityError:
                st.error(
                    f"Roll Number {roll_no} already exists."
                )

            except sqlite3.Error as e:
                st.error(
                    f"Database error: {e}"
                )


# ==========================================
# TAB 2 - ACADEMIC REPORTS
# ==========================================

with tab2:

    st.header("📊 Academic Reports")

    report_option = st.selectbox(
        "Select Report Operation",
        [
            "All Students List",
            "Top Performers (≥ 75 Marks)",
            "Department-wise Average Marks",
            "Grade Breakdown Count",
            "Custom SQL Query"
        ]
    )

    # --------------------------------------
    # PREDEFINED QUERIES
    # --------------------------------------

    if report_option == "All Students List":

        query = """
SELECT * FROM students;
"""

    elif report_option == "Top Performers (≥ 75 Marks)":

        query = """
SELECT name, department, marks, grade
FROM students
WHERE marks >= 75
ORDER BY marks DESC;
"""

    elif report_option == "Department-wise Average Marks":

        query = """
SELECT department, AVG(marks) AS avg_marks
FROM students
GROUP BY department;
"""

    elif report_option == "Grade Breakdown Count":

        query = """
SELECT grade, COUNT(*) AS total_students
FROM students
GROUP BY grade;
"""

    else:

        query = st.text_area(
            "Enter your SQL Query",
            height=150,
            placeholder="Example: SELECT * FROM students;"
        )

    # --------------------------------------
    # EXECUTE QUERY
    # --------------------------------------

    if st.button("▶ Run Report"):

        if query.strip() == "":
            st.warning("Please enter or select a SQL query.")

        else:

            st.subheader("Executed SQL Query")

            st.code(
                query,
                language="sql"
            )

            try:

                conn = sqlite3.connect(DB_NAME)

                df = pd.read_sql_query(
                    query,
                    conn
                )

                conn.close()

                # --------------------------------------
                # DISPLAY TABLE
                # --------------------------------------

                st.subheader("📋 Report Results")

                if df.empty:

                    st.info(
                        "No records found for this report."
                    )

                else:

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    # --------------------------------------
                    # CHART CHECKBOX
                    # --------------------------------------

                    generate_chart = st.checkbox(
                        "Generate Chart Visualization"
                    )

                    if generate_chart:

                        # Find numerical columns
                        numeric_columns = df.select_dtypes(
                            include="number"
                        ).columns.tolist()

                        if len(numeric_columns) > 0:

                            st.subheader(
                                "📊 Chart Visualization"
                            )

                            st.bar_chart(
                                df[numeric_columns]
                            )

                        else:

                            st.warning(
                                "No numerical data available "
                                "for chart visualization."
                            )

            except sqlite3.Error as e:

                st.error(
                    f"Database error: {e}"
                )

            except Exception as e:

                st.error(
                    f"Error executing query: {e}"
                )