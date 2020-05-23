from flatten_json import flatten
import json
import pandas as pd
import os

def json2csv(**kwargs):
    """
    Takes .json or .nljson file, flattens the file, and outputs to a .csv.
    """
    # check input and output strings
    filename, file_ext = os.path.splitext(kwargs['input'])
    if not file_ext == ".json" and not file_ext == ".nljson":
        print("{} not .json or .nljson file".format(kwargs['input']))
        exit(1)
    filename, file_ext = os.path.splitext(kwargs['output'])
    if not file_ext == ".csv":
        print("{} not .csv file".format(kwargs['output']))
        exit(1)

    # read in json file
    data = []
    for line in open(kwargs['input'], 'r'):
        data.append(json.loads(line))
    data_flatten = [flatten(d) for d in data]

    # output flattened data to csv
    df = pd.DataFrame(data_flatten)
    df.to_csv(kwargs['output'])
