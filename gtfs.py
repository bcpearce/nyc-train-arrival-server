import urllib2, os, pdb, csv, time
from google.transit import gtfs_realtime_pb2

class Gtfs:

    MTA_URL = "http://datamine.mta.info/mta_esi.php?key={0}&feed_id={1}"
    STOPS_FILE = "google_transit/stops.txt"

    def __init__(self, api_key, feed_id=1):
        self.feed_id = feed_id
        self.api_key = api_key

    def get_feed(self):
        url = self.MTA_URL.format(self.api_key, self.feed_id)
        self.response = urllib2.urlopen(url)

    def parse_feed(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(self.response.read())
        self.feed = feed

    def get_stops(data_file = STOPS_FILE):
        with open(data_file) as f:
            reader = csv.DictReader(f)
            return [x for x in reader]

    def get_updates_at_stop_id(self, stop_id):
        updates = []
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
        return times

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

    times = gtfs.get_time_to_arrival('236S')
    for eta in times:
        print "There is a {0} train arriving in {1}:{2:02d}".format(eta[0], int(eta[1]/60), int(eta[1]%60))
    pdb.set_trace()