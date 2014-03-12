from flask import Flask, session, render_template, redirect, request, flash, url_for
import model
app = Flask(__name__)
app.secret_key = "maryhasalittlelamb?!....."

@app.route("/my_rating")
def my_rating():
    return render_template("my_rating.html")

@app.route("/user/<user_id>")
def user_movies_ratings(user_id):
    movie_ids = model.session.query(model.Rating).filter_by(user_id=user_id)
    movies = []

    for movie_id in movie_ids:
        u = movie_id.movie
        movies.append({"name":u.name, "rating":movie_id.rating})     

    return render_template("search_page.html", movies=movies)

@app.route("/")
def index():
    return render_template("new_user_signup.html")

@app.route("/user_list")
def user_list():
    user_list = model.session.query(model.User).limit(10).all()
    return render_template("user_list.html", users=user_list)

@app.route("/existing_user_login", methods=["POST"])
def existing_user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        existing = model.session.query(model.User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password!")
        return redirect(url_for("index"))

    #model.session['user_id'] = existing.id
    return redirect(url_for("user_list"))


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
        flash("This email already exists,Please select another one!")
        return redirect(url_for("index")) #redirect back to sign up page
    elif password != password_ver:
        flash("Your password do not match")
        return redirect(url_for("index")) #redirect back to sign up page
    else:
        new_user = model.User(email=email, password=password, age=age, zipcode=zipcode)
        model.session.add(new_user)
        model.session.commit()
      #  model.session['user_id'] = new_user.id
        return redirect(url_for("user_list")) 
 

if __name__ == "__main__":
    app.run(debug = True)