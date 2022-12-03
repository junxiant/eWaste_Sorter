# import xml.etree.ElementTree as ET
# import glob
# import os
# import json
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--labelinput', help='XML directory', required=True)
# parser.add_argument('--imageinput', help='Images directory', required=True)
# parser.add_argument('--output', help='Output directory', required=True)

# args = parser.parse_args()

# def xml_to_yolo_bbox(bbox, w, h):
#     # xmin, ymin, xmax, ymax
#     x_center = ((bbox[2] + bbox[0]) / 2) / w
#     y_center = ((bbox[3] + bbox[1]) / 2) / h
#     width = (bbox[2] - bbox[0]) / w
#     height = (bbox[3] - bbox[1]) / h
#     return [x_center, y_center, width, height]

# classes = []
# input_dir = args.labelinput
# output_dir = args.output
# image_dir = args.imageinput

# # create the labels folder (output directory)
# os.makedirs(output_dir)

# # identify all the xml files in the annotations folder (input directory)
# files = glob.glob(os.path.join(input_dir, '*.xml'))
# # loop through each 
# for fil in files:
#     basename = os.path.basename(fil)
#     filename = os.path.splitext(basename)[0]
#     # check if the label contains the corresponding image file
#     if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
#         print(f"{filename} image does not exist!")
#         continue

#     result = []

#     # parse the content of the xml file
#     tree = ET.parse(fil)
#     root = tree.getroot()
#     width = int(root.find("size").find("width").text)
#     height = int(root.find("size").find("height").text)

#     for obj in root.findall('object'):
#         label = obj.find("name").text
#         print('label', label)
#         # check for new classes and append to list
#         if label not in classes:
#             classes.append(label)
#         index = classes.index(label)
#         pil_bbox = [int(x.text) for x in obj.find("bndbox")]
#         yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
#         # convert data to string
#         bbox_string = " ".join([str(x) for x in yolo_bbox])
#         result.append(f"{index} {bbox_string}")

#     if result:
#         # generate a YOLO format text file for each xml file
#         with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
#             f.write("\n".join(result))

# with open('classes.txt', 'w', encoding='utf8') as f:
#     f.write(json.dumps(classes))

import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--labelinput', help='XML directory', required=True)
parser.add_argument('--imageinput', help='Images directory', required=True)
parser.add_argument('--output', help='Output directory', required=True)

args = parser.parse_args()

dirs = ['train', 'val']
classes = ["person", "vest", "white", "glass", "yellow", "blue", "red", "head"]

def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + '/' + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# cwd = getcwd()

# for dir_path in dirs:
    # full_dir_path = cwd + '/' + dir_path
    # output_path = full_dir_path +'/yolo/'
output_path = args.output

if not os.path.exists(output_path):
    os.makedirs(output_path)

image_paths = getImagesInDir(args.imageinput)
# list_file = open(args.output + '.txt', 'w')

for image_path in image_paths:
    # list_file.write(image_path + '\n')
    convert_annotation(args.labelinput, output_path, image_path)
# list_file.close()

    # print("Finished processing: " + dir_path)