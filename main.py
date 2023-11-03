from flask import Flask, render_template
import util
import psycopg2
from psycopg2 import Error

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)

# evil global variables
# can be placed in a config file
# here is a possible tutorial how you can do this
username='willmath2002'
password='abc123'
host='127.0.0.1'
port='5432'
database='dvdrental'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/

@app.route('/api/update_basket_a')
# this is how you define a function in Python
def updatePage():
    
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    
    #SQL QUERY FOR INSERTING CHERRY
    sql_query = "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');"
    
    try:
        cursor.execute(sql_query)
        connection.commit()
        record = "Success!"
    except (Exception, Error) as error:
        record = error
    
    util.disconnect_from_db(connection,cursor)
    
    return render_template('update.html', log_html = record)

@app.route('/api/unique')
# this is how you define a function in Python
def index():
    # this is your index page
    # connect to DB
    cursor, connection = util.connect_to_db(username,password,host,port,database)
    
    #SQL QUERY FOR FINDING UNIQUE FRUIT
    sql_query = "SELECT fruit_a, fruit_b FROM basket_a FULL JOIN basket_b ON fruit_a = fruit_b WHERE a IS NULL OR b IS NULL"
    
    # execute SQL commands
    record = util.run_and_fetch_sql(cursor, sql_query)
    if record == -1:
        # you can replace this part with a 404 page
        print('Something is wrong with the SQL command')
    else:
        # this will return all column names of the select result table
        # ['customer_id','store_id','first_name','last_name','email','address_id','activebool','create_date','last_update','active']
        col_names = [desc[0] for desc in cursor.description]
        # only use the first five rows
        log = record[:5]
        # log=[[1,2],[3,4]]
    # disconnect from database
    util.disconnect_from_db(connection,cursor)
    # using render_template function, Flask will search
    # the file named index.html under templates folder
    return render_template('index.html', sql_table = log, table_title=col_names)


if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    app.run(host=ip)

