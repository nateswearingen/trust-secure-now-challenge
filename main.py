import mysql.connector
from flask import Flask
from flask import request
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


@app.route("/add_cust", methods=['POST', 'GET'])
def add_cust():
    #TODO
    return


@app.route("/update_cust", methods=['POST', 'GET'])
def update_cust():
    #TODO
    return


@app.route("/delete_cust", methods=['POST', 'GET'])
def delete_cust():
    #fetch id
    if id in request.form:
        cust_id = request.form['id']
    cust_id = request.args.get('id', '')
    if cust_id is None or cust_id == '':
        return "<p>You must supply a customer id.</p>"

    #check for existence
    cursor = cnx.cursor(buffered=True)
    query = "select 1 from customer c where c.id = %s"
    cursor.execute(query, [cust_id,])
    if cursor.rowcount != 1:
        cursor.close()
        return "<p>Unable to locate customer with that ID</p>"
    cursor.close()

    #delete
    cursor = cnx.cursor(buffered=True)
    query = "delete from customer c where c.id = %s"
    cursor.execute(query, [cust_id,])
    cnx.commit()
    out = str(cursor.rowcount) + " record deleted."
    cursor.close()
    return out


@app.route("/get_cust")
def get_cust():
    #fetch id
    if id in request.form:
        cust_id = request.form['id']
    cust_id = request.args.get('id', '')
    if cust_id is None or cust_id == '':
        return "<p>You must supply a customer id.</p>"

    cursor = cnx.cursor(buffered=True)
    query = "select * from customer c where c.id = %s"
    cursor.execute(query, [cust_id,])
    out = []
    for data in cursor:
        out.append(dict(zip([x[0] for x in cursor.description], data)))
    cursor.close()
    return out


@app.route("/")
def get_all_custs():
    cursor = cnx.cursor(buffered=True)
    query = "select * from customer"
    cursor.execute(query)
    out = []
    for data in cursor:
        out.append(dict(zip([x[0] for x in cursor.description], data)))
    cursor.close()
    return out
