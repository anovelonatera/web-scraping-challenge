# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


# create route that renders index.html template
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    return render_template("index.html", mars_data=mars_data)

# create route that calls imports scrape_mars.py and calls scrape()
# Store the return value in Mongo as a Python dictionary.
@app.route("/scrape")
def scrape_results():
    mars_data = mongo.db.mars_data
    # Run scrape function
    mars_data_info = scrape_mars.scrape()
    # Update Mongo database
    mars_data.update({}, mars_data_info, upsert=True)

    # Back to home page
    return redirect('/', code=302)

@app.route("/about")
def about():
    return render_template('about.html')


# Call main func app
if __name__ == "__main__":
    app.run(debug=True)
