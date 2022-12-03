import argparse
import glob 

parser = argparse.ArgumentParser()
parser.add_argument('--labelinput', help='txt directory', required=True)

args = parser.parse_args()

path = args.labelinput

for files in glob.glob(path +"/*.txt"):
    edited = []
    with open(files, 'r+') as f:
        for line in f:
            cls_id = line.split(' ')
            if cls_id[0] == '2' or cls_id[0] == '4' or cls_id[0] == '5' or cls_id[0] == '6':
                cls_id[0] = '4'
                # print("replacing")
            elif cls_id[0] == '7':
                cls_id[0] = '4'
            edited.append(cls_id)
    # print(edited)
    with open(files, "r+") as f:
        for m in edited:
            f.write(" ".join([str(x) for x in m]))    