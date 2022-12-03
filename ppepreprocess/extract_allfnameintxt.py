
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Input folder', required=True)

args = parser.parse_args()

input_dir = args.input
split_type = input_dir.split('/')
ttype = split_type[-1]

# Write txt file containing all image dir
files = glob.glob(os.path.join(input_dir, '*.jpg'))
for f in files:
    a = f.split('/')
    iname = a[-1]
    # print(iname)
    with open((f'./{ttype}.txt'), 'a') as file:
        file.write(f'./images/{ttype}/{iname}' + '\n')
