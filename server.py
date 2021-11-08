#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://is2661:7399@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

def rename_keys(row):
  if ('x_coordinates' in row):
    row['long'] = row.pop('x_coordinates')
  if ('y_coordinates' in row):
    row['lat'] = row.pop('y_coordinates')

  return row

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/', methods=['GET', 'POST'])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  print(request.form)

  cursor = g.conn.execute("SELECT DISTINCT year FROM general_compensation")
  years = []
  for result in cursor:
    years.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()
  context = dict(years = years)


  if request.method == "POST":
    if (request.form['year'] is not None and request.form['year'] is not ''):
        query =  ''
      

        if (request.form['macrostat'] == 'gross_earning') :
            query = '''SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, year, gross_earning as size
            from general_compensation g, city c WHERE g.city_id=c.city_id'''
            query = query + " and year={}".format(int(request.form['year']))

        if ('macrostat2' in request.form and request.form['macrostat2'] != ''):
            if (request.form['macrostat2'] == 'avg_unemployment_rate'):
    
              query = '''
              SELECT t.city_id, city_name, x_coordinates, y_coordinates, gross_earning as data1, avg_unemployment_rate data2, gross_earning/avg_unemployment_rate as size
              from city 
              INNER JOIN
              (
                SELECT c.city_id, gross_earning, avg_unemployment_rate
                FROM 
                  general_compensation
                  INNER JOIN (
                    SELECT 
                    city_id,
                    year,
                    avg_unemployment_rate
                  FROM 
                    employment
                  WHERE
                    year={}
                ) as c on general_compensation.city_id = c.city_id and general_compensation.year = c.year
                ) as t on t.city_id = city.city_id
              '''.format(int(request.form['year']))

        
        print(query)
        cursor = g.conn.execute(query)
        data = []
        for result in cursor:
          print(dict(result))
          data.append(rename_keys(dict(result)))
        cursor.close()
        context['query_data'] = data
        return render_template("index.html", **context)

        ##TODO: render index.html differently with the returned data
    else:
        ##TODO: this needs to be the default case
        pass

  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
