from flask import Flask, render_template
from sportsreference.ncaab.schedule import Schedule


app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Hello World"

@app.route("/players")
def players():
  return render_template('index.html')



if __name__ == '__main__':
    app.run()

