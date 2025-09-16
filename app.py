from flask import Flask, Response
import math, time

app = Flask(__name__)

CENTER_LAT, CENTER_LON = 52.4523, -1.7175   # NEC
RADIUS = 0.005      # ~500 m
PERIOD = 60.0       # seconds per full circle
ALTITUDE = 150      # meters

@app.route("/")  # friendly landing page
def index():
    return "NEC Helicopter KML – use /kml"

@app.route("/kml")  # THIS is the endpoint Google Earth needs
def kml():
    t = (time.time() % PERIOD) / PERIOD * 2 * math.pi
    lat = CENTER_LAT + RADIUS * math.sin(t)
    lon = CENTER_LON + RADIUS * math.cos(t)
    kml_text = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Placemark>
    <name>Helicopter</name>
    <Style>
      <IconStyle>
        <scale>1.5</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/shapes/heliport.png</href>
        </Icon>
      </IconStyle>
    </Style>
    <Point><coordinates>{lon:.6f},{lat:.6f},{ALTITUDE}</coordinates></Point>
  </Placemark>
</Document>
</kml>"""
    return Response(kml_text,
                    mimetype="application/vnd.google-earth.kml+xml")
