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
        icons[fname] = Image.open(img_url).convert('RGBA')

BarsIcon = icons['bars']
PlusIcon = icons['plus']
CheckIcon = icons['check']
CheckDoubleIcon = icons['check-double']
XMarkIcon = icons['xmark']
CalendarCheckIcon = icons['calendar-check']
CalendarDaysIcon = icons['calendar-days']
CalendarPlusIcon = icons['calendar-plus']
CalendarXMarkIcon = icons['calendar-xmark']
GearIcon = icons['gear']
PlusSquareIcon = icons['plus-square']
PlusSQuareRIcon = icons['plus-square-r']
SquareIcon = icons['square']
SquareCheckIcon = icons['square-check']
SquarePlusIcon = icons['square-plus']
TrashCanIcon = icons['trash-can']
SquareXMarkIcon = icons['square-xmark']
NoteStickyIcon = icons['note-sticky']
ClipboardIcon = icons['clipboard']
ClipboardRIcon = icons['clipboard-r']
CloudArrowDownIcon = icons['cloud-arrow-down']
