from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import pymysql
pymysql.install_as_MySQLdb()

Base = declarative_base()

# create potential_clients.sqlite database
engine = create_engine('sqlite:///potential_clients.sqlite')

# set up ORM templates
class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Affinities(Base):
    __tablename__ = 'affinities'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    organization = Column(String)
    market = Column(String)
    relationships = Column(Integer)
    bandwidth = Column(Integer)
    mission = Column(Integer)
    design_style = Column(Integer)
    quality = Column(Integer)
    opportunity = Column(Integer)
    selection_process = Column(Integer)
    x_factor = Column(Integer)
    total = Column(Integer)
    comments = Column(String)

# initiate mapping with create_all
conn = engine.connect()
Base.metadata.create_all(conn)

metadata = MetaData(bind=engine)
metadata.reflect()

table_clients = sqlalchemy.Table('clients', metadata, autoload=True)
table_affinities = sqlalchemy.Table('affinities', metadata, autoload=True)

#conn.execute(table_clients.delete())
#conn.execute(table_affinities.delete())


# intialize app
app = Flask(__name__)

@app.route("/index")
def index():
    print('Someone has visited the index page')
    return "Welcome to the index page"

@app.route("/entry/<firstname>/<lastname>/<organization>/<market>/<relationships>/<bandwidth>/<mission>/<design_style>/<quality>/<opportunity>/<selection_process>/<x_factor>/<total>/<comments>")
def enter_data(firstname, lastname, organization, market, relationships, bandwidth, mission, design_style, quality, opportunity, selection_process, x_factor, total, comments):
    # enter data into sqlite database columnwise
    #
    conn.execute(table_clients.insert(), new_client)
    conn.execute(table_affinities.insert(), new_affinity)
    #
    print('Someone has visited the data entry page')
    return "Welcome to the data entry page"

@app.route("/dashboard")
def summary():
    print('Someone has visited the dashboard page')
    # query existing sqlite database
    # these commands print data in console, can we store?
    conn.execute('SELECT * FROM clients').fetchall()
    conn.execute('SELECT * FROM affinities').fetchall()
    #
    # turn response to dict, then json for website to render
    return jsonify(some_dict)

if __name__ == "__main__":
    app.run(debug=True)
