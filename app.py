from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.secret_key = "secret"

# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    # Is connected ?
    if 'username' in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    # Collect infos from form
    username = request.form["username"]
    password = request.form["password"]
    action = request.form["action"]
    
    if action == "signin":
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Identifiants incorrects", "danger")
    
    elif action == "signup":
        if User.query.filter_by(username=username).first():
            flash("Nom d'utilisateur déjà pris", "danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Inscription réussie", "success")
            return redirect(url_for("dashboard"))
    
    return render_template("signin.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)