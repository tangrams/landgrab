#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## dedupe.py
## Peter Richardson, March 2015
##
## Remove duplicate features from a set of geojson tiles,
## group overlapping features in a FeatureCollection
## and move them all to a single tile based on the group's
## center of gravity
##
## Uses Polygon2 by Jörg Rädler
## https://bitbucket.org/jraedler/polygon2
##

## USAGE
##
## set "path" variable below
## run 'python dedupe.py'
## svg will be written to the same path
## deduped tiles will be written to a subdir called "dedupe"

from __future__ import division
import requests, json, time, datetime, math, re, sys, os
from sys import stdout
from numpy import *
import numpy as np
import colorsys
import xml.etree.ElementTree as ET
from random import randint
from Polygon import *
from Polygon.IO import *
import multiprocessing as mp
from multiprocessing import Pool

## location of .json files to process -
## eg: path = "tiles" will look inside ./tiles/

# path=sys.argv[1] # future
path = "manhattan/tiles1"

# Define an output queue
output = mp.Queue()


##
## class and function definitions
##

class Tile:
    def __init__(self, path, x, y, z, data):
        self.path = path
        self.filename = os.path.split(path)[1]
        self.x = x
        self.y = y
        self.data = data

        self.bounds = Polygon(((xtolong(x,z), ytolat(y,z)), (xtolong(x+1,z), ytolat(y,z)), (xtolong(x+1,z), ytolat(y+1,z)), (xtolong(x,z), ytolat(y+1,z))))
        
        self.bbox = [inf,inf,-inf,-inf]
        self.polys = []


def xtolong(x, z):
    return x / pow(2.0, z) * 360.0 - 180

def ytolat(y, z):
    n = 2.0 ** z
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    return math.degrees(lat_rad)


# expand bbox1 to include bbox2
def updateBbox(bbox1, bbox2):
    new = [bbox1[0], bbox1[1], bbox1[2], bbox1[3]]
    new[0] = min(bbox1[0], bbox2[0])
    new[1] = min(bbox1[1], bbox2[1])
    new[2] = max(bbox1[2], bbox2[2])
    new[3] = max(bbox1[3], bbox2[3])
    return new

# check for overlaps of a minimum area
def overlapsEnough(p, q):
    if p.overlaps(q):
        if ((p & q).area() > 5e-09): # magic number
            return True
    return False

# find the center of gravity of a polygon (average vertex position)
def centroid(p):
    c = [0,0]
    for v in p[0]:
        c = [c[0]+v[0], c[1]+v[1]]
    return (c[0]/len(p[0]), c[1]/len(p[0]))


# check for intersection of two bounding boxes
def bboxIntersect(bbox1, bbox2):
    if (bbox1[2]<bbox2[0] or bbox2[2]<bbox1[0] or bbox1[3]<bbox2[1] or bbox2[3]<bbox1[1]):
        return False
    else:
        return True

# write repeadedly to stdout on a single line
def printStatus(string):
    stdout.write("\r"+string)
    stdout.flush()

# def processTile(t, output):
def processTile(t):
    t.parsed = json.loads(t.data)
    # for each building
    buildings = t.parsed["buildings"]["features"]
    for b in buildings:
        # buildingcount += 1
        # make a list of all the contours in the jpoly
        contours = b["geometry"]["coordinates"]
       
        # new Polygon object
        poly = Polygon()
        poly.id = b["id"]

        # for each contour in the jpoly
        for c in contours:
            # remove last redundant coordinate from each contour
            del c[-1]

            # for each vertex
            # for v in c:
                # offset all verts in tile to arrange in scenespace
                # this isn't necessary when the data is coming straight from the json,
                # only when the data is coming from a tangram vbo
                # v = [v[0]+(4096*(tilemax[0]-tile.x)), v[1]+(4096*(tilemax[1]-tile.y))]

            poly.addContour(c)

            # update tile's bbox with contour's bbox
            t.bbox = updateBbox(t.bbox, list(poly.boundingBox()))

        poly.tile = t
        t.polys.append(poly)

    return t



if __name__ == '__main__':

    # # Define an output queue
    # output = mp.Queue()

    start_time = time.time()


    ##
    ## import files and assign to Tile objects
    ##

    files = []
    inf = float('inf')
    tilemin = [inf, inf]
    tilemax = [0, 0]
    p = re.compile('(\d*)-(\d*)-(\d*).*')
    for f in os.listdir(path):
        if f.endswith(".json"):
            files.append(path+"/"+f)
            # convert matches to ints and store in m
            m = [int(i) for i in p.findall(f)[0]]
            latlong = [m[1], m[2]]
            tilemin = [min(tilemin[0], latlong[0]), min(tilemin[1], latlong[1])]
            tilemax = [max(tilemax[0], latlong[0]), max(tilemax[1], latlong[1])]

    # print "min:", tilemin, "max:", tilemax

    tiles = []

    for t in files:
        f = open(t, 'r')

        # run the filename through the regex
        # m = saved matches 
        # example: [15, 9646, 12319]
        m = [int(i) for i in p.findall(t)[0]]
        filedata = f.read()
        tile = Tile(t, m[1], m[2], m[0], filedata)
        tiles.append(tile)

    print "Processing", len(tiles), "tiles:"


    ##
    ## convert json polys to Polygon() objects
    ##

    p = mp.Pool()


    tiles = p.map(processTile, tiles)
    print tiles[0].polys[0]
    print tiles[0].polys[0].id

    printStatus("100%")


    # make a list of all polys
    # this list comprehension is the same as the nested for loops below
    # neat, eh?
    # polys = [p for t in tiles for p in t.polys]

    polys = []
    for t in tiles:
        for p in t.polys:
            polys.append(p)

    print "\nChecking", len(polys), "polys for overlap:"

    groups = [] # all buildings

    # groups for debugging
    contains = [] # all shapes which completely contain other shapes
    overlaps = [] # all shapes which touch other shapes

    # still get overflow errors on this for large zoom values but it
    # doesn't seem to hurt anything
    total = np.float64(np.sum(range(len(polys)))*2)



    ##
    ## group overlapping polygons and assign whole groups to tiles
    ##

    # poly ids which have been grouped
    grouped = []
    # redundant tile polys to remove once the loop is complete
    toremove = []

    # for every tile
    for i, tile in enumerate(tiles):
        # for every poly in the tile
        for j, p in enumerate(tile.polys):

            # progress percentage indicator
            percent = abs(round(((len(grouped))/len(polys) * 100), 0))
            printStatus("%d%%"%percent)
            # if this is a copy of one we've already seen:
            if p.id in grouped:
                # it is redundant, mark it for removal
                # (can't remove an item from an array we're iterating over,
                # it'd throw off the index count and the loop would skip an item)
                toremove.append([tile, p])
                # skip to the next poly
                continue

            # otherwise, add it to the register
            grouped.append(p.id)        
            # start a new group
            group = [p]

            groupsToJoin = set()
            # check overlaps with polys in preexisting groups first
            for k, g in enumerate(groups):
                for poly in g:
                    # if p.id != poly.id and p.overlaps(poly):
                    if p.id != poly.id and overlapsEnough(p, poly):
                        groupsToJoin.add(k)

            groupsToJoin = list(groupsToJoin)

            # combine and flatten all implicated groups into the new group
            for i in groupsToJoin: group += groups[i]
            # once the combination is done, delete the implicated groups
            # (slightly more complex because groupsToJoin is a list of indices)
            # set groups to be the list all the elements which aren't indexed in groupsToJoin
            groups[:] = [x for ind, x in enumerate(groups) if ind not in groupsToJoin]

            # check against all other polys in all other tiles
            for t in tiles:
                # skip self, skip any tiles whose bbox doesn't overlap self's bbox
                if (tile == t) or (not bboxIntersect(tile.bbox, t.bbox)): continue

                # now checking tile.polys[p] against all polys 'q' in t.polys
                for q in t.polys:
                    # if q is a copy of p
                    if p.id == q.id:
                        # mark it for removal
                        toremove.append([t, q])
                        # skip to next q poly
                        continue
                    # if p overlaps q significantly:
                    if overlapsEnough(p, q):
                        good = True
                        # if q is already in the group, mark it for removal
                        for x in group:
                            if x.id == q.id:
                                toremove.append([t, q])
                                good = False
                        # otherwise add q to the group
                        if good: group.append(q)

            groups.append(group)


    printStatus("100%")

    for g in groups:
        if len(g) > 1:
            overlaps.append(g)

    # print "groups:", len(grouped)
    # print "removed:", len(toremove)
    print "\nRemoving", len(toremove), "redundant polys:"

    # remove redundant polys
    # each entry is a list: [tile, poly]
    for i, r in enumerate(toremove):
        # progress percentage indicator
        percent = abs(round((i/len(toremove) * 100), 0))
        printStatus("%d%%"%percent)

        if r[1] in r[0].polys:

            # this seems to be unnecessary - a single json tile typically has no dupes
            # # find the associated source json
            # # if it's in there more than once
            # if sum(f["id"] == r[1].id for f in r[0].parsed["buildings"]["features"]) > 1:
            #     j = next((f for f in r[0].parsed["buildings"]["features"] if f["id"] == r[1].id), None)
            #     # remove it
            #     if j != None:
            #         r[0].parsed["buildings"]["features"].remove(j)
            #         # del j

            # remove the poly from the tile's poly list
            r[0].polys.remove(r[1])

    printStatus("100%")


    print "\nAssigning", len(groups), "groups to tiles:"
    # assign groups to tiles
    for i, g in enumerate(groups):
        # progress percentage indicator
        percent = abs(round((i/len(groups) * 100), 0))
        printStatus("%d%%"%percent)

        # sort all polys in group by area
        g.sort(key=lambda p: p.area)
        # assume poly with largest area is the outermost polygon
        outer = g[0]
        # find "home" tile in which the outer's centroid lies
        c = centroid(outer)
        home = None
        for i, t in enumerate(tiles):
            if t.bounds.isInside(c[0], c[1]):
                home = t
        # if the poly's centroid is outside of all the tiles,
        # just use the tile the poly started in
        if home == None:
            home = outer.tile

        # for each polygon in the group
        for p in g:
            # if the poly isn't already there
            if home != p.tile:
                # copy poly to home tile
                home.polys.append(p)
                # find the associated source json, using the poly's .tile attribute
                for i, f in enumerate(p.tile.parsed["buildings"]["features"]):
                    if f["id"] == p.id:
                        # copy it over too
                        home.parsed["buildings"]["features"].append(f)

            # remove the poly and the json from all other tiles
            for t in tiles:
                if t != home:
                    # find and remove the poly
                    if p in t.polys:
                        t.polys.remove(p)
                    # find and remove the json
                    for f in t.parsed["buildings"]["features"]:
                        if f["id"] == p.id:
                            t.parsed["buildings"]["features"].remove(f)

    printStatus("100%")


    print "\nWriting JSON"
    ## json output
    if not os.path.exists(path+'/deduped/'):
        os.mkdir(path+'/deduped/')
    for i, t in enumerate(tiles):
        # progress percentage indicator
        percent = abs(round((i/len(tiles) * 100), 0))
        printStatus("%d%%"%percent)
        with open(path+'/deduped/'+t.filename, 'w') as outfile:

            # # write a single layer:
            # json.dump(t.parsed["buildings"], outfile)

            # write everything:
            json.dump(t.parsed, outfile)

    printStatus("100%")

    print "\nWriting SVG"
    ## SVG output
    ##

    # flatten lists for writing to svg
    groups2 = [item for sublist in groups for item in sublist] 
    overlaps2 = [item for sublist in overlaps for item in sublist] 

    # 'strokecolor' parameter is a tuple of RGB values, one for each polygon
    strokecolor = ()
    allpolys = []
    for i, t in enumerate(tiles):
        # color each tile randomly
        color = ((colorsys.hsv_to_rgb(random.random(), 1., 1.)),)
        color = (tuple([int(c*255) for c in list(color[0])]),)

        # add tile bounds to polys list, to visualize it in the svg
        allpolys.append(t.bounds)
        # add a color entry for the tile bounds rectangle
        strokecolor += color

        for p in t.polys:
            # add the poly to the poly list
            allpolys.append(p)
            # add a corresponding color entry to the colors list
            strokecolor += color

        # write one svg per tile:
        if len(t.polys) > 0:
            writeSVG(path+'/'+'%s.svg'%t.filename, t.polys, height=800, stroke_width=(1, 1), stroke_color=color, fill_opacity=((0),), )

    # write one big svg
    if len(allpolys) > 0:
        writeSVG(path+'/'+'allpolys.svg', allpolys, height=2000, stroke_width=(2, 2), stroke_color=strokecolor, fill_opacity=((0),), )

    printStatus("100%")

    elapsed = time.time() - start_time
    print "\nDone in", datetime.timedelta(seconds=elapsed)
    sys.exit()

    # done!