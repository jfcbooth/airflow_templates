from flatten_json import flatten
import json
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', type=str, required=True, help='input file name')
ap.add_argument('-o', '--output', type=str, required=True, help='output file name')
args = vars(ap.parse_args())

data = []
for line in open(args['input'], 'r'):
    data.append(json.loads(line))
data_flatten = [flatten(d) for d in data]

df = pd.DataFrame(data_flatten)
df.to_csv(args['output'])