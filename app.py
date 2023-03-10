from flask import Flask, render_template, request, jsonify
from database import load_cardata_from_db, add_application_to_db

app = Flask(__name__)
servicetypes1 = [{
  'id': 1,
  'Service_type': "Become a host",
  'Description': "Share your car with us and earn!!!",
  'Activity': "Share my car",
  'link': "Host"
}, {
  'id': 2,
  'Service_type': "Rent a car",
  'Description': "Rent a car and have a happy journey!!",
  'Activity': "Rent a car",
  'link': "User"
}]


@app.route("/")
def homepage():
  return render_template("home.html", servicetypes=servicetypes1)


@app.route("/Host")
def gethostdetails():
  return render_template("hostdetail.html")


@app.route("/User")
def getcarlist():
  return render_template("userdata.html")


@app.route("/host/apply", methods=['post'])
def getdata():
  data = request.form
  add_application_to_db(data)
  #return jsonify(data)
  return render_template('app_submitted.html', application=data)


if __name__ == "__main__":
  app.run('0.0.0.0', debug=True)
