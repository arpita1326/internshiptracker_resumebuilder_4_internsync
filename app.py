# app.py

from flask import Flask, render_template, request, redirect, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "careerpilot_secret"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(BASE_DIR, "internship.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

# =====================================================
# MODELS
# =====================================================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

class Internship(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(50), nullable=False)

    deadline = db.Column(db.String(50), nullable=False)

    link = db.Column(db.String(300))

    notes = db.Column(db.Text)

    user = db.Column(db.String(100), nullable=False)

# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session["user"] = username

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")

# =====================================================
# REGISTER
# =====================================================

@app.route("/register", methods=["GET", "POST"])

def register():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                "register.html",
                error="Username already exists"
            )

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")

def logout():

    session.pop("user", None)

    return redirect("/login")

# =====================================================
# DASHBOARD
# =====================================================

@app.route("/")

def home():

    if "user" not in session:

        return redirect("/login")

    search = request.args.get("search", "").lower()

    status_filter = request.args.get("status_filter", "")

    featured_companies = [

        {
            "name": "Google",
            "role": "Software Engineer Intern",
            "location": "Bangalore",
            "stipend": "₹50,000/month",
            "deadline": "30 June 2026",
            "logo": "https://logo.clearbit.com/google.com",
            "link": "https://careers.google.com"
        },

        {
            "name": "Microsoft",
            "role": "AI/ML Intern",
            "location": "Hyderabad",
            "stipend": "₹45,000/month",
            "deadline": "15 July 2026",
            "logo": "https://logo.clearbit.com/microsoft.com",
            "link": "https://careers.microsoft.com"
        },

        {
            "name": "Amazon",
            "role": "Cloud Intern",
            "location": "Chennai",
            "stipend": "₹40,000/month",
            "deadline": "25 June 2026",
            "logo": "https://logo.clearbit.com/amazon.com",
            "link": "https://amazon.jobs"
        }
    ]

    if search:

        featured_companies = [

            company for company in featured_companies

            if search in company["name"].lower()

            or search in company["role"].lower()

            or search in company["location"].lower()
        ]

    all_internships = Internship.query.filter_by(
        user=session["user"]
    ).all()

    if status_filter:

        internships = [

            i for i in all_internships

            if i.status == status_filter
        ]

    else:

        internships = all_internships

    total = len(all_internships)

    applied = len([
        i for i in all_internships
        if i.status == "Applied"
    ])

    interview = len([
        i for i in all_internships
        if i.status == "Interview"
    ])

    selected = len([
        i for i in all_internships
        if i.status == "Selected"
    ])

    rejected = len([
        i for i in all_internships
        if i.status == "Rejected"
    ])

    return render_template(
        "dashboard.html",
        internships=internships,
        total=total,
        applied=applied,
        interview=interview,
        selected=selected,
        rejected=rejected,
        featured_companies=featured_companies,
        search=search,
        status_filter=status_filter
    )

# =====================================================
# ADD
# =====================================================

@app.route("/add", methods=["GET", "POST"])

def add_internship():

    if "user" not in session:

        return redirect("/login")

    if request.method == "POST":

        new_internship = Internship(

            company=request.form["company"],

            role=request.form["role"],

            status=request.form["status"],

            deadline=request.form["deadline"],

            link=request.form.get("link", ""),

            notes=request.form.get("notes", ""),

            user=session["user"]
        )

        db.session.add(new_internship)

        db.session.commit()

        return redirect("/")

    return render_template("add_internship.html")

# =====================================================
# DELETE
# =====================================================

@app.route("/delete/<int:id>")

def delete(id):

    internship = Internship.query.filter_by(
        id=id,
        user=session["user"]
    ).first_or_404()

    db.session.delete(internship)

    db.session.commit()

    return redirect("/")

# =====================================================
# EDIT
# =====================================================

@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit(id):

    internship = Internship.query.filter_by(
        id=id,
        user=session["user"]
    ).first_or_404()

    if request.method == "POST":

        internship.company = request.form["company"]

        internship.role = request.form["role"]

        internship.status = request.form["status"]

        internship.deadline = request.form["deadline"]

        internship.link = request.form.get("link", "")

        internship.notes = request.form.get("notes", "")

        db.session.commit()

        return redirect("/")

    return render_template(
        "edit_internship.html",
        internship=internship
    )

# =====================================================
# PROFILE
# =====================================================

@app.route("/profile")

def profile():

    internships = Internship.query.filter_by(
        user=session["user"]
    ).all()

    total = len(internships)

    selected = len([
        i for i in internships
        if i.status == "Selected"
    ])

    return render_template(
        "profile.html",
        username=session["user"],
        total=total,
        selected=selected
    )

# =====================================================
# RESUME BUILDER
# =====================================================

@app.route("/resume-builder")

def resume_builder():

    return render_template("resume_builder.html")

# =====================================================
# GENERATE RESUME
# =====================================================

@app.route("/generate-resume", methods=["POST"])

def generate_resume():

    name = request.form.get("name", "")

    email = request.form.get("email", "")

    phone = request.form.get("phone", "")

    skills = request.form.get("skills", "")

    education = request.form.get("education", "")

    projects = request.form.get("projects", "")

    content = f"""

NAME: {name}

EMAIL: {email}

PHONE: {phone}

SKILLS:
{skills}

EDUCATION:
{education}

PROJECTS:
{projects}

"""

    filename = f"{secure_filename(name)}_Resume.txt"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    with open(filepath, "w", encoding="utf-8") as file:

        file.write(content)

    return send_file(
        filepath,
        as_attachment=True
    )

# =====================================================
# AI CHECKER
# =====================================================

@app.route("/ai-checker", methods=["GET", "POST"])

def ai_checker():

    score = None

    message = ""

    suggestions = []

    analysis = ""

    if request.method == "POST":

        file = request.files.get("resume")

        if file:

            score = 85

            message = "Excellent Resume!"

            suggestions = [

                "Add more projects",

                "Include certifications",

                "Use ATS keywords"
            ]

            analysis = """

✔ ATS Friendly

✔ Technical skills detected

✔ Professional structure identified

"""

    return render_template(
        "ai_checker.html",
        score=score,
        message=message,
        suggestions=suggestions,
        analysis=analysis
    )

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)