import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup                                #
#################################################

engine = create_engine('sqlite:///hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

conn = engine.connect()
Base.metadata.create_all(conn)

Base.classes.keys()
measurements= Base.classes.measurements
stations= Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Provide temperature observations from the last year"""
    # Query all measurements data
    now = dt.datetime.now()
    past_yr = now.replace(year=2017)
    measurements = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > past_yr).all()

    # New Dictionary
    all_measurements = []
    for measurement in measurements:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["temp"] = measurement.tobs
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def station():
    """Return a JSON list of stations from the dataset"""
    # Query all stations
    stations = session.query(measurements.station).all()
    
    # Convert list of tuples into a normal list
    stations_dict = list(np.ravel(stations))

    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def temperature():
    """Provide temperature observations from the last year"""
    # Query all measurements data
    now = dt.datetime.now()
    past_yr = now.replace(year=2017)
    temperatures = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > past_yr).all()

    # New Dictionary
    all_temps = []
    for temp in temperatures:
        temp_dict = {}
        temp_dict["temp"] = measurement.tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/")
def min_max():
    minimum = session.query(func.min(measurements.tobs)).\
    filter(measurement.date >= start_date).all()

# Convert list of tuples into normal list
    minimum_dict = list(np.ravel((minimum)))

    return jsonify(minimum_dict)

    maximum = session.query(func.max(measurements.tobs)).\
    filter(measurement.date >= start_date).all()
# Convert list of tuples into normal list
    maximum_dict = list(np.ravel((maximum)))

    return jsonify(maximum_dict)

    average = session.query(func.avg(measurements.tobs)).\
    filter(measurement.date >= start_date).all()
# Convert list of tuples into normal list
    maximum_dict = list(np.ravel((average)))

    return jsonify(average)

if __name__ == '__main__':
    app.run(debug=True)
