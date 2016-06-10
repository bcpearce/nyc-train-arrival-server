import csv

def get_stop_list(filepath = 'google_transit/stops.txt'):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        data = [x for x in reader]

    return [(d['stop_id'], d['stop_name']) for d in data if len(d['stop_id']) == 3]

def get_stop_dict(filepath = 'google_transit/stops.txt'):
    return dict(get_stop_list(filepath))

def get_stop_name_dict(filepath = 'google_transit/stops.txt'):
    stops = [(a, b) for b, a in get_stop_list(filepath)]
    return dict(stops)

# keys are obtained with api_key within gtfs.py
def get_stop_names_from_keys(keys, filepath = 'google_transit/stops.txt'):
    stops = get_stop_dict(filepath)
    return {stops[k]:k for k in keys}

