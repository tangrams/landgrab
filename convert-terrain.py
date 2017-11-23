# converts mapzen terrarium pngs to 16-bit greyscale pngs

from PIL import Image
import sys
import os
import png

try:
    args = list(reversed(sys.argv))
    idx = args.index("--")

except ValueError:
    params = []

else:
    params = args[:idx][::-1]
    file = args[0]

# print("Script params:", params)
# print("file:", file)

def unpack(h):
    # unpack data to [-32768 - 32768], the range in the raw data
    v = (h[0] * 256 + h[1] + h[2] / 256) - 32768;
    # pypng doesn't like negative values
    v = max(v, 0);
    return v;

im = Image.open(file)
pix = im.load()

# print(unpack(pix[0,0]))

rows = [];
for y in range(0,im.size[0]):
    row = [];
    for x in range(0,im.size[1]):
        row.append(unpack(pix[x,y]))
    rows.append(row);

with open('./images/converted/'+os.path.splitext(os.path.basename(file))[0]+"-gray.png", 'wb') as f:
    # save as 16-bit grayscale png
    writer = png.Writer(width=im.size[0], height=im.size[1], bitdepth=16, greyscale=True)
    writer.write(f, rows)

