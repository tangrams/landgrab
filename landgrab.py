# todo: handle cases where the boundary crosses the dateline

import requests, json, math, sys, os
import xml.etree.ElementTree as ET
import pprint

OSMID=sys.argv[1]
zoom=int(sys.argv[2])
coordsonly=0
if len(sys.argv) > 3:
    coordsonly=int(sys.argv[3])
    print coordsonly

success = False
try:
    INFILE = 'http://www.openstreetmap.org/api/0.6/relation/'+OSMID+'/full'
    print "Downloading", INFILE
    r = requests.get(INFILE)
    r.raise_for_status()
    success = True
except Exception, e:
    print e

if not success:
    try:
        INFILE = 'http://www.openstreetmap.org/api/0.6/way/'+OSMID+'/full'
        print "Downloading", INFILE
        r = requests.get(INFILE)
        r.raise_for_status()
        success = True
    except Exception, e:
        print e

if not success:
    try:
        INFILE = 'http://www.openstreetmap.org/api/0.6/node/'+OSMID
        print "Downloading", INFILE
        r = requests.get(INFILE)
        r.raise_for_status()
        success = True
    except Exception, e:
        print e
        print "Element not found, exiting"
        sys.exit()

# print r.encoding
open('outfile.xml', 'w').close() # clear existing OUTFILE

with open('outfile.xml', 'w') as fd:
  fd.write(r.text.encode("UTF-8"))
  fd.close()

try:
    tree = ET.parse('outfile.xml')
except Exception, e:
    print e
    print "XML parse failed, please check outfile.xml"
    sys.exit()

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

## find boundingbox of latlongs
# minx = 180.
# maxx = -180.
# miny = 90.
# maxy = -90.
print "Processing:"

for node in root:
    if node.tag == "node":
        lat = float(node.attrib["lat"])
        lon = float(node.attrib["lon"])
        points.append({'y':lat, 'x':lon})
#         minx = min(minx, lon)
#         maxx = max(maxx, lon)
#         miny = min(miny, lat)
#         maxy = max(maxy, lat)
# print miny, minx, maxy, maxx

## find tile
for point in points:
    tiles.append(tileForMeters(latLngToMeters({'x':point['x'],'y':point['y']}), zoom))

## de-dupe
tiles = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in tiles)]

## patch holes in tileset

## get min and max tiles for lat and long

minx = 1048577
maxx = -1
miny = 1048577
maxy = -1

for tile in tiles:
    minx = min(minx, tile['x'])
    maxx = max(maxx, tile['x'])
    miny = min(miny, tile['y'])
    maxy = max(maxy, tile['y'])
# print miny, minx, maxy, maxx

newtiles = []

for tile in tiles:
    # find furthest tiles from this tile on x and y axes
    x = tile['x']
    lessx = 1048577
    morex = -1
    y = tile['y']
    lessy = 1048577
    morey = -1
    for t in tiles:
        if int(t['x']) == int(tile['x']):
            # check on y axis
            lessy = min(lessy, t['y'])
            morey = max(morey, t['y'])
        if int(t['y']) == int(tile['y']):
            # check on x axis
            lessx = min(lessx, t['x'])
            morex = max(morex, t['x'])

    # if a tile is found which is not directly adjacent, add all the tiles between the two
    if (lessy + 2) < tile['y']:
        for i in range(int(lessy+1), int(tile['y'])):
            newtiles.append({'x':tile['x'],'y':i, 'z':zoom})
    if (morey - 2) > tile['y']:
        for i in range(int(morey-1), int(tile['y'])):
            newtiles.append({'x':tile['x'],'y':i, 'z':zoom})
    if (lessx + 2) < tile['x']:
        for i in range(int(lessx+1), int(tile['x'])):
            newtiles.append({'x':i,'y':tile['y'], 'z':zoom})
    if (morex - 2) > tile['x']:
        for i in range(int(morex-1), int(tile['x'])):
            newtiles.append({'x':i,'y':tile['y'], 'z':zoom})

## de-dupe
newtiles = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in newtiles)]
## add fill tiles to boundary tiles
tiles = tiles + newtiles
## de-dupe
tiles = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in tiles)]


if coordsonly == 1:
    ## output coords
    pprint.pprint(tiles)
    print "Finished: %i tiles at zoom level %i" % (len(tiles), zoom)
else:
    ## download tiles
    print "Downloading %i tiles at zoom level %i" % (len(tiles), zoom)

    ## make/empty the tiles folder
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

    total = len(tiles)
    if total == 0:
        print("Error: no tiles")
        exit()
    count = 0
    sys.stdout.write("\r%d%%" % (float(count)/float(total)*100.))
    sys.stdout.flush()
    for tile in tiles:
        tilename = "%i-%i-%i.json" % (zoom,tile['x'],tile['y'])
        r = requests.get("http://vector.mapzen.com/osm/all/%i/%i/%i.json" % (zoom, tile['x'],tile['y']))
        j = json.loads(r.text)

        # extract only buildings layer - mapzen vector tile files are collections of jeojson objects -
        # doing this turns each file into a valid standalone geojson files -
        # you can replace "buildings" with whichever layer you want
        # j = json.dumps(j["buildings"]) 

        # use this jumps() command instead for the original feature collection with all the data
        j = json.dumps(j);

        with open('tiles/'+tilename, 'w') as fd:
            fd.write(j.encode("UTF-8"))
            fd.close()
        count += 1
        sys.stdout.write("\r%d%%" % (float(count)/float(total)*100.))
        sys.stdout.flush()
        