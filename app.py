# TODO for next iteration:

"""
What do we want to do with the website, what can the users do:
-they input their level,
-their date & time at which they want to sail,
-the kind of spot they are looking for (flat or waves)
    (level and plan d'eau are too correlated, need to figure out what to do with it),
- their main location
- the time they are willing to travel max

It gives them back a list of spots, plus a GPT generated discussion 
about pros and cons of each spot.
GPT.input : the request / the sublist of spots filtered and their comments.
GPT.output : the discussion about it, and recommended one.

How to get there now?

TODO:
- Finish the scraping of the data from thespot2be: 
    - Parse the big json file into list of spots
    - For each one of them, create a spot in the database (using gpt?)
    - Think how to store the spots optimally - so they can be easy to filter


- Add the new fields for the web app
- Make the web app prettier?
- Handle the GPT querying part with correct prompt engineering.
- Find a way to get wind information for each spot.

Think about the way the information is stored in the DB. Currently, every spot is
simply a city, for a level of winger, a type of plan d'eau, and the wind orientation

Ideally, now that we can scrape the data from thespot2be, it could be interesting 
to add comments



"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from db import get_spots, populate_db

app = Flask(__name__)


# Main page route
@app.route("/")
def main_page():
    return render_template("index.html")


if __name__ == "__main__":
    populate_db()
    # Initialize the database
    # Run the Flask app
    app.run(debug=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        level = request.form["level"]
        flat_waves = request.form["flat_waves"]
        city = request.form["city"]

        spots = get_spots(level, flat_waves, city)
        if spots:
            return render_template("index.html", results=spots[0])
        else:
            return render_template("index.html", results="None found")
    return render_template("index.html")
