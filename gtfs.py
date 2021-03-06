import urllib2, os, pdb, csv, time
from google.transit import gtfs_realtime_pb2

class Gtfs:

    MTA_URL = "http://datamine.mta.info/mta_esi.php?key={0}&feed_id={1}"
    STOPS_FILE = "google_transit/stops.txt"

    def __init__(self, api_key, feed_id=1, feed_age = 60, VERBOSE=False):
        self.feed_id = feed_id
        self.api_key = api_key
        self.feed_age = feed_age
        self.VERBOSE = VERBOSE
        self.stops = self.get_stops()
        self.feed = None

    def get_feed(self):
        url = self.MTA_URL.format(self.api_key, self.feed_id)
        self.response = urllib2.urlopen(url)
        self.last_read = time.time()
        if self.VERBOSE:
            print "Feed {0}: updated arrival times".format(self.feed_id)

    def parse_feed(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(self.response.read())
        self.feed = feed

    def get_stops(self, data_file = STOPS_FILE):
        with open(data_file) as f:
            reader = csv.DictReader(f)
            stops = [x for x in reader]
        keys = [x['parent_station'] for x in stops]
        return dict(zip(keys, stops))

    def get_updates_at_stop_id(self, stop_id):
        updates = []
        # only get the feed if the dataset is older than the feed age
        if not self.feed or time.time() - self.last_read > self.feed_age:
            self.get_feed()
            self.parse_feed()
        
        for entity in self.feed.entity:
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == stop_id:
                    updates.append((entity.trip_update.trip.route_id,
                                    stop_time_update.arrival.time,
                                    stop_time_update.stop_id))
        return updates

    def get_time_to_arrival(self, stop_id):
        updates = self.get_updates_at_stop_id(stop_id)
        times = []
        for update in updates:
            eta = update[1] - round(time.time())
            times.append((update[0], eta, update[2]))
        arrivals = [dict(zip(["route", "time", "stop_id"], t)) for t in times]
        return arrivals

    def get_stations_with_gtfs_data(self):
        stop_id_list = []
        self.get_feed()
        self.parse_feed()
        for entity in self.feed.entity:
            for stop_time_update in entity.trip_update.stop_time_update:
                stop_id_list.append(stop_time_update.stop_id[:-1])

        return list(set(stop_id_list))

if __name__ == "__main__":

    if not os.environ.get('MTA_API_KEY'):
        with open("api_key") as f:
            os.environ['MTA_API_KEY'] = f.readline().strip()

    gtfs = Gtfs(os.environ['MTA_API_KEY'])

    times = gtfs.get_time_to_arrival('239N')
    for eta in times:
        print eta
        print "There is a {0} train arriving in {1}:{2:02d}".format(
            eta["route"], int(eta["time"]/60), int(eta["time"]%60))
    pdb.set_trace()
