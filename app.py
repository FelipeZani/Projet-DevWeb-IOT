from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, inspect
from datetime import datetime
from static.application_modules.mailing import mailling
import os
import re

app= Flask(__name__)
# Makes sure user can't modify cookie and can't give him admin rights or other bad things ;)
app.secret_key = "xdhZ5enkMV4oBBBlR9ElADGbKPOba42gRtGVbiqnFrY4lRp3ez0DYh1oTmCqmTNxDlOrOrkPGcxhCzZEdH4W21OE2eCpkkMH2NRU"

# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
metadata = MetaData()

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    fname = db.Column(db.String(32), nullable=False)
    lname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    role = db.Column(db.String(6), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.today, nullable=False)

# Routes
@app.route("/")
def home():

    return render_template("home.html")
@app.route("/testing")
def testing():
    return render_template("testing.html")
@app.route("/signin")
def signin():
    session.clear() # avoid creating new account while still having session infos
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    if 'username' not in session or not session["verified"]:
        return redirect(url_for("home"))

    inspector = inspect(db.engine)
    tables = [table for table in inspector.get_table_names() if table not in ["user", "login_history"]]
    objects = {}

    metadata.reflect(bind=db.engine)

    with db.engine.connect() as conn:
        for table_name in tables:
            table = metadata.tables.get(table_name)
            if table is not None:
                query = table.select()
                result = conn.execute(query).fetchall()
                objects[table_name] = [dict(row._mapping) for row in result]

    return render_template("dashboard.html", objects=objects)


@app.route("/", methods=["POST","GET"])
def login():
    message = None
    list_messages = []
 
    # Collect infos from form
    username = request.form.get("username")
    password = request.form.get("password")
    action = request.form.get("action")
    

    if action == "signin":
            
            user = User.query.filter_by(username=username).first()
            if not user: # user doesnt exists
                message = "Incorrect username or password"
                list_messages.append({'sin-form':message})    
            elif check_password_hash(user.password, password) and user.is_verified:
                session["username"] = user.username
                session["fname"] = user.fname
                session["lname"] = user.lname
                session["gender"] = user.gender
                session["role"] = user.role
                session["birthdate"] = user.birthdate.strftime("%Y-%m-%d")
                session["level"] = user.level
                session["email"] = user.email
                session["verified"] = 1
                add_points(user.username, 1)
                log_user_login(user.username)
                return redirect(url_for('dashboard'))
            elif not user.is_verified:
                message = "You are not in the family yet, please wait for admin to accept you"
                list_messages.append({'nif':message})
            else:
                message = "Incorrect username or password"
                list_messages.append({'sin-form':message}) #add something here 
    elif action == "signup":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        gender = request.form.get("gender")
        role = request.form.get("role")
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        if not username or not email or not password or not role or not birthdate_str or not gender or not fname or not lname:
            message = "All fields must be filled"
            list_messages.append({'sup-form':message})
        if User.query.filter_by(username=username).first():
            message = "Username already taken"
            list_messages.append({'susername':message})
        if User.query.filter_by(email=email).first():
            message = "Email already taken"
            list_messages.append({'email':message})
        if gender not in ["male", "female"]:
            message = "Gender is incorrect"
            list_messages.append({'gender':message})
        if role not in ["parent", "child"]:
            message = "Role is incorrect"
            list_messages.append({'role':message})
        if birthdate > datetime.today().date():
            message = "You are not Marty McFly"
            list_messages.append({'nif':message})
        elif len(username) > 32 or len(username) < 3 or len(email) > 64 or len(email) < 3 or len(password) > 32  or len(password) < 0 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            message = "username, first name and last name are 32 chars max, email is 64 chars max"
            list_messages.append({"sup-form":message})
        if len(list_messages) == 0:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username, 
                fname=fname,
                lname=lname,
                email=email, 
                password=hashed_password,
                gender = gender,
                role=role,
                birthdate=birthdate,
                level=0,
                is_verified=0,
            )
            db.session.add(new_user)
            db.session.commit()
    return render_template("home.html", message=list_messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    if 'username' in session and session["verified"]:
        users = User.query.filter(User.username != session["username"], User.is_verified == 1).all()
        return render_template("profile.html", users=users)
    else :
        return redirect(url_for("home"))
    
@app.route("/user/<int:user_id>")
def user_profile(user_id):
    user = User.query.get(user_id)
    if user and user.is_verified:
        add_points(session["username"], 1)
        return render_template("user_profile.html", user=user)
    else:
        return redirect(url_for("profile"))

@app.route("/change_password", methods=["POST"])
def change_password():
    if 'username' not in session or not session["verified"]:
        return redirect(url_for('home'))

    user = User.query.filter_by(username=session['username']).first()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    # Checks if the current password is correct
    if not check_password_hash(user.password, current_password):
        session.clear()
        return redirect(url_for("signin", message="Old password is wrong. The password haven't been changed, please reconnect"))
    
    # makes sure new password is different from old one
    if new_password == current_password:
        session.clear()
        return redirect(url_for("signin", message="New password must be different from old one, please reconnect"))
    
    # generates new password
    user.password = generate_password_hash(new_password)
    db.session.commit()
    session.clear()
    
    return redirect(url_for("signin", message="Password sucessfully changed, please reconnect"))

@app.route('/change_email', methods=['POST'])
def change_email():
    if 'username' not in session or not session["verified"]:
        return redirect(url_for('home'))
    
    user = User.query.filter_by(username=session['username']).first()

    new_email = request.form.get('email')

    if User.query.filter_by(email=new_email).first():
        return redirect(url_for('profile', message="Email already taken"))

    user.email = new_email
    db.session.commit()

    return redirect(url_for('profile', message="Email successfully changed"))

@app.route("/admin_panel")
def admin_panel():
    if 'username'not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    users = User.query.filter(User.username != session["username"]).all()
    return render_template("admin_panel.html", users=users)

@app.route("/verify_user/<int:user_id>", methods=["POST"])
def verify_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    if user:
        user.is_verified = True
        db.session.commit()
    
    return redirect(url_for("admin_panel"))

@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for("admin_panel"))

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"]) # GET is the form, POST is for processing new data
def edit_user(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for("admin_panel"))

    if request.method == "POST":
        message = None 
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        gender = request.form.get("gender")
        role = request.form.get("role")
        level = int(request.form.get("level"))
        birthdate_str = request.form.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date() if birthdate_str else user.birthdate

        if not email or not gender or not fname or not lname or not birthdate_str or not role or level is None:
            message = "All fields must be œfilled"
        elif User.query.filter_by(email=email).first() and email != user.email:
            message = "Email already taken"
        elif gender not in ["male", "female"]:
            message = "Gender is incorrect"
        elif role not in ["parent", "child"]:
            message = "Role is incorrect"
        elif birthdate > datetime.today().date():
            message = "He is not Marty McFly"
        elif level < 0:
            message = "Level must be positive"
        elif len(email) > 64 or len(email) < 3 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            message = "Username, first name, and last name are 32 chars max, email is 64 chars max"
        
        if message: # if there is an error
            return render_template("edit_user.html", user=user, message=message)
        
        # no error means we can update infos
        user.fname = fname
        user.lname = lname
        user.email = email
        user.gender = gender
        user.role = role
        user.birthdate = birthdate
        user.level = level 
        db.session.commit()
        
        return redirect(url_for("admin_panel"))

    return render_template("edit_user.html", user=user)

@app.route("/view_login_history/<int:user_id>")
def view_login_history(user_id):
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    user = User.query.get(user_id)
    if user:
        history = LoginHistory.query.filter_by(username=user.username).order_by(LoginHistory.login_time.desc()).all()
        return render_template("view_login_history.html", history=history, user=user)
    else:
        return redirect(url_for("admin_panel"))

@app.route("/kill_admins", methods=["POST"]) # Removes admin rights of  everyone
def kill_admins():
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    users = User.query.filter(User.level >= 20, User.username != session["username"]).all()
    
    for user in users:
        user.level = 0
        db.session.commit()
    
    return redirect(url_for("admin_panel"))

@app.route("/backup_db", methods=["POST"])
def backup_db():
    db_path = 'instance/database.db'
    backup_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.db"
    backup_path = f"backups/{backup_filename}"
    
    try:
        if not os.path.exists('backups'):
            os.makedirs('backups')
        with open(db_path, 'rb') as source_db:
            with open(backup_path, 'wb') as backup_db:
                backup_db.write(source_db.read())
        return redirect(url_for('admin_panel', message="Sucessfully backed up database"))
    except :
        return redirect(url_for('admin_panel', message="Error while backing up"))

@app.route("/new_object", methods=["GET", "POST"])
def new_object():
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        table_name = request.form.get("table_name").strip()
        field_names = request.form.getlist("field_names[]")
        field_types = request.form.getlist("field_types[]")

        if not table_name or not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
            return render_template("new_object.html", message="Invalid table name format.")
        if not field_names:
            return render_template("new_object.html", message="Please add at least one field.")
        
        if len(set(field_names)) != len(field_names):
            return render_template("new_object.html", message="Field names must be unique.")

        columns = [Column("id", Integer, primary_key=True)]

        for field_name, field_type in zip(field_names, field_types):
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", field_name):
                return render_template("new_object.html", message=f"Invalid field name: {field_name}")
            
            if field_type == "Integer":
                columns.append(Column(field_name, Integer))
            elif field_type == "String":
                columns.append(Column(field_name, String(32)))
            elif field_type == "Boolean":
                columns.append(Column(field_name, Boolean))
            else:
                return render_template("new_object.html", message=f"Invalid field type: {field_type}")

        try:
            new_table = Table(table_name, metadata, *columns, extend_existing=True)
            new_table.create(db.engine)
        except Exception as e:
            return render_template("new_object.html", message=f"Error creating table: {str(e)}")

        return redirect(url_for("admin_panel", message="Successfully created new object type"))

    return render_template("new_object.html")

@app.route("/remove_object", methods=["GET", "POST"])
def remove_object():
    if 'username' not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        table_name = request.form.get("table_name").strip()
        
        if not table_name:
            return render_template("remove_object.html", message="Please enter a table name.")

        inspector = inspect(db.engine)
        if table_name in inspector.get_table_names():
            metadata.reflect(bind=db.engine)
            table = metadata.tables.get(table_name)

            if table is not None:
                table.drop(db.engine)
                return redirect(url_for("admin_panel", message="Successfully removed object type."))
            else:
                return render_template("remove_object.html", message="Table not found.")
        else:
            return render_template("remove_object.html", message="Table does not exist.")

    inspector = inspect(db.engine)
    all_tables = [table for table in inspector.get_table_names() if table not in ['user', 'login_history']]

    return render_template("remove_object.html", tables=all_tables)

@app.route("/add_object", methods=["GET", "POST"])
def add_object():
    if 'username' not in session:
        return redirect(url_for("login"))

    inspector = inspect(db.engine)
    tables = [table for table in inspector.get_table_names() if table not in ["user", "login_history"]]
    columns = []

    if request.method == "POST":
        table_name = request.form.get("table_name")
        if not table_name or table_name not in tables:
            return render_template("add_object.html", tables=tables, message="Invalid table selected.", columns=[])

        metadata.reflect(bind=db.engine)
        table = metadata.tables.get(table_name)

        if table is None:
            return render_template("add_object.html", tables=tables, message="Table not found.", columns=[])

        columns = [{"name": col.name, "type": str(col.type)} for col in table.columns if col.name != "id"]

        if "submit" in request.form:
            data = {}
            for col in columns:
                value = request.form.get(col["name"])
                if "BOOLEAN" in col["type"]:
                    data[col["name"]] = value == "True" # converts str True to Bool True
                else:
                    data[col["name"]] = value

            with db.engine.connect() as conn:
                conn.execute(table.insert().values(**data))
                conn.commit()

            return redirect(url_for('dashboard', message="Sucessfully added object"))

    return render_template("add_object.html", tables=tables, columns=columns)



@app.route("/delete_object/<table_name>/<int:object_id>", methods=["POST"])
def delete_object(table_name, object_id):
    if 'username' not in session:
        return redirect(url_for("login"))

    inspector = inspect(db.engine)
    if table_name not in inspector.get_table_names():
        return redirect(url_for("dashboard", message="Invalid table"))

    metadata.reflect(bind=db.engine)
    table = metadata.tables.get(table_name)

    if table is None:
        return redirect(url_for("dashboard", message="Table not found"))

    with db.engine.connect() as conn:
        query = table.delete().where(table.c.id == object_id)
        conn.execute(query)
        conn.commit()

    return redirect(url_for("dashboard"))


# Functions
def add_points(username, points):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return False 
    
    user.level += points
    db.session.commit()
    return True

def log_user_login(username):
    login_history = LoginHistory(username=username)
    db.session.add(login_history)
    db.session.commit()

# start server and init db
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)