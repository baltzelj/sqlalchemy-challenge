# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

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
        f'Precipitations: /api/v1.0/precipitation \n'
        f'Stations: /api/v1.0/stations \n'
        f'Temperatures: /api/v1.0/tobs \n'
        f'Specific Dates: /api/v1.0/<start> and /api/v1.0/<start>/<end>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Listing Precipitations"""

@app.route("/api/v1.0/stations")
def stations():
    """Listing Stations"""

@app.route("/api/v1.0/tobs")
def tobs():
    """Listing Temperatures"""


if __name__ == '__main__':
    app.run(debug=True)