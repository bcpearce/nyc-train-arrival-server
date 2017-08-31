import os, pdb
from gtfs import Gtfs

from flask import Flask, jsonify, send_file, redirect
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

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
s_not_flat = [gtfs.get_stations_with_gtfs_data() for gtfs in gtfs_l]
s_flat = sorted([item for sublist in s_not_flat for item in sublist])

@app.route('/')
def root():
    return "Please direct your request to https://"

@app.route('/stop/<stop_id>')
def get_arrivals(stop_id):
    for gtfs in gtfs_l:
        arrivals = gtfs.get_time_to_arrival(stop_id)
        if len(arrivals) > 0:
            break
    stop_info = gtfs.stops[stop_id.rstrip('N').rstrip('S')]
    stop_info["stop_id"] = stop_id
    #from pprint import pprint
    #pprint({'stop':stop_info, 'arrivals':arrivals})
    return jsonify({'stop':stop_info, 'arrivals':arrivals})

@app.route('/stop_list')
@app.route('/stops')
def get_stops():
    return jsonify({ k:gtfs.stops.get(k) for k in s_flat })

@app.route('/bullet/<bullet_id>')
def get_bullet(bullet_id, ext="png"):
    if not bullet_id.endswith((".png", ".gif", ".bmp", ".jpg")):
        return redirect("/bullet/{0}.{1}".format(bullet_id, ext), code=302)
    return send_file("img/{0}".format(bullet_id), mimetype="image/{0}".format(ext))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
