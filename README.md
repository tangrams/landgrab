landgrab
========

A python script to download vector tiles which contain a feature on openstreetmap.

![Manhattan](https://raw.githubusercontent.com/meetar/landgrab/master/manhattan.jpg)

## Requirements

- the python requests module: http://docs.python-requests.org/en/latest/user/install/#install

## Usage

Currently only tested with the outline of Manhattan: www.openstreetmap.org/relation/3954665

    python landgrab.py 3954665

Will save the relevant tiles in a tiles directory, which you can then view on http://geojson.io/
