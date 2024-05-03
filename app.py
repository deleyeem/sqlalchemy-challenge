# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine ,func
import numpy as np
import datetime as dt
from datetime import datetime

#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")####

# Declare a Base using `automap_base()`
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Start at the homepage using "/" and list all the available routes.
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date_row = session.query(measurement.date).\
                    order_by(measurement.date.desc()).first()
    last_date = last_date_row[0]
    last_date_dt = datetime.strptime(last_date, "%Y-%m-%d")
    last_12_months = last_date_dt - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precip_query = session.query(measurement.date, measurement.prcp).\
                    filter(measurement.date > last_12_months).all()   
# # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# # Return the JSON representation of your dictionary.
    results = list(np.ravel(precip_query))
    return jsonify(results)

# @app.route("/api/v1.0/stations)
# # Return a JSON list of stations from the dataset.
# def stations():
#     return jsonify(INSERT)
           
# @app.route("/api/v1.0/tobs)
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
# def previous_data():
#     return jsonify()
           
@app.route("/api/v1.0/<start>") 
@app.route("/api/v1.0/<start>/<end>")
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
def stats(start = None, end = None):
    sel  = [func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)] 

    if not end:
        start = dt.datetime.strptime(start,"%Y%m%d")
        result = session.query(*sel).\
            filter(measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(result))
        return jsonify(temps)
    start = dt.datetime.strptime(start,"%Y%m%d")
    end = dt.datetime.strptime(end,"%Y%m%d")
    result = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date<=end).all()
    session.close()
    temps = list(np.ravel(result))
    return jsonify(temps)
    #return pass

if __name__ == "__main__":
    app.run(debug=True)