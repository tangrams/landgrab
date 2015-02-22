# todo: handle cases where the boundary crosses the dateline

# from __future__ import print_function
import requests, json, math, re, sys, os
import xml.etree.ElementTree as ET
import pprint
from Polygon import *
from Polygon.IO import *
# OSMID=sys.argv[1]
# zoom=int(sys.argv[2])
# coordsonly=0
# if len(sys.argv) > 3:
#     coordsonly=int(sys.argv[3])
#     print coordsonly


# read a file
# read all the files
# parse the json into a python object

files = []
inf = float('inf')
tilemin = [inf, inf]
tilemax = [0, 0]
p = re.compile('(\d*)-(\d*)-(\d*).*')

for f in os.listdir("tiles1"):
    if f.endswith(".json"):
        files.append("tiles1/"+f)
        # convert matches to ints and store in m
        m = [int(i) for i in p.findall(f)[0]]
        print m
        latlong = [m[1], m[2]]
        tilemin = [min(tilemin[0], latlong[0]), min(tilemin[1], latlong[1])]
        tilemax = [max(tilemax[0], latlong[0]), max(tilemax[1], latlong[1])]

print "min:", tilemin, "max:", tilemax

tiles = []
# files = 
class Tile:
    def __init__(self, filename, x, y, data):
        self.path = filename
        self.x = x
        self.y = y
        self.data = data

for t in files:
    f = open(t, 'r')
    m = [int(i) for i in p.findall(t)[0]]
    # print m
    filedata = f.read()
    # print len(filedata)
    tile = Tile(t, m[1], m[2], filedata)
    tiles.append(tile)

print len(tiles)
print [t.path for t in tiles]
# print [t.data for t in tiles]


polys = []
dupes = []
for t in tiles:
    j = json.loads(t.data)
        # extract only buildings layer - mapzen vector tile files are collections of jeojson objects -
        # doing this turns each file into a valid standalone geojson files -
        # you can replace "buildings" with whichever layer you want
        # j = json.dumps(j["buildings"]) 

        # use this jumps() command instead for the original feature collection with all the data
# j = json.dumps(j);
# pprint.pprint(j)
# print len(j["buildings"])
# print j["buildings"].keys()
# pprint.pprint(j["buildings"]["features"])
# for f in j["buildings"]["features"]:
#     for c in f["geometry"]["coordinates"]:
#         # print len(c) # likely 5 - a square, with first and last coords the same
#         # print tuple(tuple(i) for i in c)
#         polys.append(Polygon(tuple(tuple(i) for i in c)))

    for f in j["buildings"]["features"]:
        p = Polygon()
        for c in f["geometry"]["coordinates"]:
            # print len(c) # rectangles have 5 - first and last coords are identical
            # remove last redundant coordinate from each poly
            del c[-1]
            # print len(c)
            # print c
            for v in c:
                # print "v:", v
                # print tilemax[0]
                # offset tiles to arrange in scenespace
                v = [v[0]+(4096*(tilemax[0]-tile.x)), v[1]+(4096*(tilemax[1]-tile.y))]
                # print "v2:", v
            # for i in c:
            #     print(tuple(i))
            # print (tuple(i) for i in c)
            p.addContour([tuple(i) for i in c])
            # print p
            # print p[0]
            # sys.exit()

            # print "poly:", poly
            # print ""
            # pp = tuple(tuple(j) for j in poly)
            # print "pp:", pp
            #     # polys.append(pp)
            # ppp = Polygon(pp)
            # print Polygon(tuple(tuple(j) for j in poly))
            # polys.append(Polygon(tuple(tuple(j) for j in poly)))
            # polys.append(Polygon(tuple(tuple(j) for j in poly)))
            polys.append(p)
            # polys.append(Polygon(tuple(tuple(i) for i in c)))

print len(polys)

matches = []
mults = []

def compare(first, second):
    for i, v in enumerate(first):
        # print "> checking:"
        # print p[j]
        # print polys[index][j]
        if v != polys[i]:
            return False
    return True


# brute force duplication check
# for each polygon
for i, p in enumerate(polys):
    # check against every other polygon in the list, starting with the next one
    # print len(p)
    if len(p) > 1:
        # print len(p)
        # for j in p:
            # print len(j), j
        mults.append(p)
        # print len(mults)
    for index in range(i+1, len(polys)):
        # if they have the same # of contours
        if len(p) == len(polys[index]):
            match = True
            # for each vertex
            for j, v in enumerate(p):
                print "> checking:"
                print p[j]
                print polys[index][j]
                if p[j] != polys[index][j]:
                    match = False
                    break
                else:
                    print ">> match"
            if match:
                sys.exit()
                # print "match:", p, polys[index]
                matches.append(p)


# writeSVG('tiles.svg', polys, width=800, height=800)
# writeSVG('overlap.svg', matches, width=800, height=800)
writeSVG('tiles.svg', polys)
writeSVG('mults.svg', mults)
writeSVG('overlap.svg', matches)


sys.exit()




# get the tile mins and maxes
# parse out all the verts
# for each layer
# apply offset to all the verts to get them all in the same scenespace
# then for just the buildings layer:
    # make a quadtree
    # add all polys to the quadtree
    # find overlap polys - collision detect
    # determine poly hierarchy - determine which is the "master" poly for each group
    # assign each group to a tile by centroid of master poly
    # find and delete duplicate groups
# write the trimmed tiles back out














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
        