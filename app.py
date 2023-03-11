from flask import Flask, render_template, request
from database import load_cardata_from_db, add_application_to_db, listpossiblecars,returning_dict_of_possible_cars
import re, datetime

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

@app.route("/contactus")
def getcontactdetails():
  return render_template("contact.html")


@app.route("/User")
def getcarlist():
  return render_template("userdata.html")

@app.route("/Booked")
def succesfull():
  return render_template("booked.html")


@app.route("/user/rent", methods=['post'])
def putdata():
  reqdata = request.form
  place = reqdata['uplace']
  idlist = load_cardata_from_db(place)

  sdate1 = reqdata['stdate']
  edate1 = reqdata['endate']

  days1 = re.search('\d{4}-\d{2}-\d{2}', sdate1)
  reqdatestart = datetime.datetime.strptime(days1.group(), '%Y-%m-%d')
  days2 = re.search('\d{4}-\d{2}-\d{2}', edate1)
  reqdateend = datetime.datetime.strptime(days2.group(), '%Y-%m-%d')
  rstart = reqdatestart.date()
  rend = reqdateend.date()

  finalidlist = []

  for ids in idlist:
    id = listpossiblecars(ids, rstart, rend)
    if id > 0:
      daysrented=(rend-rstart).days
      finalidlist.append(id)
  if len(finalidlist) == 0:
    return render_template("carslist.html")
  else:
    listofdictofdata=returning_dict_of_possible_cars(finalidlist,daysrented)
    return render_template("listingcars.html",listofdictofdata=listofdictofdata)

 

@app.route("/host/apply", methods=['post'])
def getdata():
  amount = {
    "Punto": 1800,
    "Grande punto": 2140,
    "Avventura": 1680,
    "Ecosport": 1600,
    "Everest": 1250,
    "Ranger": 1570,
    "Amaze": 1600,
    "City": 1580,
    "Jazz": 1650,
    "Ace": 1200,
    "Nano": 1000,
    "ALTROZ": 1780,
    "Rapid style": 1400,
    "Rapid Elegance": 2310
  }
  data = request.form
  add_application_to_db(data)

  sdate = data['stdate']
  edate = data['endate']

  day = re.search('\d{4}-\d{2}-\d{2}', sdate)
  startdate = datetime.datetime.strptime(day.group(), '%Y-%m-%d').date()
  day2 = re.search('\d{4}-\d{2}-\d{2}', edate)
  enddate = datetime.datetime.strptime(day2.group(), '%Y-%m-%d').date()

  carmodel = data['cmodel']
  dayscalc = (enddate - startdate).days
  calcamnt = dayscalc * amount[carmodel]
  
  return render_template('app_submitted.html',
                         application=data,
                         amount=calcamnt,
                         dayscalc=dayscalc)


if __name__ == "__main__":
  app.run('0.0.0.0', debug=True)
