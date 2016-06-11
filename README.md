# NYC Train Arrival Server
Server for Feeding Data to nyc-train-arrival.

## Setup
Create a file `api_key` in the root directory.  Add to this file only the MTA supplied API key.  The key can be obtained here http://datamine.mta.info/.

Run `$ pip install -r requirements.txt` to install dependencies.  

## Running
Run these commands in a terminal from the root directory:

`$ export FLASK_APP='app.py'`

`$ python -m flask run`
