from flask import Flask, session, render_template, redirect, request, flash, url_for
import model
app = Flask(__name__)
app.secret_key = "maryhasalittlelamb?!....."

# @app.route("/user_list")
# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     print user_list
#     return render_template("user_list.html", users=user_list)
@app.route("/")
def index():
    return render_template("new_user_signup.html")

@app.route("/search_page")
def search_page():
    return render_template("search_page.html")

@app.route("/existing_user_login", methods=["POST"])
def existing_user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        existing = model.session.query(model.User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password!", "Error")
        return redirect(url_for("index"))

    #model.session['user_id'] = existing.id
    return redirect(url_for("search_page"))


@app.route("/new_user_signup", methods=["POST"])
def new_user_signup():
    email = request.form.get("email")
    password = request.form.get("password")
    password_ver = request.form.get("password_ver")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
#Verification if user already exists
    existing = model.session.query(model.User).filter_by(email=email).first()
    if existing:
        flash("This email already exists,Please select another one!", "Error")
        return redirect(url_for("index")) #redirect back to sign up page
    elif password != password_ver:
        flash("Your password do not match", "Error")
        return redirect(url_for("index")) #redirect back to sign up page
    else:
        new_user = model.User(email=email, password=password, age=age, zipcode=zipcode)
        model.session.add(new_user)
        model.session.commit()
      #  model.session['user_id'] = new_user.id
        return redirect(url_for("search_page")) 
 

if __name__ == "__main__":
    app.run(debug = True)