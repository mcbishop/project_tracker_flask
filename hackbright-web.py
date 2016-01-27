from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student_search")
def get_student_form():
    """Shows the student search form"""

    return render_template("student_search.html")

@app.route("/add_student_form")
def add_student_form():
    """Shows the form for student input"""

    return render_template("student_add.html")


@app.route("/student_add", methods=['POST'])
def student_add():
    """Add a student."""

    # get information for new student from form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    # call the "add student function" from hackbright module with our info
    hackbright.make_new_student(first_name, last_name, github)


    #call student from database to confirm that student was added
    new_student = hackbright.get_student_by_github(github)

    # ensure that we render a template that lets the user name the
    # student they requested was added to DB successfully

    return render_template("added_student.html", 
        first=new_student[0], last=new_student[1], github=new_student[2])



@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    first, last, github = hackbright.get_student_by_github(github)
    student_grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", 
        first=first, last=last, github=github, grades=student_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
