# Split into train/val
import splitfolders
import argparse
import os 

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Input directory', required=True)
parser.add_argument('--output', help='Output directory', required=True)
parser.add_argument('--seed', help='Seed', required=True)

args = parser.parse_args()

# Get args
f_input = args.input
f_output = args.output
seed = int(args.seed)

# Split
splitfolders.ratio(f_input, output=f_output, seed=seed, ratio=(0.8,0.1,0.1)) 

