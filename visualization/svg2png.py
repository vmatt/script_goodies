import os
import cairosvg
from PIL import Image, ImageChops

def get_path_filename(filename):
    return os.path.normpath(os.path.dirname(os.path.realpath(__file__))) + '/' + filename

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


svgs = os.listdir(get_path_filename("svg/"))

for img in svgs:
    svg_path = get_path_filename("svg/"+img)
    png_path = get_path_filename("png/"+img.split(".")[0]+".png")
    cairosvg.svg2png(
        url=svg_path, write_to=png_path)
    try:
        im = Image.open(png_path)
        im = trim(im)
        im.save(png_path)
    except AttributeError:
        print(png_path+" not existing??")
