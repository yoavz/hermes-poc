from difflib import get_close_matches
from pprint import pprint
from os import listdir
import json

tags = list()
buckets = dict()

json_files = [ f for f in listdir('.') if f.endswith('.json') ]

for json_file in json_files:
    print 'Building tag buckets for %s ...' % json_file
    data = []
    with open(json_file, 'r') as f:
        try:
            for line in f:
                data.append(json.loads(line))
        except:
            print 'Could not parse file %s' % json_file
            continue
    for deal in data:
        deal_tags = deal.get('tags')
        if not deal_tags:
            continue
        for t in deal_tags:
            if t not in tags:
                tags.append(t)
                buckets[t] = list()
            buckets[t].append(deal)

while(True):
    i = raw_input('Search for keyword (x to quit):')
    if i == 'x':
       exit(0)
    matches = get_close_matches(i, tags)
    if not matches:
        print 'No match for %s, try again?' % i
    else:
        pprint(buckets[matches[0]])
        print 'Tag used: %s' % matches[0] 
