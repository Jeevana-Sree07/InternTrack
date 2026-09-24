from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection
from datetime import date

app = Flask(__name__)


@app.route("/")
def home():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM Internship")
    total_internships = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM Application")
    total_applications = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM Application
        WHERE status = 'Interview'
    """)
    interviews = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM Application
        WHERE status = 'Selected'
    """)
    selected = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        total_internships=total_internships,
        total_applications=total_applications,
        interviews=interviews,
        selected=selected
    )


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
        SELECT skill_id, skill_name
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


@app.route("/apply/<int:internship_id>", methods=["GET", "POST"])
def apply(internship_id):

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

        student_id = request.form["student_id"]
        application_date = date.today()

        try:

            cursor.execute("""
                INSERT INTO Application
                (student_id, internship_id, application_date, status)
                VALUES (%s, %s, %s, 'Applied')
            """, (student_id, internship_id, application_date))

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

            return "Application failed. Please try again.", 400

    cursor.execute("""
        SELECT
            student_id,
            name,
            email,
            college
        FROM Student
        ORDER BY name
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "apply.html",
        internship=internship,
        students=students
    )


@app.route("/applications")
def applications():

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
        ORDER BY a.application_date DESC
    """)

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications=applications
    )


@app.route("/update-status/<int:application_id>", methods=["POST"])
def update_status(application_id):

    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE Application
            SET status = %s
            WHERE application_id = %s
        """, (status, application_id))

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("applications"))

    except Exception as error:

        connection.rollback()

        cursor.close()
        connection.close()

        return "Status update failed. Please try again.", 400


@app.route("/add-interview", methods=["GET", "POST"])
def add_interview():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        application_id = request.form["application_id"]
        round_number = request.form["round_number"]
        interview_date = request.form["interview_date"]
        result = request.form["result"]
        feedback = request.form["feedback"]

        try:

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
            """, (application_id,))

            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for("interviews_page"))

        except Exception as error:

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
        WHERE a.status IN ('Shortlisted', 'Interview')
        ORDER BY a.application_id
    """)

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_interview.html",
        applications=applications
    )


@app.route("/interviews")
def interviews_page():

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
        ORDER BY iv.interview_date
    """)

    interviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "interviews.html",
        interviews=interviews
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)