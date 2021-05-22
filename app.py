import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    print("Welcome")

    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/yyyy-mm-dd<br/>"
        f"/api/v1.0/date/yyyy-mm-dd/yyyy-mm-dd")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    Return the JSON representation of your dictionary."""
    results = session.query(Measurement.date, Measurement.prcp, func.avg(Measurement.prcp)).filter(
        Measurement.date >= query_date).group_by(Measurement.date).all()

    session.close
    return jsonify(precipitation=results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    stations = session.query(Station.station).all()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Query the dates and temperature observations of the most active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.station == 'USC00519281').filter(Measurement.date >= query_date).all()
    return jsonify(results)

@app.route("/api/v1.0/date/<start>")
@app.route("/api/v1.0/date/<start>/<end>")
def sttenddates(start=None, end=None):
    session = Session(engine)
    """* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    * When given the start only or the start/end date, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    # SELECT Statement
    sel = [func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)]
    print("======================")
    print(*sel)
    print("======================")
    if not end:
        # calculate min, max, avg for dates greater than start
        # results = session.query(*sel).filter(measurement.date >= start).all()
        results = session.query(func.min(Measurement.tobs), func.avg(
            Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    else:
        # calculate min, max, avg for dates between start and stop
        results = session.query(
            func.min(Measurement.tobs), func.avg(
                Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # unravel results into a 1D array and convert to list
    temps = list(np.ravel(results))
    session.close
    return jsonify(temps=temps)







    session.close
    return jsonify(tobs=results)


    session.close
    return jsonify(stations=stations)


if __name__ == "__main__":
    app.run()


