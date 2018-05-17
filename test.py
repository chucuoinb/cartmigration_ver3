from libs.utils import *
import json
import pprint
sample = {
	'a': 'b',
	'c': 'd',
}
log(12345,sample)

with open('result.json', 'w') as fp:
    json.dump(sample, fp)