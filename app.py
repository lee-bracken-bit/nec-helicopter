@app.route("/kml")
def kml():
    import datetime, math, time
    CENTER_LAT, CENTER_LON = 52.4523, -1.7175
    RADIUS   = 0.005    # ~500 m
    PERIOD   = 60.0     # seconds per lap
    ALT      = 150      # m
    STEP     = 0.5      # seconds between samples
    WINDOW   = 5.0      # seconds history (gives 10 samples)

    def state(ts):
        th = (ts % PERIOD) / PERIOD * 2*math.pi
        lat = CENTER_LAT + RADIUS * math.sin(th)
        lon = CENTER_LON + RADIUS * math.cos(th)
        dlat =  (RADIUS * math.cos(th))
        dlon = -(RADIUS * math.sin(th))
        hdg = (math.degrees(math.atan2(dlon, dlat)) + 360) % 360
        return lat, lon, hdg

    now = time.time()
    samples = []
    t0 = now - WINDOW
    n  = int(WINDOW/STEP) + 1
    for i in range(n):
        ts = t0 + i*STEP
        lat, lon, hdg = state(ts)
        when = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
        samples.append((when, lon, lat, ALT, hdg))

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">',
        '<Document>',
        '  <Placemark><name>Helicopter</name>',
        '    <gx:Track><altitudeMode>absolute</altitudeMode>'
    ]
    for when, *_ in samples:
        parts.append(f'      <when>{when}</when>')
    for _, lon, lat, alt, _ in samples:
        parts.append(f'      <gx:coord>{lon:.6f} {lat:.6f} {alt}</gx:coord>')
    for *_, hdg in samples:
        parts.append(f'
