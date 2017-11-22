python collect.py --bounds 41.991794 -124.703541 46.299099 -116.463504 --zoom 12 --mapzen_api_key XXXXXX ./images/

for i in *.tif; do gdal_translate -ot UInt16 -of PNG -scale 0 8900 0 65536 -co worldfile=no --config GDAL_PAM_ENABLED NO $i ./converted/$i.png; done;

/Applications/Blender.app/Contents/MacOS/blender --python ../../dir_to_blender.py -- ./converted 1