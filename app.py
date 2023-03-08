from flask import Flask, render_template

app = Flask(__name__)
servicetypes1 = [{
  'id': 1,
  'Service_type': "Become a host",
  'Description': "Share your car with us and earn!!!",
  'Activity': "Share my car"
}, {
  'id': 2,
  'Service_type': "Rent a car",
  'Description': "Rent a car and have a happy journey!!",
  'Activity': "Rent a car"
}]


@app.route("/")
def homepage():
  return render_template("home.html", servicetypes=servicetypes1)


if __name__ == "__main__":
  app.run('0.0.0.0', debug=True)
