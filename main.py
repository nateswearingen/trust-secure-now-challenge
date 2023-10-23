from flask import appcontext_tearing_down
import signal
import mysql.connector
from flask import Flask
app = Flask(__name__)

try:
    cnx = mysql.connector.connect(user='root', password='f5TuBZtZYZqWTopEXGyu',
                                  host='localhost',
                                  database='car-rentals')
except mysql.connector.Error as err:
    print(err)
    exit("Couldn't establish db connection")
else:
    print("Connection established!")

def close_db_connection(sender, **extra):
    print("Closing DB Connection")
    cnx.close()

@app.post("/add_cust")
def add_cust():
    #TODO
    return
@app.post("/update_cust")
def update_cust():
    #TODO
    return
@app.post("/delete_cust")
def delete_cust():
    #TODO
    return
@app.get("/get_cust")
def get_cust():
    cursor = cnx.cursor()
    query = "select * from customer c where c.id = "
    id = request.form['id']
    if id == None:
        id = request.args.get('id', '')
    cursor.execute(query, id)
    out = ""
    for t in cursor:
        out += "<p>" + str(t) + "</p>"
    return out

@app.route("/")
def get_all_custs():
    cursor = cnx.cursor()
    query = "select * from customer"
    cursor.execute(query)
    out = ""
    for t in cursor:
        out += "<p>" + str(t) + "</p>"
    return out