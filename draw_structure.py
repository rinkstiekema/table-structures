import sys
import os
import json
from PIL import Image, ImageDraw

if len(sys.argv) < 4:
    print("Missing arguments. Usage: <image_folder> <image_json_file> <tex_json_files>")
    exit(-1)

image_folder = sys.argv[1]
image_json_path = sys.argv[2]
tex_json_path = sys.argv[3]

image_files = os.listdir(image_folder)


def draw_structure(image_url, shape):
    im = Image.open(image_url)
    draw = ImageDraw.Draw(im)

    col_offset = (im.size[0]-1) / shape[0]
    row_offset = im.size[1] / shape[1]

    col_pos = 0
    row_pos = 0

    while col_pos <= im.size[0]:
        draw.line((col_pos, 0, col_pos, im.size[1]), fill=128, width=1)
        col_pos += col_offset

    while row_pos <= im.size[1]:
        draw.line((0, row_pos, im.size[0], row_pos), fill=128, width=1)
        row_pos += row_offset

    im.show(command='fim')


with open(tex_json_path) as tex_json_file:
    tex_json = json.load(tex_json_file)[1]
    with open(image_json_path) as image_json_file:
        image_json = json.load(image_json_file)[1]
        draw_structure(image_json['renderURL'], tex_json['shape'])
