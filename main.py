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
    print("DB Connection established!")


def close_db_connection(sender, **extra):
    print("Closing DB Connection")
    cnx.close()


@app.route("/add_cust", methods=['POST', 'GET'])
def add_cust():
    ''' Api for adding a customer
    Extra fields are ignored.

    This currently doesn't support json inputs, but it needs to
    '''
    # get the columns in the customer table
    cursor = cnx.cursor(buffered=True)
    query = "select * from customer c limit 1"
    cursor.execute(query)
    data = {}
    for column, data_type in [(x[0], x[1]) for x in cursor.description]:
        if column == "id": #don't allow inserting the ID, as it's maintained by the database
            continue
        if column in request.form:
            field = request.form[column]
        else:
            field = request.args.get(column, '')
        if field is None or field == '':
            continue
        match mysql.connector.FieldType.get_info(data_type):
            case "VARCHAR":
                field = "'" + field + "'"
            case "VAR_STRING":
                field = "'" + field + "'"
            #TODO Insert support for the date datatype here, and whatever else gets implemented
        data[column] = field
    cursor.close()

    #business validations
    out = ""
    if "email" in data or "phone" in data or "address" in data:
        pass
    else:
        out += "At least one of phone, email, or address is required"
    if not "name" in data:
        out += "Name is a required field"
    if len(out) > 0:
        return out

    #build insert string
    query = "Insert into customer ("
    vals = ") values ("
    #vulnerable to SQL injection attack (out of time to rework)
    i = 0
    for k, v in data.items():
        if i > 0:
            query += ", "
            vals += ", "
        query += k
        vals += v
        i += 1
    query += vals + ")"

    cursor = cnx.cursor(buffered=True)
    cursor.execute(query)
    cnx.commit()
    out = str(cursor.rowcount) + " record(s) added."
    cursor.close()
    return out


@app.route("/update_cust", methods=['POST', 'GET'])
def update_cust():
    #TODO
    return


@app.route("/delete_cust", methods=['POST', 'GET'])
def delete_cust():
    #fetch id
    if 'id' in request.form:
        cust_id = request.form['id']
    else:
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
    if 'id' in request.form:
        cust_id = request.form['id']
    else:
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
