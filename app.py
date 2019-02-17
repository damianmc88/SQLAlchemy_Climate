import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

app = Flask(__name__)


@app.route("/")
def homepage():

     return (
         f"Avalable Routes:<br/>"
         f"/api/v1.0/precipitation"
         f"- Dates and temperature observations from the last year<br/>"

         f"/api/v1.0/stations"
         f"- List of stations<br/>"

         f"/api/v1.0/tobs"
         f"- Temperature Observations from the past year<br/>"

         f"/api/v1.0/<start>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start day<br/>"

         f"/api/v1.0/<start>/<end>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
     )

@app.route("/api/v1.0/precipitation")
def pcrp():
    today = datetime.datetime.today()
    today = today.date()
    last_year = today - datetime.timedelta(365)
    pcp_year = list(session.query(Measurement.date, Measurement.prcp).filter((Measurement.date <= today, Measurement.date >= last_year)).all())
    return jsonify(pcp_year)

@app.route("/api/v1.0/stations")
def station_list():
    st_list = session.query(Station.station).all()
    all_stations= list(np.ravel(st_list))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp_year():
    today = datetime.datetime.today()
    today = today.date()
    last_year = today - datetime.timedelta(365)
    temp_year = session.query(Measurement.date, Measurement.tobs).filter((Measurement.date <= today, Measurement.date >= last_year)).all()
    return jsonify(temp_year)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp_data)

    

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter((Measurement.date >= start, Measurement.date <= end)).all()
    
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)

# import datetime as datetime
# import numpy as np
# import pandas as pd

# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func

# from flask import Flask, jsonify


# def get_session_tables():
#     engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#     Base = automap_base()
#     Base.prepare(engine, reflect=True)
#     Measurement = Base.classes.measurement
#     Station = Base.classes.station
#     session = Session(engine)
#     return (session, Measurement, Station)

# app = Flask(__name__)

# @app.route("/")
# def homepage():
#     # thread gets created to service the request
#     """List of all returnable API routes."""
#     return(
#         f"(Note: Dates range from 2010-01-01 to 2017-08-23). <br><br>"
#         f"Available Routes: <br>"

#         f"/api/v1.0/precipitation<br/>"
#         f"Returns dates and temperature from the last year. <br><br>"

#         f"/api/v1.0/stations<br/>"
#         f"Returns a json list of stations. <br><br>"

#         f"/api/v1.0/tobs<br/>"
#         f"Returns list of Temperature Observations(tobs) for previous year. <br><br>"

#         f"/api/v1.0/yyyy-mm-dd/<br/>"
#         f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"

#         f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
#         f"Returns an Average, Max, and Min temperatures for a given date range."

        
#     )

# # Note - here we are getting the db variables
# # within the same thread that's servicing the request
# # So we don't throw some programming error on Windows machines
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     # connection to the db, session, tables
#     session, Measurement, Station = get_session_tables()
#     """Return Dates and Temp from the last year."""
#     precip_analysis = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
#         filter(Measurement.date <= "2017-08-23").all()

#     # creates JSONified list
#     precipitation_list = [precip_analysis]

#     return jsonify(precipitation_list)

# if __name__ == '__main__':
#     app.run(debug=True)