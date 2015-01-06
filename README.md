landgrab
========

A python script to download vector tiles which contain a feature on OpenStreetMap.

![Manhattan](https://raw.githubusercontent.com/meetar/landgrab/master/manhattan.jpg)

## Requirements

- the python requests module: http://docs.python-requests.org/en/latest/user/install/#install

## Usage

python landgrab.py [osm id] [zoom level] [optional list-only flag]

- Manhattan Island: `python landgrab.py 3954665 15`
- Manhattan Island, list of tiles only: `python landgrab.py 3954665 15 1`
- Rhode Island: `python landgrab.py 392915 12`
- Indiana: `python landgrab.py 161816 9`
- Alaska: `python landgrab.py 1116270 6` (broken)

Test your downloads by viewing them on http://geojson.io/

## Todo:

- handle shapes which cross the International Date Line
