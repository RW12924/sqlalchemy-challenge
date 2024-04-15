# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    return (
        f'Welcome!<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'<br/>'
        f'For the routes below, start/end can be replaced by dates formatted as YYYY-MM-DD.<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    # Creates a session (link) from Python to the database
    session = Session(engine)

    # Calculates the date 1 year before the latest datapoint was collected
    earlier_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Queries the session for dates and precipitation data that were collected
    # after the date calculated above
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= earlier_date)

    # Close Session
    session.close()

    # Organizes the retrieved data into a dictionary
    # Adds the dictionary entries into a list
    date_prcp_list = []
    for date, prcp in date_prcp:
        date_prcp_dict = {}
        date_prcp_dict['date'] = date
        date_prcp_dict['prcp'] = prcp
        date_prcp_list.append(date_prcp_dict)

    # Converts our list into json format and returns the json representation
    return jsonify(date_prcp_list)

@app.route('/api/v1.0/stations')
def stations():
    # Creates a session (link) from Python to the database
    session = Session(engine)

    # Queries our database to retrieve all stations
    all_stations = session.query(Station.station)

    # Close Session
    session.close()

    # Organizes the retrieved data into a dictionary
    # Adds the dictionary entries into a list
    stations_list = []
    for station in all_stations:
        stations_dict = {}
        stations_dict['stations'] = station[0]
        stations_list.append(stations_dict)

    # Converts our list into json format and returns the json representation
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Creates a session (link) from Python to the database
    session = Session(engine)

    # Calculates the date that was 1 year before the last data collection
    # for station USC00519281
    station_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    # Queries our database to retrieve temperatures for station USC00519281
    # that occurred in the last year of data collection
    all_tobs = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= station_date)

    # Close Session
    session.close()

    # Organizes the retrieved data into a dictionary
    # Adds the dictionary entries into a list
    tobs_list = []
    for each_entry in all_tobs:
        tobs_dict = {}
        tobs_dict['tobs'] = each_entry[0]
        tobs_list.append(tobs_dict)

    # Converts our list into json format and returns the json representation
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start_date_func(start):
    # Creates a session (link) from Python to the database
    session = Session(engine)

    # Queries our database for minimum, maximum, and average temperatures 
    # observed after the start date provided
    start_summary = session.query(func.min(Measurement.tobs, label='min_temp'),\
    func.avg(Measurement.tobs, label='avg_temp'),\
    func.max(Measurement.tobs, label='max_temp')).\
    filter(Measurement.date >= start).all()

    # Close Session
    session.close()

    # Organizes the retrieved data into a dictionary
    # Adds the dictionary entries into a list
    start_list = []
    for min_temp, avg_temp, max_temp in start_summary:
        start_dict = {'date_start': start}
        start_dict['min_temp'] = min_temp
        start_dict['avg_temp'] = avg_temp
        start_dict['max_temp'] = max_temp
        start_list.append(start_dict)

    # Converts our list into json format and returns the json representation
    return jsonify(start_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    # Creates a session (link) from Python to the database
    session = Session(engine)

    # Queries our database for minimum, maximum, and average temperatures 
    # observed between the start date and end date provided
    end_summary = session.query(func.min(Measurement.tobs, label='min_temp'),\
    func.avg(Measurement.tobs, label='avg_temp'),\
    func.max(Measurement.tobs, label='max_temp')).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    # Close Session
    session.close()

    # Organizes the retrieved data into a dictionary
    # Adds the dictionary entries into a list
    end_list = []
    for min_temp, avg_temp, max_temp in end_summary:
        end_dict = {'date_start': start,
                    'date_end': end}
        end_dict['min_temp'] = min_temp
        end_dict['avg_temp'] = avg_temp
        end_dict['max_temp'] = max_temp
        end_list.append(end_dict)

    # Converts our list into json format and returns the json representation
    return jsonify(end_list)

if __name__ == '__main__':
    app.run(debug=True)