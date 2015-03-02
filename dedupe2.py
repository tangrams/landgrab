# todo: handle cases where the boundary crosses the dateline

# from __future__ import print_function
from __future__ import division
import requests, json, time, math, re, sys, os
from sys import stdout
from numpy import *
import numpy as np
import xml.etree.ElementTree as ET
import pprint
from Polygon import *
from Polygon.IO import *
# OSMID=sys.argv[1]
# zoom=int(sys.argv[2])

files = []
inf = float('inf')
tilemin = [inf, inf]
tilemax = [0, 0]
p = re.compile('(\d*)-(\d*)-(\d*).*')
path = "tiles2"
for f in os.listdir(path):
    if f.endswith(".json"):
        files.append(path+"/"+f)
        # convert matches to ints and store in m
        m = [int(i) for i in p.findall(f)[0]]
        # print m
        latlong = [m[1], m[2]]
        tilemin = [min(tilemin[0], latlong[0]), min(tilemin[1], latlong[1])]
        tilemax = [max(tilemax[0], latlong[0]), max(tilemax[1], latlong[1])]

print "min:", tilemin, "max:", tilemax

tiles = []

def xtolong(x, z):
    return x / pow(2.0, z) * 360.0 - 180

def ytolat(y, z):
    n = 2.0 ** z
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    return math.degrees(lat_rad)

class Tile:
    def __init__(self, filename, x, y, z, data):
        self.path = filename
        # x = 19299
        # y = 24633
        # x = 0
        # y = 0
        # z = 16
        self.x = x
        self.y = y
        self.data = data

        # self.bounds = Polygon(((xtolong(x), ytolat(y)), (xtolong(x+1), ytolat(y)), (xtolong(x+1), ytolat(y+1)), (xtolong(x), ytolat(y+1))))
        self.bounds = (xtolong(x,z), ytolat(y,z)), (xtolong(x+1,z), ytolat(y,z)), (xtolong(x+1,z), ytolat(y+1,z)), (xtolong(x,z), ytolat(y+1,z))
        print self.bounds
        sys.exit()
        # when z = 1, this should produce ((-180,-90),(180,90),(180,-90),(-180,-90))


        # self.bounds = Polygon(((tx, ty), (tx+4096, ty), (tx+4096, ty+4096), (tx, ty+4096)))
        self.bbox = [inf,inf,-inf,-inf]
        self.polys = []

for t in files:
    f = open(t, 'r')

    # run the filename through the regex - m = saved matches 
    # example: [15, 9646, 12319]
    m = [int(i) for i in p.findall(t)[0]]
    # print m
    filedata = f.read()
    tile = Tile(t, m[1], m[2], m[0], filedata)
    tiles.append(tile)

print "Processing", len(tiles), "tiles"

# naming conventions for clarity:
# "jpoly" will be a polygon defined in json - "poly" will be a Polygon()
# "jcontour" will be a contour of a jpoly - "contour", that of a poly

# expand bbox1 to include bbox2
def updateBbox(bbox1, bbox2):
    new = [bbox1[0], bbox1[1], bbox1[2], bbox1[3]]
    new[0] = min(bbox1[0], bbox2[0])
    new[1] = min(bbox1[1], bbox2[1])
    new[2] = max(bbox1[2], bbox2[2])
    new[3] = max(bbox1[3], bbox2[3])
    return new

# a flat list of all the polygons in the scene
# alljpolys = []

# create a non-duplicated set of all the jpolys in the scene
# buildingcount = 0
# contourcount = 0
for t in tiles:
    print t
    j = json.loads(t.data)

    # for each building
    buildings = j["buildings"]["features"]
    for b in buildings:
        # buildingcount += 1
        # make a non-duplicating set of all the contours in the jpoly
        # jpoly = set()
        contours = b["geometry"]["coordinates"]
        id = b["id"]
        # if len(contours) > 1: 

        # new Polygon object
        poly = Polygon()
        poly.id = id

        # for each contour in the jpoly
        for c in contours:
            # contourcount += 1
            # remove last redundant coordinate from each contour
            del c[-1]
            # for each vertex
            # for v in c:
                # offset all verts in tile to arrange in scenespace
                # this isn't necessary when the data is coming straight from the json,
                # only when the data is coming from a tangram vbo
                # print v[0]
                # if not (4096*(tilemax[0]-tile.x)) == 0:
                #     print (4096*(tilemax[0]-tile.x))
                # if not (4096*(tilemax[1]-tile.y)) == 0:
                #     print (4096*(tilemax[1]-tile.y))
                # print v[1]
                # print (4096*(tilemax[1]-tile.y))
                # v = [v[0]+(4096*(tilemax[0]-tile.x)), v[1]+(4096*(tilemax[1]-tile.y))]
            # print c
            # sys.exit()
            tuplec = tuple(tuple(i) for i in c)
            # jpoly.add(tuplec)

            poly.addContour(c)
            # update tile's bbox with contour's bbox
            t.bbox = updateBbox(t.bbox, list(poly.boundingBox()))

        t.polys.append(poly)
        # alljpolys.append(tuple(jpoly))
        # jpolysset.add(tuple(jpoly))

# jpolyslist = list(jpolysset)




## convert json polys to Polygon objects
allpolys = []
# first, the polys from the list (everything in the json)
# for p in alljpolys:
#     poly = Polygon()
#     poly.sources = []
#     for c in p:
#         poly.addContour(c)
#         poly.sources.append(c)
#     allpolys.append(poly)
# print "length allpolys:", len(allpolys)

# then, the polys from the set (no duplicates)
polys = set()
for t in tiles:
    for p in t.polys:
        polys.add(p)
polys = list(polys)
# print "number of buildings", buildingcount
# print "number of contours", contourcount
# print "length polys", len(polys)

print "checking polys for overlap"
groups = [] # all buildings
contains = [] # all shapes which completely contain other shapes
overlaps = [] # all shapes which touch other shapes
area = []
areas = []
sortedpolys = []
count = 0
total = np.float64(np.sum(range(len(polys)))*2)

# check for intersection of two bounding boxes
def bboxIntersect(bbox1, bbox2):
    if (bbox1[2]<bbox2[0] or bbox2[2]<bbox1[0] or bbox1[3]<bbox2[1] or bbox2[3]<bbox1[1]):
        return False
    else:
        return True

grouped = []
# find overlaps among polys
for i, tile in enumerate(tiles):
    stdout.write("\r%d%%" % abs(round((i/len(tiles) * 100), 0)))
    stdout.flush()
    for p in tile.polys:
        if p.id in grouped: continue
        grouped.append(p.id)
        # print "\n\nnew P:", p
        group = [p]
        # group.append(p)
        # print "len(group):", len(group)
        for t in tiles:
            if (tile == t) or (not bboxIntersect(tile.bbox, t.bbox)): continue
            if bboxIntersect(list(p.boundingBox()), t.bbox):
                for q in t.polys:
                    # sys.exit()
                    # if not list(p) == list(q):
                    # if p.id != q.id:
                    if p.overlaps(q):
                        # print p.id, q.id
                            # print "\nQ:", q

                        group.append(q)
                    # else:
                    #     print 'exact'
        # if group in groups: print "already there"
        # print "group:", group
        # print "tuple(group):", tuple(group)
        # groups.add(tuple(group))
        groups.append(group)
        # print "len(group):", len(group)
        # if the group has more than one element
        if len(group) > 1:
            # overlaps.add(tuple(group))
            overlaps.append(group)
    # print "len(groups):", len(groups)

# for i, p in enumerate(polys):
#     # skip polys which have already been grouped by a previous match
#     # if i not in sortedpolys:
#     #     sortedpolys.append(i)
#         # check polygon against all grouped polygons
#         # if checkGroups(p):
#             # skip to next poly
#             # continue

#     # if not, start a new group
#     group = [p]
#     area = [p]

#     # check polygon against all ungrouped polygons
#     for j, q in enumerate(polys):
#         count = j+(i*len(polys))
#         if count % (int(float(total)/100)) == 0:
#             stdout.write("\r%d%%" % abs(round((count/total * 100), 0)))
#             stdout.flush()
#         if not i == j:
#             # check for any touching
#             if p.overlaps(q):
#                 group.append(q)

#     groups.append(group)
#     # if the group has more than one element
#     if len(group) > 1:
#         overlaps.add(tuple(group))



stdout.write("\r100%\n")
stdout.flush() 


# assign groups to tiles
for g in groups:
    # sort all polys in group by area
    g.sort(key=lambda p: p.area)
    # assume largest area is the outer polygon
    # find tile in which the outer's centroid lies
    outer = g[0]
    # print outer
    c = outer.center()
    # print c
    home = ""
    for t in tiles:
        # if 
        print "t.bounds", t.bounds[0]
        print "c", c
        print t.bounds.isInside(c[0], c[1])
        sys.exit()
        if t.bounds.isInside(c[0], c[1]):
            print "c", c
            print t.bounds.isInside(c[0], c[1])
                # remove all instances of the polys in this group
            # from all other tiles
            home = t
    for p in g:
        for t in tiles:
            if t == home:
                print "home"
            if not t == home:
                # print "not"
                # pass
                if p in t.polys:
                    # print "found", p, "in", t
                    pass
            






areaids = []
# sort areas groups by apparent area
# print areas[0]
# print "groups:"
# print groups

# flatten lists
# groups2 = [item for sublist in list(groups) for item in sublist] 
groups2 = [item for sublist in groups for item in sublist] 
overlaps2 = [item for sublist in overlaps for item in sublist] 
# groups2 = list(set(groups2))
# overlaps2 = list(set(overlaps2))
overlap_count = len(overlaps2)

print "checking overlap areas:"
for i, g in enumerate(overlaps2):
    if i % (float(overlap_count)/100.0) == 0:
            stdout.write("\r%d%%" % abs(round((i/overlap_count * 100), 0)))
            stdout.flush()
    for h in overlaps2: 
        if (g.id == h.id):
            if len(g) != len(h):
                print "\nMISMATCH:"
                print g
                print h
                print "\n"
            # else: print "MATCH"
        # check for overlap greater than some area:
        elif ((g & h).area() > 5e-09):
            if not g.id in areaids:
                # print "\n\ng:\n", g
                areaids.append(g.id)
                areas.append(g)
            if not h.id in areaids:
                # print "h:\n", h
                areaids.append(h.id)
                areas.append(h)


print ""
print "polys in groups:", len(groups2)
print "strict overlaps:", len(overlaps2)
print "area overlaps:", len(areas)

areas.sort(key=lambda x: x.id)
# for a in areas:
#     print a.id
if len(groups2) > 0: writeSVG('groups.svg', groups2, height=800, stroke_width=(.2,.2), fill_opacity=((0),), )
if len(overlaps2) > 0: writeSVG('overlaps.svg', overlaps2, height=800, stroke_width=(.2,.2), fill_opacity=((0),), )
if len(areas) > 0: writeSVG('area.svg', areas, height=800, stroke_width=(.2,.2), fill_opacity=((0),), )



sys.exit()



## TODO
# track jpoly ids during Polygon() conversion
# check ids of all polys after conversion and remove jpolys not in the list
# group overlapping polys
# determine which is the "master" poly for each group
# assign each group to a tile by centroid of master poly
# move grouped jpolys to the appropriate tile
# write json tiles back out





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
    folder = "tiles1"
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
        