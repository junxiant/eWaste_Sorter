# Separate xml and img files
import shutil
import argparse
import os 
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Input directory', required=True)
parser.add_argument('--output', help='Output directory', required=True)

args = parser.parse_args()

# Input folder
folder_dir = args.input

# If output dir does not exist, create
try:
    if not os.path.isdir(args.output):
        os.makedirs(args.output+'_img')
        os.makedirs(args.output+'_img/img')

        os.makedirs(args.output+'_xml')
        os.makedirs(args.output+'_xml/xml')
except:
    print("Folder already exists.")
        
for files in glob.glob(folder_dir+'/*'):
    file_name, file_ext = os.path.splitext(files)
    file_name_split = file_name.split('/')

    if file_ext == '.xml':
        shutil.move(files, f'./{args.output}_xml/xml/'+file_name_split[-1]+'.xml')
        
    elif file_ext == '.jpg':
        shutil.move(files, f'./{args.output}_img/img/'+file_name_split[-1]+'.jpg')
