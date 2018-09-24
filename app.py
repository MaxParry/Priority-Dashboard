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

# delete existing tables (for debugging)
conn.execute(table_clients.delete())
conn.execute(table_affinities.delete())

table_clients = sqlalchemy.Table('clients', metadata, autoload=True)
table_affinities = sqlalchemy.Table('affinities', metadata, autoload=True)

# intialize app
app = Flask(__name__)

@app.route("/index")
def index():
    print('Someone has visited the index page')
    return "Welcome to the index page"

@app.route("/client_entry/<firstname>/<lastname>/<organization>/<market>/<relationships>/<bandwidth>/<mission>/<design_style>/<quality>/<opportunity>/<selection_process>/<x_factor>/<total>/<comments>")
def enter_client(name):
    # enter data into sqlite database columnwise
    new_client_dict = {'name': name}
    # new_client and new_affinity must be in dict
    conn.execute(table_clients.insert(), new_client_dict)
    print('Someone has entered data into the clients table')
    return "Welcome to the data entry page"

@app.route("/affinity_entry/<firstname>/<lastname>/<organization>/<market>/<relationships>/<bandwidth>/<mission>/<design_style>/<quality>/<opportunity>/<selection_process>/<x_factor>/<total>/<comments>")
def enter_affinity(firstname, lastname, organization, market, relationships, bandwidth, mission, design_style, quality, opportunity, selection_process, x_factor, total, comments):
    # build dict and insert into proper table
    new_affinity_dict = {'firstname': firstname,
                         'lastname': lastname,
                         'organization': organization,
                         'market': market,
                         'relationships': relationships,
                         'bandwidth': bandwidth,
                         'mission': mission,
                         'design_style': design_style,
                         'quality': quality,
                         'opportunity': opportunity,
                         'selection_process': selection_process,
                         'x_factor': x_factor,
                         'total': total,
                         'comments': comments}
    conn.execute(table_affinities.insert(), new_affinity_dict)
    print('Someone has entered data into the affinities table')
    return "Welcome to the data entry page"

@app.route("/dashboard")
def summary():
    # query existing sqlite database
    # these commands print data in console, can we store?
    clients_response = conn.execute('SELECT * FROM clients').fetchall()
    affinities_response = conn.execute('SELECT * FROM affinities').fetchall()
    # build dict from response
    all_response = {'clients_response': clients_response,
                    'affinities_response': affinities_response}
    # return json for website to render
    print('Someone has visited the dashboard page')
    return jsonify(all_response)

if __name__ == "__main__":
    app.run(debug=True)
