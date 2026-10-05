from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Change this to a long random secret before production
app.secret_key = "interntrack-secret-key-2026"


# ---------------- DASHBOARD ----------------

@app.route("/")
def home():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Total internships available
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM Internship
    """)
    total_internships = cursor.fetchone()["total"]

    # Personalized statistics
    if "student_id" in session:

        student_id = session["student_id"]

        # My applications
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Application
            WHERE student_id = %s
        """, (student_id,))

        total_applications = cursor.fetchone()["total"]

        # My interviews
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Interview iv
            JOIN Application a
                ON iv.application_id = a.application_id
            WHERE a.student_id = %s
        """, (student_id,))

        interviews = cursor.fetchone()["total"]

        # My selected applications
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Application
            WHERE student_id = %s
              AND status = 'Selected'
        """, (student_id,))

        selected = cursor.fetchone()["total"]

    else:

        total_applications = 0
        interviews = 0
        selected = 0

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        total_internships=total_internships,
        total_applications=total_applications,
        interviews=interviews,
        selected=selected
    )


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        college = request.form["college"].strip()
        graduation_year = request.form["graduation_year"]
        password = request.form["password"]

        if not name or not email or not password:
            return "Name, email and password are required.", 400

        if len(password) < 6:
            return "Password must contain at least 6 characters.", 400

        password_hash = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO Student
                (name, email, phone, college, graduation_year, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                name,
                email,
                phone,
                college,
                graduation_year,
                password_hash
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("login"))

        except Exception as error:

            connection.rollback()

            cursor.close()
            connection.close()

            if "Duplicate entry" in str(error):
                return "An account with this email already exists.", 400

            return f"Registration failed: {error}", 400

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                student_id,
                name,
                email,
                password_hash
            FROM Student
            WHERE email = %s
        """, (email,))

        student = cursor.fetchone()

        cursor.close()
        connection.close()

        if student and student["password_hash"]:

            if check_password_hash(
                student["password_hash"],
                password
            ):

                session["student_id"] = student["student_id"]
                session["student_name"] = student["name"]
                session["student_email"] = student["email"]

                return redirect(url_for("home"))

        return "Invalid email or password.", 401

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- INTERNSHIPS ----------------

@app.route("/internships")
def internships():

    skill = request.args.get("skill", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if skill:

        cursor.execute("""
            SELECT DISTINCT
                i.internship_id,
                i.title,
                i.description,
                i.stipend,
                i.deadline,
                c.company_name,
                c.location
            FROM Internship i
            JOIN Company c
                ON i.company_id = c.company_id
            JOIN Internship_Skill isk
                ON i.internship_id = isk.internship_id
            JOIN Skill s
                ON isk.skill_id = s.skill_id
            WHERE s.skill_name LIKE %s
            ORDER BY i.deadline
        """, ("%" + skill + "%",))

    else:

        cursor.execute("""
            SELECT
                i.internship_id,
                i.title,
                i.description,
                i.stipend,
                i.deadline,
                c.company_name,
                c.location
            FROM Internship i
            JOIN Company c
                ON i.company_id = c.company_id
            ORDER BY i.deadline
        """)

    internships = cursor.fetchall()

    cursor.execute("""
        SELECT
            skill_id,
            skill_name
        FROM Skill
        ORDER BY skill_name
    """)

    skills = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "internships.html",
        internships=internships,
        skills=skills,
        selected_skill=skill
    )


# ---------------- APPLY ----------------

@app.route("/apply/<int:internship_id>", methods=["GET", "POST"])
def apply(internship_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            i.internship_id,
            i.title,
            i.description,
            i.stipend,
            i.deadline,
            c.company_name,
            c.location
        FROM Internship i
        JOIN Company c
            ON i.company_id = c.company_id
        WHERE i.internship_id = %s
    """, (internship_id,))

    internship = cursor.fetchone()

    if internship is None:

        cursor.close()
        connection.close()

        return "Internship not found", 404

    if request.method == "POST":

        student_id = session["student_id"]
        application_date = date.today()

        try:

            cursor.execute("""
                INSERT INTO Application
                (student_id, internship_id, application_date, status)
                VALUES (%s, %s, %s, 'Applied')
            """, (
                student_id,
                internship_id,
                application_date
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("applications"))

        except Exception as error:

            connection.rollback()

            cursor.close()
            connection.close()

            if "Duplicate entry" in str(error):
                return "You have already applied for this internship.", 400

            if "Application deadline has passed" in str(error):
                return "The application deadline has passed.", 400

            return "Application failed. Please try again.", 400

    cursor.close()
    connection.close()

    return render_template(
        "apply.html",
        internship=internship
    )


# ---------------- APPLICATIONS ----------------

@app.route("/applications")
def applications():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.application_id,
            s.name AS student_name,
            c.company_name,
            i.title AS internship_title,
            a.application_date,
            a.status
        FROM Application a
        JOIN Student s
            ON a.student_id = s.student_id
        JOIN Internship i
            ON a.internship_id = i.internship_id
        JOIN Company c
            ON i.company_id = c.company_id
        WHERE a.student_id = %s
        ORDER BY a.application_date DESC
    """, (session["student_id"],))

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications=applications
    )


# ---------------- UPDATE STATUS ----------------

@app.route("/update-status/<int:application_id>", methods=["POST"])
def update_status(application_id):

    if "student_id" not in session:
        return redirect(url_for("login"))

    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE Application
            SET status = %s
            WHERE application_id = %s
              AND student_id = %s
        """, (
            status,
            application_id,
            session["student_id"]
        ))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("applications"))

    except Exception:

        connection.rollback()

        cursor.close()
        connection.close()

        return "Status update failed. Please try again.", 400


# ---------------- ADD INTERVIEW ----------------

@app.route("/add-interview", methods=["GET", "POST"])
def add_interview():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        application_id = request.form["application_id"]
        round_number = request.form["round_number"]
        interview_date = request.form["interview_date"]
        result = request.form["result"]
        feedback = request.form["feedback"]

        try:

            # Make sure the application belongs to the logged-in student
            cursor.execute("""
                SELECT application_id
                FROM Application
                WHERE application_id = %s
                  AND student_id = %s
            """, (
                application_id,
                session["student_id"]
            ))

            application = cursor.fetchone()

            if application is None:

                cursor.close()
                connection.close()

                return "Invalid application.", 403

            cursor.execute("""
                INSERT INTO Interview
                (application_id, round_number, interview_date, result, feedback)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                application_id,
                round_number,
                interview_date,
                result,
                feedback
            ))

            cursor.execute("""
                UPDATE Application
                SET status = 'Interview'
                WHERE application_id = %s
                  AND student_id = %s
            """, (
                application_id,
                session["student_id"]
            ))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("interviews_page"))

        except Exception:

            connection.rollback()

            cursor.close()
            connection.close()

            return "Interview creation failed. Please try again.", 400

    cursor.execute("""
        SELECT
            a.application_id,
            s.name AS student_name,
            c.company_name,
            i.title AS internship_title
        FROM Application a
        JOIN Student s
            ON a.student_id = s.student_id
        JOIN Internship i
            ON a.internship_id = i.internship_id
        JOIN Company c
            ON i.company_id = c.company_id
        WHERE a.student_id = %s
          AND a.status IN ('Shortlisted', 'Interview')
        ORDER BY a.application_id
    """, (session["student_id"],))

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_interview.html",
        applications=applications
    )


# ---------------- INTERVIEWS ----------------

@app.route("/interviews")
def interviews_page():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            iv.interview_id,
            s.name AS student_name,
            c.company_name,
            i.title AS internship_title,
            iv.round_number,
            iv.interview_date,
            iv.result,
            iv.feedback
        FROM Interview iv
        JOIN Application a
            ON iv.application_id = a.application_id
        JOIN Student s
            ON a.student_id = s.student_id
        JOIN Internship i
            ON a.internship_id = i.internship_id
        JOIN Company c
            ON i.company_id = c.company_id
        WHERE a.student_id = %s
        ORDER BY iv.interview_date
    """, (session["student_id"],))

    interviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "interviews.html",
        interviews=interviews
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )