import os
from flask import Flask, render_template, jsonify, request, redirect
#################################
# OLD
#################################
# import sqlalchemy
# from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session

# import pymysql
# pymysql.install_as_MySQLdb()
#################################

# intialize app
app = Flask(__name__)

# setup Flask
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
db = SQLAlchemy(app)

#################################
# OLD
#################################

# Base = declarative_base()

# create potential_clients.sqlite database
# engine = create_engine('sqlite:///potential_clients.sqlite')
#################################

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Client %r>' % (self.name)

class Affinity(db.Model):
    __tablename__ = 'affinities'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    organization = db.Column(db.String(64))
    market = db.Column(db.String)
    relationships = db.Column(db.Integer)
    bandwidth = db.Column(db.Integer)
    mission = db.Column(db.Integer)
    design_style = db.Column(db.Integer)
    quality = db.Column(db.Integer)
    opportunity = db.Column(db.Integer)
    selection_process = db.Column(db.Integer)
    x_factor = db.Column(db.Integer)
    total = db.Column(db.Integer)
    comments = db.Column(db.String(64))

    def __repr__(self):
        return '<%r %r Affinity %r>' % (self.firstname,
                                        self.lastname,
                                        self.id)

# db.drop_all()
db.create_all()


#################################
# OLD
#################################
# initiate mapping with create_all
# conn = engine.connect()
# Base.metadata.create_all(conn)

# metadata = MetaData(bind=engine)
# metadata.reflect()

# delete existing tables (for debugging)
# conn.execute(table_clients.delete())
# conn.execute(table_affinities.delete())

# table_clients = sqlalchemy.Table('clients', metadata, autoload=True)
# table_affinities = sqlalchemy.Table('affinities', metadata, autoload=True)
################################

@app.route("/")
def home():
    print('Someone has visited the index page')
    # return render_template("index.html")
    return render_template("index.html")

@app.route("/send/client", methods=["GET", "POST"])
def send_client():
    if request.method == "POST":
        name = request.form["name"]

        new_client = Client(name=name)
        db.session.add(new_client)
        db.session.commit()
        return redirect("/", code=302)
    
    return render_template("form.html")

@app.route("/send/affinity", methods=["GET", "POST"])
def send_affinity():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        organization = request.form["organization"]
        market = request.form["market"]
        relationships = request.form["relationships"]
        bandwidth = request.form["bandwidth"]
        mission = request.form["mission"]
        design_style = request.form["design_style"]
        quality = request.form["quality"]
        opportunity = request.form["opportunity"]
        selection_process = request.form["selection_process"]
        x_factor = request.form["x_factor"]
        total = (int(relationships) + 
                 int(bandwidth) + 
                 int(mission) + 
                 int(design_style) +
                 int(quality) +
                 int(opportunity) +
                 int(selection_process) +
                 int(x_factor)
        )
        comments = request.form["comments"]
        
        new_affinity = Affinity(first_name=first_name,
                                last_name=last_name,
                                organization=organization,
                                market=market,
                                relationships=relationships,
                                bandwidth=bandwidth,
                                mission=mission,
                                design_style=design_style,
                                quality=quality,
                                opportunity=opportunity,
                                selection_process=selection_process,
                                x_factor=x_factor,
                                total=total,
                                comments=comments)
        db.session.add(new_affinity)
        db.session.commit()
        return redirect("/", code=302)
    
    return render_template("form.html")

# @app.route("/client_entry/<name>")
# def enter_client(name):
#     # enter data into sqlite database columnwise
#     new_client_dict = {'name': name}
#     # new_client and new_affinity must be in dict
#     conn.execute(table_clients.insert(), new_client_dict)
#     print('Someone has entered data into the clients table')
#     return "Welcome to the data entry page"

# @app.route("/affinity_entry/<firstname>/<lastname>/<organization>/<market>/<relationships>/<bandwidth>/<mission>/<design_style>/<quality>/<opportunity>/<selection_process>/<x_factor>/<total>/<comments>")
# def enter_affinity(firstname, lastname, organization, market, relationships, bandwidth, mission, design_style, quality, opportunity, selection_process, x_factor, total, comments):
#     # build dict and insert into proper table
#     new_affinity_dict = {'firstname': firstname,
#                          'lastname': lastname,
#                          'organization': organization,
#                          'market': market,
#                          'relationships': relationships,
#                          'bandwidth': bandwidth,
#                          'mission': mission,
#                          'design_style': design_style,
#                          'quality': quality,
#                          'opportunity': opportunity,
#                          'selection_process': selection_process,
#                          'x_factor': x_factor,
#                          'total': total,
#                          'comments': comments}
#     conn.execute(table_affinities.insert(), new_affinity_dict)
#     print('Someone has entered data into the affinities table')
#     return "Welcome to the data entry page"

# @app.route("/dashboard")
# def summary():
#     # query existing sqlite database
#     # these commands print data in console, can we store?
#     clients_response = conn.execute('SELECT * FROM clients').fetchall()
#     affinities_response = conn.execute('SELECT * FROM affinities').fetchall()
#     # build dict from response
#     all_response = {'clients_response': clients_response,
#                     'affinities_response': affinities_response}
#     # return json for website to render
#     print('Someone has visited the dashboard page')
#     return jsonify(all_response)

@app.route("/api/clients")
def serve_clients():
    results = db.session.query(Client.name).all()

    client_names = [result[0] for result in results]

    clients_data = [{
        "clients": client_names
    }]

    return jsonify(clients_data)

@app.route("/api/affinities")
def serve_affinities():
    results = db.session.query(Affinity.first_name,
                               Affinity.last_name,
                               Affinity.organization,
                               Affinity.market,
                               Affinity.relationships,
                               Affinity.bandwidth,
                               Affinity.mission,
                               Affinity.design_style,
                               Affinity.quality,
                               Affinity.opportunity,
                               Affinity.selection_process,
                               Affinity.x_factor,
                               Affinity.total,
                               Affinity.comments).all()

    first_name_list = [result[0] for result in results]
    last_name_list = [result[1] for result in results]
    organization_list = [result[2] for result in results]
    market_list = [result[3] for result in results]
    relationships_list = [result[4] for result in results]
    bandwidth_list = [result[5] for result in results]
    mission_list = [result[6] for result in results]
    design_style_list = [result[7] for result in results]
    quality_list = [result[8] for result in results]
    opportunity_list = [result[9] for result in results]
    selection_process_list = [result[10] for result in results]
    x_factor_list = [result[11] for result in results]
    total_list = [result[12] for result in results]
    comment_list = [result[13] for result in results]

    affinities_data = [{
        "first_name": first_name_list,
        "last_name": last_name_list,
        "organization": organization_list,
        "market": market_list,
        "relationships": relationships_list,
        "bandwidth": bandwidth_list,
        "mission": mission_list,
        "design_style": design_style_list,
        "quality": quality_list,
        "opportunity": opportunity_list,
        "selection_process": selection_process_list,
        "x_factor": x_factor_list,
        "total": total_list,
        "comment": comment_list
    }]

    return jsonify(affinities_data)

if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
