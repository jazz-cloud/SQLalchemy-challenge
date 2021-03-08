#import libraries
import numpy as np
import pandas as pd
import datetime as dt

# python SQL toolkit and object relational mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask
from flask import Flask, jsonify

# Create engine using the `demographics.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# C: \Users\Owner\OneDrive\Desktop\SQalchemy-challenge\Resources\hawaii.sqlite
# Declare a Base using `automap_base()`
Base = automap_base()


# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Measurement = base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Welcome to my Home page!<br><br>"
            f"/api/v1.0/precipitation<br><br>"
            f"/api/v1.0/stations<br><br>"
            f"/api/v1.0/tobs<br><br>"
            f"/api/v1.0/<start><br><br>"
            f"/api/v1.0/<start>/<end>")

# gettin the precipitation


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= year_ago).all()
    session.close()
    prcp_dict = {date: prcp for date, prcp in precipitation}

    return jsonify(prcp_dict)

# getting the stations


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    stations_list = list(np.ravel(stations))
    session.close()
    return jsonify(stations_list)

# getting the temperature for previous year


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.tobs).filter(
        Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()
    session.close()
    tobs_list = list(np.ravel(tobs))

    return jsonify(tobs_list)

# getting minimum temperature, avg temperature and max temperature when give date


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    temperature = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    temp_list = list(np.ravel(temperature))

    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)
    temperature = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temp_list = list(np.ravel(temperature))

    return jsonify(temp_list)


if __name__ == "__main__":
    app.run(debug=True)
