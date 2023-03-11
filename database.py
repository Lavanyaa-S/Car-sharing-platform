from sqlalchemy import create_engine, text
from sqlalchemy import *
import re, datetime
import mysql.connector

db_connection_string = "mysql+pymysql://kkvtffkdk6kggcx53xwe:pscale_pw_ko5zYg2BkIQWYDPavNm3ccE73NR9kYc7UHTX3YL9L7J@ap-south.connect.psdb.cloud/carsharing?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def returning_dict_of_possible_cars(idlist,days):
  with engine.connect() as conn:
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
    
  
    result = conn.execute(text("select * from carhostdet "))
    result_dicts = []
    for row in result.all():
      temp=row._asdict()
      if temp['id'] in idlist:
        model=temp['cmodel']
        amnt=days*amount[model]
        temp2={"amount":amnt}
        temp.update(temp2)
        result_dicts.append(temp)
  return result_dicts



def load_cardata_from_db(place):
  with engine.connect() as conn:
    result = conn.execute(text("select id,pickuppoint from carhostdet "))
    idlist=[]
    result_dicts = []
    for row in result.all():
      result_dicts.append(row._asdict())
    for i in result_dicts:
      if i["pickuppoint"]==place:
        idlist.append(i['id'])
  return idlist



def listpossiblecars(id,reqdatestart,reqdateend):
  mydb = mysql.connector.connect(host="ap-south.connect.psdb.cloud",user="kkvtffkdk6kggcx53xwe",password="pscale_pw_ko5zYg2BkIQWYDPavNm3ccE73NR9kYc7UHTX3YL9L7J",database="carsharing")
  mycursor = mydb.cursor()

  sql = "SELECT * FROM carhostdet WHERE id = %s"
  adr = (id, )

  mycursor.execute(sql, adr)

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

  myresult = mycursor.fetchall()
  if len(myresult)==0:
    return -9

  for x in myresult:
    savaildate=x[7]
    eavaildate=x[8]
    if reqdatestart<reqdateend:
      if savaildate<=reqdatestart<=eavaildate:
        if savaildate<=reqdateend<=eavaildate:
          return x[0]
        else:
          return -9
      else:
        return -9
    else:
      return -9
    

def add_application_to_db(data):
  mydb = mysql.connector.connect(
    host="ap-south.connect.psdb.cloud",
    user="kkvtffkdk6kggcx53xwe",
    password="pscale_pw_ko5zYg2BkIQWYDPavNm3ccE73NR9kYc7UHTX3YL9L7J",
    database="carsharing")
  mycursor = mydb.cursor()

  sql = "INSERT INTO carhostdet (hostname,pickuppoint,hostmail,hphne,cbrand,cmodel,startdate,enddate) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
  val = (data["hostname"], data["hplace"], data["mail"], data["phno"],
         data["cbrand"], data["cmodel"], data["stdate"], data["endate"])
  mycursor.execute(sql, val)

  mydb.commit()
