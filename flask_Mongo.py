from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

db.mars_collection.drop()
db.mars_collection.insert(scrape_mars.scrape())

@app.route("/")
def home(): 

    # Find data
    mars_info = list(db.mars_collection.find())

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    db.mars_collection.drop()
    db.mars_collection.insert(scrape_mars.scrape())

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)