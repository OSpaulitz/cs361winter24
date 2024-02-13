from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "sneaky"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # users is the name of the table that we are referencing
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)


with app.app_context():
    db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))                              # these are the attributes
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/sample")
def sample():
    return render_template("sample.html")

@app.route("/register")
def register():
    return render_template("register.html")



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST": 
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()  # users is class, filter_by is property, first result **you can return multiple by using .all()**
        if found_user:                                         # use .delete() on next line db.session.commit() to delete a single user *use for loop for multiple
            session["email"] = found_user.email
            
        else:
            usr = users(user, None)
            db.session.add(usr)                                # adding to the database
            db.session.commit()                                        # if i don't have the commit it allows me to roll back database

        flash("Login Successful!", "info")
        return redirect(url_for("user"))
    
    else:    
        if "user" in session:
            flash("Already Logged In", "info")
            return redirect(url_for("user"))
        
        else:
            return render_template("login.html")
        

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()           # video 8 minute 6 for reference
            found_user.email = email
            db.session.commit()                            
            flash("Email was saved!")

        else:
            if "email" in session:
                email = session["email"]   

        return render_template("user.html", email=email)
    
    else:
        flash("You are not logged in", "info")
        return redirect(url_for("login"))
    
    
@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None) 
    return redirect(url_for("login"))

@app.route("/avocado_toast")
def avocado_toast():
    return render_template("avocado_toast.html")

@app.route("/albondiga_soup")
def albondiga_soup():
    return render_template("albondiga_soup.html")

@app.route("/summer_soup")
def summer_soup():
    return render_template("summer_soup.html")


if __name__ ==  "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)