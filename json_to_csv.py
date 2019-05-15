import sys, json, csv, time
from collections import Mapping
from itertools import chain
from operator import add

# Flatten dictionary and adding nested keys together
_FLAG_FIRST = object()
def flattenDict(d, join=add, lift=lambda x:x):
    results = []
    def visit(subdict, results, partialKey):
        for k,v in subdict.items():
            newKey = lift(k) if partialKey==_FLAG_FIRST else join(partialKey,lift(k))
            if isinstance(v,Mapping):
                visit(v, results, newKey)
            else:
                results.append((newKey,v))
    visit(d, results, _FLAG_FIRST)
    return dict(results)

# Parse dictionaries to CSV
def json_to_csv(input):

  # Loading json & creating _syn.csv file
  output = str(input) + '_syn.csv'
  with open(input, 'r') as json_file, open(output, 'w+') as csv_file:
    csv_output = csv.writer(csv_file, delimiter=";", quoting=csv.QUOTE_ALL)
    json_list = json_file.readlines()
    json_data = json.loads(json.dumps(json_list))
    
    # Generating headers
    print "Generating headers..."
    headers = set([])
    for i in json_data:
      i = flattenDict(json.loads(i))
      for key in i:
        headers.add(key)
    headers = list(headers)
    csv_output.writerow(headers)
    
    # Writing lines
    print "Writing lines..."
    for i in json_data:
      i = flattenDict(json.loads(i))
      line = {str(h):"" for h in headers}
      for key in i:
        line[key] = i[key]
      csv_output.writerow(line.values())

infile = input("Filename: ")

start = time.time()
json_to_csv(in_file)
end = time.time()

print "Done. Parsing took " + str(round(end - start, 3)) + " seconds. A new file ending on _syn.csv has been created in the same folder as the original file"
