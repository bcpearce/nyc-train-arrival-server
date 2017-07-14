import os, pdb
from gtfs import Gtfs

from flask import Flask, jsonify
app = Flask(__name__)

with open("feeds.txt", "r") as f:
    feeds_ids = [int(x) for x in f.readline().split()]

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

gtfs_l = [Gtfs(os.environ['MTA_API_KEY'], feed_id = fid, VERBOSE=True) for fid in feeds_ids]

@app.route('/')
def root():
    return "Please direct your request to https://"

@app.route('/stop/<stop_id>')
def get_arrivals(stop_id):
    for gtfs in gtfs_l:
        ret_val = gtfs.get_time_to_arrival(stop_id)
        if len(ret_val) > 0:
            break
    return jsonify(ret_val)

@app.route('/stop_list')
@app.route('/stops')
def get_stops():
    s_not_flat = [gtfs.get_stations_with_gtfs_data() for gtfs in gtfs_l]
    return jsonify(sorted([item for sublist in s_not_flat for item in sublist]))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
