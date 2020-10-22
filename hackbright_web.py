"""A web application for tracking projects, students, and student grades."""

from flask import Flask, redirect, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html", first=first,
                            last=last, github=github, grades=grades)

    return html
    


@app.route("/new-student-form")
def display_new_student_form():

    return render_template("new_student_creation.html")

@app.route("/new-student-creation", methods=["POST"])
def create_new_student():
    """Add a new student."""
    
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    github = request.form.get("github")
    hackbright.make_new_student(first, last, github)

    return render_template("confirmation.html", github=github)

@app.route("/project")
def find_project():
    """Show info about a project."""
    title = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(title)
    grades= hackbright.get_grades_by_title(title)

    return render_template("project_info.html", title = title, description=description,
                            max_grade=max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
