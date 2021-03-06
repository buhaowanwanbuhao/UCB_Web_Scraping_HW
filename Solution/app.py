from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


# Scraping Data
@app.route('/scrape')
def get():
    mars = mongo.db.mars
    data = scrape_mars.get_scraped_data()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


if __name__ == "__main__":
    app.run()