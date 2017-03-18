import os
from gtfs import Gtfs

from flask import Flask, jsonify
app = Flask(__name__)

# set up GTFS data collection
if not os.environ.get('MTA_API_KEY'):
    try:
        with open("api_key") as f:
            os.environ['MTA_API_KEY'] = f.readline().strip()
    except:
        print "ERROR: no API Key found."
        print "Please add API key in '{0}/api_key' file".format(app.root_path)
        print "or set the API as environment variable 'MTA_API_KEY'."
        raise SystemExit

gtfs = Gtfs(os.environ['MTA_API_KEY'], VERBOSE=True)

@app.route('/')
def root():
    return "Please direct your request to https://"

@app.route('/stop/<stop_id>')
def get_arrivals(stop_id):
    return jsonify(gtfs.get_time_to_arrival(stop_id))

@app.route('/stop_list')
def get_stops():
    return jsonify(gtfs.get_stations_with_gtfs_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0")
