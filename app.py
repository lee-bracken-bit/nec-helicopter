from flask import Flask, Response
import math, time, datetime

app = Flask(__name__)

CENTER_LAT, CENTER_LON = 52.4523, -1.7175  # NEC
RADIUS   = 0.005        # ~500 m
PERIOD   = 60.0         # seconds per full circle
ALTITUDE = 150          # metres
HISTORY_SECONDS = 5.0   # short tail so rotation registers
STEP      = 0.5         # seconds between samples

def heli_state(t):
    """Return lat, lon, heading_deg at epoch time t."""
    # parametric circle
    theta = (t % PERIOD) / PERIOD * 2*math.pi
    lat = CENTER_LAT + RADIUS * math.sin(theta)
    lon = CENTER_LON + RADIUS * math.cos(theta)
    # velocity for bearing (tangent of circle)
    dlat =  (RADIUS * math.cos(theta))           # d/dt scaled out
    dlon = -(RADIUS * math.sin(theta))
    # compass bearing: 0=N, 90=E
    bearing_rad = math.atan2(dlon, dlat)
    heading = (math.

