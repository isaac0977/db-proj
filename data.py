import os
import random
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
DATABASEURI = "postgresql://is2661:7399@35.196.73.133/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)


# adding new data for each year 2010 - 2018
def populate_employment_years():
    #insert data for each city for each year
    counter = 11
    incre = 1.5
    for year in range(2010,2020):
        for i in range(1,11):
            counter +=1
            # make it look like unemployment falling to about the correct amount rn (4%)
            incre /= 1.01
            rate = random.uniform(0.06,0.07) * incre
            print(year,i,rate)
            query = """INSERT INTO employment (employment_stat_id, city_id, year, avg_unemployment_rate) VALUES ('{stat_id}','{id}','{year}','{rate}' ) ;""".format(stat_id = counter, id=i, year = year, rate = rate)
            engine.execute(query) 

def populate_comp_years():
    #insert data for each city for each year
    counter = 1
    incre = 1.01
    gross = {
        1: 55000,
        2: 57000,
        3: 50000,
        4: 53000,
        5: 45000,
        6: 40000,
        7: 59000,
        8: 30000,
        9: 37000,
        10: 35000
    }
    hourly = {
        1: 30,
        2: 26,
        3: 20,
        4: 28,
        5: 22,
        6: 20,
        7: 31,
        8: 15,
        9: 20,
        10: 19
    }
    for year in range(2010,2021):
        for i in range(1,11):
            counter +=1
            # make it change / year
            incre += .003
            g = random.uniform(0.99,1.01) * incre * gross[i]
            h = random.uniform(0.99,1.01) * incre * hourly[i]
            idx = random.uniform(120,121) * incre
            print(year,i,'gross',g,'hourly',h, 'costindex',idx)
            query = """INSERT INTO general_compensation (wage_stat_id, city_id, year, employment_cost_index, gross_earning, average_earning) VALUES ('{stat_id}','{id}','{year}','{rate}','{gross}','{hr}' ) ;""".format(stat_id = counter, id=i, year = year, rate = idx, gross = g, hr = h)
            engine.execute(query) 

def populate_spending_years():
    counter = 1
    incre = 1.01
    city = {
       1: 40000,
        2: 42000,
        3: 25000,
        4: 30000,
        5: 27000,
        6: 30000,
        7: 45000,
        8: 12000,
        9: 15000,
        10: 17000 
    }
    for year in range(2010,2021):
        for i in range(1,11):
            counter +=1
            # make it look like chaning / year
            incre += .003
            g = random.uniform(0.99,1.01) * incre * city[i]
            print(counter, year,i,'avg spend',g)
            query = """INSERT INTO spending (spending_stat_id, city_id, year,avg_consumer_spending) VALUES ('{stat_id}','{id}','{year}','{spend}') ;""".format(stat_id = counter, id=i, year = year, spend = g)
            engine.execute(query) 

def populate_house_years():
    counter = 1
    incre = 1.01
    city = {
       1: [450000, 800, 1, 1],
        2: [350000, 1000, 1, 1],
        3: [200000, 1100, 1, 2],
        4: [250000, 1400, 2, 2],
        5: [300000, 900, 1, 1],
        6: [170000, 1600, 2, 2],
        7: [500000, 600, 1, 1],
        8: [125000, 2000, 2, 1],
        9: [150000, 1600, 2, 1],
        10: [130000, 1500, 2, 1],
    }
    for year in range(2010,2021):
        for i in range(1,11):
            counter +=1
            # make it look like chaning / year
            incre += .003
            p = random.uniform(0.99,1.01) * incre * city[i][0]
            print(counter, year,i,'avg price',p)
            query = """INSERT INTO house_purchase (home_stat_id, city_id, year, num_bedroom, num_bathroom, square_footage, price) VALUES ('{stat_id}','{id}','{year}','{bed}','{bath}', '{sq}', '{price}') ;""".format(stat_id = counter, 
            id=i, year = year, bed = city[i][2], bath=city[i][3], sq = city[i][1], price = p)
            engine.execute(query) 

def populate_rent_years():
    counter = 1
    incre = 1.01
    city = {
       1: [2700, 800, 1, 1],
        2: [2500, 1000, 1, 1],
        3: [2000, 1100, 1, 2],
        4: [1900, 1400, 2, 2],
        5: [1800, 900, 1, 1],
        6: [1400, 1600, 2, 2],
        7: [3100, 600, 1, 1],
        8: [1100, 2000, 2, 1],
        9: [1200, 1600, 2, 1],
        10: [1250, 1500, 2, 1],
    }
    for year in range(2010,2021):
        for i in range(1,11):
            counter +=1
            # make it look like chaning / year
            incre += .003
            p = random.uniform(0.99,1.01) * incre * city[i][0]
            print(counter, year,i,'rent price',p)
            query = """INSERT INTO house_rent (home_stat_id, city_id, year, num_bedroom, num_bathroom, square_footage, rent_price) VALUES ('{stat_id}','{id}','{year}','{bed}','{bath}', '{sq}', '{price}') ;""".format(stat_id = counter, 
            id=i, year = year, bed = city[i][2], bath=city[i][3], sq = city[i][1], price = p)
            engine.execute(query) 

# TODO - run appropriate insert queries after modifying above / as necessary
# ALREADY DONE
# populate_employment_years()
# populate_comp_years()
# populate_spending_years()
# populate_house_years()

# RUNNING HERE
populate_rent_years()
