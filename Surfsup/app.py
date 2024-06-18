# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def home():
    """List of all available routes"""
    return (
        '<b>Available Routes:</b><br/>'
        'Precipitations: /api/v1.0/precipitation<br/>'
        'Stations: /api/v1.0/stations<br/>'
        'Temperatures: /api/v1.0/tobs<br/>'
        'Specific Dates: /api/v1.0/<start> and /api/v1.0/<start>/<end>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Listing Precipitations"""
    most_rec_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    most_rec_date = dt.datetime.strptime(most_rec_date[0], '%Y-%m-%d').date()
    query_date = most_rec_date - dt.timedelta(days=365)
    recent_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date)
    prcp_data = pd.DataFrame(recent_data)
    prcp_data = prcp_data.rename(columns={
        'date': 'Date',
        'prcp': 'Precipitation'
    })
    all_data = list(np.ravel(prcp_data))
    
    return (
        jsonify(all_data)
    )

@app.route("/api/v1.0/stations")
def stations():
    """Listing Stations"""
    act_sta = session.query(measurement.station, func.count(measurement.station)).\
        order_by(func.count(measurement.station).desc()).\
        group_by(measurement.station).all()

    act_sta = list(np.ravel(act_sta))
    return (
        jsonify(act_sta)
    )

@app.route("/api/v1.0/tobs")
def tobs():
    """Listing Temperatures"""
    actsta_temps = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').all()

    actsta_temps = list(np.ravel(actsta_temps))
    return (
        jsonify(actsta_temps)
    )

@app.route("/api/v1.0/<start>")
def date_search(start):
    """Finding for Specific Dates"""
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= start).all()
    temps = list(np.ravel(temps))
    return (temps)

@app.route("/api/v1.0/<start>/<end>")
def bet_dates(start, end):
    """Finding Data Between Dates"""
    temps = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    temps = list(np.ravel(temps))
    return(temps)

if __name__ == '__main__':
    app.run(debug=True)