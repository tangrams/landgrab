import requests, json, math, sys, os
import xml.etree.ElementTree as ET

OSMID=sys.argv[1]
# OUTFILE=sys.argv[2]

r = requests.get('http://www.openstreetmap.org/api/0.6/relation/'+OSMID+'/full')
print r.encoding
open('outfile.xml', 'w').close() # clear existing OUTFILE

with open('outfile.xml', 'w') as fd:
  fd.write(r.text.encode("UTF-8"))
  fd.close()

zoom = 15

tree = ET.parse('outfile.xml')

root = tree.getroot()

points = []
tiles = []

##
## HELPER FUNCTIONS
##

tile_size = 256
half_circumference_meters = 20037508.342789244;

# Convert lat-lng to mercator meters
def latLngToMeters( coords ):
    y = float(coords['y'])
    x = float(coords['x'])
    # Latitude
    y = math.log(math.tan(y*math.pi/360 + math.pi/4)) / math.pi
    y *= half_circumference_meters

    # Longitude
    x *= half_circumference_meters / 180;

    return {"x": x, "y": y}

# convert from tile-space coords to meters, depending on zoom
def tile_to_meters(zoom):
    return 40075016.68557849 / pow(2, zoom)

# Given a point in mercator meters and a zoom level, return the tile X/Y/Z that the point lies in
def tileForMeters(coords, zoom):
    y = float(coords['y'])
    x = float(coords['x'])
    return {
        "x": math.floor((x + half_circumference_meters) / (half_circumference_meters * 2 / pow(2, zoom))),
        "y": math.floor((-y + half_circumference_meters) / (half_circumference_meters * 2 / pow(2, zoom))),
        "z": zoom
    }

# Convert tile location to mercator meters - multiply by pixels per tile, then by meters per pixel, adjust for map origin
def metersForTile(tile):
    return {
        "x": tile['x'] * half_circumference_meters * 2 / pow(2, tile.z) - half_circumference_meters,
        "y": -(tile['y'] * half_circumference_meters * 2 / pow(2, tile.z) - half_circumference_meters)
    }

##
## PROCESSING
##

minx = 180.
maxx = -180.
miny = 90.
maxy = -90.

# extract latlongs
for node in root:
    if node.tag == "node":
        lat = float(node.attrib["lat"])
        lon = float(node.attrib["lon"])
        points.append({'y':lat, 'x':lon})
        minx = min(minx, lon)
        maxx = max(maxx, lon)
        miny = min(miny, lat)
        maxy = max(maxy, lat)
print miny, minx, maxy, maxx

# find tile
for point in points:
    tiles.append(tileForMeters(latLngToMeters({'x':point['x'],'y':point['y']}), zoom))

# de-dupe
print len(tiles)
tiles = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in tiles)]
print len(tiles)
print tiles

folder = "tiles"
if not os.path.exists(folder):
    os.makedirs(folder)

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e

for tile in tiles:
    tilename = "%i-%i-%i.json" % (zoom,tile['x'],tile['y'])
    r = requests.get("http://vector.mapzen.com/osm/all/%i/%i/%i.json" % (zoom, tile['x'],tile['y']))

    j = json.loads(r.text)
    j = json.dumps(j["earth"]) 

    with open('tiles/'+tilename, 'w') as fd:
        # fd.write(r.text.encode("UTF-8"))
        fd.write(j.encode("UTF-8"))
        fd.close()
    