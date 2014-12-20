landgrab
========

A python script to download vector tiles which contain a feature on openstreetmap and save them in a directory, which you can then view on http://geojson.io/

![Manhattan](https://raw.githubusercontent.com/meetar/landgrab/master/manhattan.jpg)

## Requirements

- the python requests module: http://docs.python-requests.org/en/latest/user/install/#install

## Usage

python landgrab.py [osm id] [zoom level]

- Manhattan Island: `python landgrab.py 3954665 15`
- Rhode Island: `python landgrab.py 392915 12`
- Indiana: `python landgrab.py 161816 9`
- Alaska: `python landgrab.py 1116270 6` (broken)

## Todo:

- handle shapes which cross the international dateline
