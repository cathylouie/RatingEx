import model
import csv
import datetime

def load_users(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, age, gender, occupation, zipcode = row
            id = int(id)
            age = int(age)
            u = model.User(id=id,
                           email=None,
                           password=None,
                           age=age,
                           zipcode=zipcode)
            session.add(u)
        session.commit()

def load_movies(session):
    # use u.item
    with open("seed_data/u.item") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id = int(row[0])
            name = row[1][0:-7]
            name = name.decode("latin-1")
            if row[2] != "":
                released_at = datetime.datetime.strptime(row[2], "%d-%b-%Y")
                imdb_url = row[4]

                u = model.Movie(id=id,
                            name=name,
                           released_at=released_at,
                           imdb_url=imdb_url)
                session.add(u)
        session.commit()

def load_ratings(session):
    # use u.data
    # user id | item id | rating | timestamp
    with open("seed_data/u.data") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            user_id, movie_id, rating, timestamp = row
            user_id = int(user_id)
            movie_id = int(movie_id)
            rating = int(rating)
            u = model.Rating(movie_id=movie_id,
                           user_id=user_id,
                           rating=rating)
            session.add(u)
        session.commit()
    

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
