from sqlalchemy import create_engine, text
from sqlalchemy import *
import mysql.connector

db_connection_string = "mysql+pymysql://kkvtffkdk6kggcx53xwe:pscale_pw_ko5zYg2BkIQWYDPavNm3ccE73NR9kYc7UHTX3YL9L7J@ap-south.connect.psdb.cloud/carsharing?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_cardata_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from carhostdet"))
    result_dicts = []
    for row in result.all():
      result_dicts.append(row._asdict())
    for i in result_dicts:
      date1=i['startdate']
      date2=i['enddate']
  print(result_dicts)


def add_application_to_db(data):
  mydb = mysql.connector.connect(
  host="ap-south.connect.psdb.cloud",
  user="kkvtffkdk6kggcx53xwe", password="pscale_pw_ko5zYg2BkIQWYDPavNm3ccE73NR9kYc7UHTX3YL9L7J", database="carsharing")
  mycursor = mydb.cursor()

  sql = "INSERT INTO carhostdet (hostname,pickuppoint,hostmail,hphne,cbrand,cmodel,startdate,enddate) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
  val = (data["hostname"],data["hplace"],data["mail"],data["phno"],data["cbrand"],data["cmodel"],data["stdate"],data["endate"])
  mycursor.execute(sql, val)

  mydb.commit()
    
