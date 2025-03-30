from flask import Flask, render_template, request, redirect, session, url_for,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, inspect, text
from static.application_modules.mailing.mailling import add_dict_confirmation_list,accounts_to_confirm,send_mail
from flask_mailman import Mail
from sqlalchemy.orm import joinedload
from datetime import datetime
from time import time
import os
import re
import uuid


app= Flask(__name__)
# Makes sure user can't modify cookie and can't give him admin rights or other bad things ;)
app.secret_key = "xdhZ5enkMV4oBBBlR9ElADGbKPOba42gRtGVbiqnFrY4lRp3ez0DYh1oTmCqmTNxDlOrOrkPGcxhCzZEdH4W21OE2eCpkkMH2NRU"

# SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
metadata = MetaData()


with app.app_context():
    db.create_all()


# Config Mailman
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "projetweb.iot@gmail.com"
app.config['MAIL_PASSWORD'] = "kpdm hdvx jtic fvul"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


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

class DelSuggestion(db.Model):
    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    username = Column(String, nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    objects = db.relationship('Object', backref='room', cascade='all, delete-orphan')

class Object(db.Model):
    __tablename__ = 'objects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    description = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)


# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin")
def signin():
    session.clear() # avoid creating new account while still having session infos
    return render_template("signin.html")

@app.route("/dashboard")
def dashboard():
    if 'username' not in session or not session.get("verified"): # Vérifie aussi verified
        # Si l'utilisateur n'est pas connecté ou vérifié, redirige vers la page d'accueil
        return redirect(url_for("home", message="Veuillez vous connecter pour accéder au tableau de bord."))

    # Récupérer les pièces pour le filtre
    rooms = Room.query.order_by(Room.name).all()

    # Récupérer tous les objets avec leurs informations de pièce (eager loading)
    objects_query = Object.query.options(joinedload(Object.room)).order_by(Object.name).all()

    # Préparer les données des objets pour le JavaScript (JSON)
    objects_data = []
    for obj in objects_query:
        objects_data.append({
            "id": obj.id,
            "name": obj.name,
            "type": obj.type or "N/A", # Fournir une valeur par défaut si None
            "description": obj.description or "", # Fournir une valeur par défaut si None
            "room_id": obj.room_id,
            "room_name": obj.room.name if obj.room else "Pièce inconnue" # Gérer le cas où la pièce n'existe plus
        })

    # Convertir en JSON pour le script dans le template
    import json
    objects_json = json.dumps(objects_data)

    # Rendre le template avec les données nécessaires
    return render_template("dashboard.html", rooms=rooms, objects_json=objects_json)

#Pour le login
@app.route("/login", methods=["POST"])
def login():
    # Collect form data from the frontend
    data = request.get_json()  # Getting data from the front
    username = data.get("username")
    password = data.get("password")
    action = data.get("action")
    
    # List for storing messages
    list_messages = []

    if action == "signin":
        user = User.query.filter_by(username=username).first()
        if not user:  # User does not exist
            list_messages.append({'sin-form': "Incorrect username or password"})
        elif check_password_hash(user.password, password) and user.is_verified:
            # Set session variables
            session["username"] = user.username
            session["fname"] = user.fname
            session["lname"] = user.lname
            session["gender"] = user.gender
            session["role"] = user.role
            session["birthdate"] = user.birthdate.strftime("%Y-%m-%d")
            session["level"] = user.level
            session["email"] = user.email
            session["verified"] = 1

            # Return a success message and redirect URL
            return jsonify({"success": True, "redirect": url_for('dashboard')}), 200
        elif not user.is_verified:
            list_messages.append({'nif': "You are not in the family yet, please wait for admin to accept you"})
        else:
            list_messages.append({'sin-form': "Incorrect username or password"})
    elif action == "signup":
        fname = data.get("fname") 
        lname = data.get("lname")
        email = data.get("email")
        gender = data.get("gender")
        role = data.get("role")
        birthdate_str = data.get("birthdate")
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()

        # Validate fields
        if not username or not email or not password or not role or not birthdate_str or not gender or not fname or not lname:
            list_messages.append({'sup-form': "All fields must be filled"})
        if User.query.filter_by(username=username).first():
            list_messages.append({'susername': "Username already taken"})
        if User.query.filter_by(email=email).first():
            list_messages.append({'email': "Email already taken"})
        if gender not in ["male", "female"]:
            list_messages.append({'gender': "Gender is incorrect"})
        if role not in ["parent", "child"]:
            list_messages.append({'role': "Role is incorrect"})
        if birthdate > datetime.today().date():
            list_messages.append({'nif': "You are not Marty McFly"})
        elif len(username) > 32 or len(username) < 3 or len(email) > 64 or len(email) < 3 or len(password) > 32  or len(password) < 0 or len(fname) < 3 or len(fname) > 32 or len(lname) < 3 or len(lname) > 32:
            list_messages.append({"sup-form": "Username, first name, last name, and email should have specified max lengths"})
        
        if not list_messages:
            
            #creating a dict structure to store the users data, and an index to in order to implement mail confirmation system:
            # user is sent a mail containing link (tokien validation), click on it will trigger the validation of the mail
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            user_sup_data = { #user data dict
                "username":username, 
                "fname":fname,
                "lname":lname,
                "email" : email, 
                "password" : hashed_password,
                "gender": gender,
                "role" : role,
                "birthdate" : birthdate,  
            }

            user_id = str(uuid.uuid4())[0:12] #get the first 12 characters of the id 
            
            add_dict_confirmation_list(user_id,user_sup_data)
            
            send_mail(email,fname,user_id)
           
            return jsonify({"success":True,"message":"Confirmation Mail Sent"}),200
        
    # If validation failed, return error messages to frontend
    return jsonify({"success": False, "messages": list_messages}),401

#After clicking on the link user will have its token verified, in case of success added to the data base
@app.route("/signup/<userid>")
def confirm_email(userid):

    try:   
        user_data = accounts_to_confirm[userid]
        new_user = User(
            username = user_data["username"], 
            fname = user_data["fname"],
            lname = user_data["lname"],
            email = user_data["email"], 
            password = user_data["password"],
            gender = user_data["gender"],
            role = user_data["role"],
            birthdate = user_data["birthdate"],
            level=0,
            is_verified=0,
        )

        db.session.add(new_user)
        db.session.commit()
        
        del accounts_to_confirm[userid]

        return render_template("home.html"), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Invalid registration token!\n Error: "}), 400

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
    
    suggestions = DelSuggestion.query.all()
    users = User.query.filter(User.username != session["username"]).all()
    return render_template("admin_panel.html", users=users, suggestions=suggestions)

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
    all_tables = [table for table in inspector.get_table_names() if table not in ['user', 'login_history', 'del_suggestion']]

    return render_template("remove_object.html", tables=all_tables)

#add_objet
@app.route("/add_object", methods=["GET", "POST"])
def add_object():
    if 'username' not in session:
        return redirect(url_for("login"))

    inspector = inspect(db.engine)
    tables = [table for table in inspector.get_table_names() if table not in ["user", "login_history", 'del_suggestion']]
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
    if 'username' not in session or not session["verified"]:
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

@app.route("/suggest_delete", methods=["POST"])
def suggest_delete():
    if "username" not in session or not session["verified"]:
        return redirect(url_for("home"))

    table_name = request.form.get("table_name")
    if not table_name:
        return redirect(url_for("dashboard", message="Invalid table name"))

    suggestion = DelSuggestion(table_name=table_name, username=session["username"])
    db.session.add(suggestion)
    db.session.commit()

    return redirect(url_for("dashboard", message="Delete suggestion sent !"))

@app.route("/delete_table", methods=["POST"])
def delete_table():
    if "level" not in session or session["level"] < 20 or not session["verified"]:
        return redirect(url_for("dashboard"))

    table_name = request.form.get("table_name")
    if not table_name:
        return redirect(url_for("admin_panel", message="Table name missing"))

    try:
        with db.engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            conn.commit()

        DelSuggestion.query.filter_by(table_name=table_name).delete()
        db.session.commit()

        return redirect(url_for("admin_panel", message="Deleted table successfully"))
    except Exception as e:
        return redirect(url_for("admin_panel", message=f"Error: {str(e)}"))

""" 
@app.route("/test_max", methods=["GET","POST"])
def config_maison():

    if 'username' not in session or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    return render_template("config_maison.html")
"""

@app.route("/config_maison", methods=["GET"])
def config_maison():
    rooms = Room.query.all()
    return render_template("config_maison.html", rooms=rooms, selected_room=None)

@app.route('/create_piece', methods=['POST'])
def create_piece():
    name = request.form.get('new_room')
    if name:
        new_room = Room(name=name)
        db.session.add(new_room)
        db.session.commit()
        rooms = Room.query.all()
    return redirect(url_for('config_maison'))

@app.route('/select_piece', methods=['GET'])
def select_piece():
    room_id = request.args.get('room_id')
    selected_room = Room.query.get(room_id)
    rooms = Room.query.all()
    return render_template("config_maison.html", rooms=rooms, selected_room=selected_room)

@app.route('/add_object2', methods=['POST'])
def add_object2():
    room_id = request.form.get('room_id')
    name = request.form.get('object_name')
    type_ = request.form.get('object_type')
    description = request.form.get('object_description')

    if room_id and name:
        new_object = Object(
            name=name,
            type=type_,
            description=description,
            room_id=room_id
        )
        db.session.add(new_object)
        db.session.commit()

    return redirect(url_for('select_piece', room_id=room_id))


@app.route('/delete_object2', methods=['POST'])
def delete_object2():
    object_id = request.form.get('object_id')
    room_id = request.form.get('room_id')

    obj = Object.query.get(object_id)
    if obj:
        db.session.delete(obj)
        db.session.commit()

    return redirect(url_for('select_piece', room_id=room_id))


@app.route('/delete_room2', methods=['POST'])
def delete_room2():
    room_id = request.form.get('room_id')
    print("ID de la pièce à supprimer :", room_id)  # DEBUG

    room = Room.query.get(room_id)
    if room:
        db.session.delete(room)
        db.session.commit()

    return redirect(url_for('config_maison'))

@app.route("/edit_object", methods=["GET", "POST"])
def edit_object():
    if 'username' not in session or not session["verified"]:
        return redirect(url_for("dashboard"))
    
    table_name = request.args.get("table_name") or request.form.get("table_name") # we need variables both from get and post
    object_id = request.args.get("object_id") or request.form.get("object_id")

    # makes sure table exists
    inspector = inspect(db.engine)
    valid_tables = inspector.get_table_names()
    if table_name not in valid_tables:
        return redirect(url_for("dashboard", message="Table does not exist"))

    metadata.reflect(bind=db.engine)
    table = metadata.tables.get(table_name)
    if table is None:
        return redirect(url_for("dashboard", message="Invalid table"))

    with db.engine.connect() as conn:
        query = table.select().where(table.c.id == object_id)
        result = conn.execute(query).fetchone()
        if result is None:
            return redirect(url_for("dashboard", message="Object not found"))

    object_data = dict(result._mapping)
    
    if request.method == "POST":
        new_data = {}
        for col in table.columns:
            if col.name != "id":  # do not modify id
                value = request.form.get(col.name)
                if value is not None:
                    # convert according to column type
                    if "INTEGER" in str(col.type) and value.isdigit():
                        new_data[col.name] = int(value)
                    elif "BOOLEAN" in str(col.type): # converts 1 and 0 to True and False
                        new_data[col.name] = value == "1"
                    else:
                        new_data[col.name] = value

        # update the object in the database
        with db.engine.connect() as conn:
            query = table.update().where(table.c.id == object_id).values(**new_data)
            conn.execute(query)
            conn.commit()

        return redirect(url_for("dashboard", message="object updated successfully!"))

    # get column info and their type for better form
    columns_info = []
    for col in table.columns:
        col_type = "text"
        if isinstance(col.type, Integer):
            col_type = "number"
        elif isinstance(col.type, Boolean):
            col_type = "boolean"
        
        columns_info.append({"name": col.name, "type": col_type})

    # display the form to modify the object
    return render_template("edit_object.html", table_name=table_name, object_id=object_id, object_data=object_data, columns_info=columns_info)


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