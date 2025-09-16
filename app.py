from flask import Flask, Response
import math, time, datetime

app = Flask(__name__)

# NEC centre
CENTER_LAT, CENTER_LON = 52.4523, -1.7175
RADIUS   = 0.005      # ~500 m
PERIOD   = 60.0       # seconds per loop
ALTITUDE = 150        # m

def heli_state(t):
    theta = (t % PERIOD) / PERIOD * 2*math.pi
    lat = CENTER_LAT + RADIUS * math.sin(theta)
    lon = CENTER_LON + RADIUS * math.cos(theta)
    dlat =  (RADIUS * math.cos(theta))
    dlon = -(RADIUS * math.sin(theta))
    bearing_rad = math.atan2(dlon, dlat)
    heading = (math.degrees(bearing_rad) + 360) % 360  # << no line break
    return lat, lon, heading

@app.route("/")
def index():
    return "<h3>NEC Helicopter KML</h3><p>Use <code>/kml</code> in your NetworkLink.</p>"

@app.route("/kml")
def kml():
    now = time.time()
    lat, lon, hdg = heli_state(now)
    kml_text = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
<Document>
  <Placemark>
    <name>Helicopter</name>
    <Style>
      <IconStyle>
        <scale>1.6</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/heliport.png</href></Icon>
      </IconStyle>
    </Style>
    <gx:Track><altitudeMode>absolute</altitudeMode>
      <when>{datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</when>
      <gx:coord>{lon:.6f} {lat:.6f} {ALTITUDE}</gx:coord>
      <gx:angles>{hdg:.1f} 0 0</gx:angles>
    </gx:Track>
  </Placemark>
</Document>
</kml>"""
    return Response(kml_text, mimetype="application/vnd.google-earth.kml+xml")


