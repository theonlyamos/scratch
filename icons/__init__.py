#from cairosvg import svg2png
from PIL import Image

#from io import BytesIO
import os


icons = {}

folder = os.path.realpath(os.path.join(os.curdir, 'icons'))

for fd in os.listdir(folder):
    fname, ext = os.path.splitext(fd)
    if ext == '.png':
        img_url = os.path.realpath(os.path.join(os.curdir, 'icons', fd))
        
        if 'plane' in fname:
            icons[fname] = Image.open(img_url).convert('RGBA')
        else:
            icons[fname] = Image.open(img_url).convert('RGBA').resize((12, 12))
