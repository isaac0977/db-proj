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


DATABASEURI = "postgresql://is2661:7399@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

def rename_food(name):
  return name

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




def construct_single_query(tableName, statName, year):
  query = ''

  if (tableName=='occupation'):
    query = "SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, city_avg_wage as size from occupation g, city c, occupation_wages w where w.city_id=c.city_id and w.year={} and g.occupation_id=w.occupation_id and g.occupation_name='{}'".format(year, statName)
  elif (tableName=='house_rent' or tableName=='house_purchase'):
    bedroom = statName[0]
    bathroom = statName[2]
    statName = ''
    if (tableName == 'house_rent'):
      statName = 'rent_price'
    if (tableName == 'house_purchase'):
      statName = 'price'
    print(statName)
    query = "SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, avg({}) as size from {} g, city c where g.city_id=c.city_id and g.year={} and g.num_bedroom={} and g.num_bathroom={} GROUP BY c.city_id, c.x_coordinates, c.y_coordinates, c.city_name".format(statName, tableName, year, bedroom, bathroom)
  elif (tableName=='ingredient'):
    query = '''SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, price as size from {} g, city c where g.city_id=c.city_id
            and g.year={} and g.ingredient_name=\'{}\''''.format(tableName, year, statName)
  elif (tableName=='food'):
    query = '''SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, price as size from {} g, city c where g.city_id=c.city_id
            and g.year={} and g.food_name=\'{}\''''.format(tableName, year, statName)
  else :
    query = '''SELECT c.city_id, c.x_coordinates, c.y_coordinates, c.city_name, {} as size
          from {} g, city c where g.city_id=c.city_id and g.year={}'''.format(statName, tableName, year)

  return query;

def construct_multi_query(table1, table2, stat1, stat2, year):
  query1 = construct_single_query(table1, stat1, year)

  query2 = construct_single_query(table2, stat2, year)

  combinedQuery = '''
    SELECT query1.city_id, query1.x_coordinates, query1.y_coordinates, query1.city_name, query1.size as data1, query2.size as data2, query1.size/query2.size as size
    from ({}) query1, ({}) query2 where query1.city_id=query2.city_id'''.format(query1, query2)
  return combinedQuery



@app.route('/', methods=['GET', 'POST'])
def index():


  print(request.form)

  cursor = g.conn.execute("SELECT DISTINCT year FROM general_compensation order by year desc")
  years = []
  for result in cursor:
    years.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT occupation_name FROM occupation order by occupation_name asc")
  occupations = []
  for result in cursor:
    occupations.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT FORMAT('%%sB%%sB', num_bedroom, num_bathroom) structure from house_purchase")
  structures = []
  
  for result in cursor:
    structures.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT food_name from food_name order by food_name")
  foods = []
  
  for result in cursor:
    foods.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT ingredient_name from ingredient_name order by ingredient_name")
  ingredients = []
  
  for result in cursor:
    ingredients.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT ingredient_name from ingredient_creates_food c where c.food_name='Chicken Nuggets 6 Pieces'")
  nuggs = []
  
  for result in cursor:
    nuggs.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT ingredient_name from ingredient_creates_food c where c.food_name='Chicken Ceasar'")  
  salad = []
  
  for result in cursor:
    salad.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT ingredient_name from ingredient_creates_food c where c.food_name='Orange Chicken'")  
  orange = []
  
  for orange in cursor:
    orange.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT ingredient_name from ingredient_creates_food c where c.food_name='Crunch Wrap Supreme")  
  wrap = []
  
  for result in cursor:
    wrap.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT food_name from ingredient_creates_food c where c.ingredient_name='Panko'")  
  panko = []
  
  for result in cursor:
    panko.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT food_name from ingredient_creates_food c where c.ingredient_name='Chicken Thighs'")  
  thighs = []
  
  for result in cursor:
    thighs.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT food_name from ingredient_creates_food c where c.ingredient_name='Chicken Breast'")  
  breast = []
  
  for result in cursor:
    breast.append(result[0])  # can also be accessed using result[0]
  
  breast.close()

  cursor = g.conn.execute("SELECT DISTINCT food_name from ingredient_creates_food c where c.ingredient_name='Ground Beef'")  
  beef = []
  
  for result in cursor:
    beef.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  cursor = g.conn.execute("SELECT DISTINCT food_name from ingredient_creates_food c where c.ingredient_name='Lettuce'")  
  lettuce = []
  
  for result in cursor:
    lettuce.append(result[0])  # can also be accessed using result[0]
  
  cursor.close()

  context = dict(years = years, occupations=occupations, structures=structures, foods=foods, ingredients=ingredients, lettuce=lettuce, beef=beef, breast=breast, thighs=thighs, panko=panko, wrap=wrap, salad=salad, orange=orange, nuggs=nuggs)



  if request.method == "POST":
    if (request.form['year'] is not None and request.form['year'] is not ''):
        query =  ''
        statNameKey = 'macrostat-{}'.format(request.form['macrostat-table'])
        query = construct_single_query(request.form['macrostat-table'], request.form[statNameKey], int(request.form['year']))
        print(query)

        if (request.form['queryType'] == 'multi'):
            stateNameKey2 = ''
            if (request.form['macrostat-table2'] == 'ingredient' or request.form['macrostat-table2'] == 'food'):
              statNameKey2 = 'macrostat-{}2-{}'.format(request.form['macrostat-table2'], rename_food(request.form[statNameKey]))
            else:
              statNameKey2 = 'macrostat-{}2'.format(request.form['macrostat-table2'])
            query = construct_multi_query(request.form['macrostat-table'], request.form['macrostat-table2'], request.form[statNameKey], request.form[statNameKey2], int(request.form['year']))

        
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
