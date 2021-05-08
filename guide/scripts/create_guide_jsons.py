"""Utility script to create training json file for wakeword.
There should be two directories. one that has all of the 0 labels
and one with all the 1 labels
"""
import os
import argparse
import json
import random


def main(args):
	data = []
	for i in range(6):
		class_dir = os.path.join(args.dataset_dir, str(i))
		files = os.listdir(class_dir)
		percent = args.percent
		for f in files:
			data.append({
            "key": os.path.join(class_dir, f),
            "label": i
        })

	random.shuffle(data)

	f = open(args.save_json_path +"/"+ "train.json", "w")
    
	with open(args.save_json_path +"/"+ 'train.json','w') as f:
		d = len(data)
		i=0
		while(i<int(d-d/percent)):
			r=data[i]
			line = json.dumps(r)
			f.write(line + "\n")
			i = i+1
    
	f = open(args.save_json_path +"/"+ "test.json", "w")

	with open(args.save_json_path +"/"+ 'test.json','w') as f:
		d = len(data)
		i=int(d-d/percent)
		while(i<d):
			r=data[i]
			line = json.dumps(r)
			f.write(line + "\n")
			i = i+1
    

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""
	Utility script to create training json file for wakeword.
	There should be two directories. one that has all of the 0 labels
	and one with all the 1 labels """
	)
	parser.add_argument('--dataset_dir', type=str, default="/home/greatman/data/guide", required=False,
						help='directory of clips with zero labels')
	parser.add_argument('--save_json_path', type=str, default="/home/greatman/code/vics/guide/neuralnet", required=False,
						help='path to save json file')
	parser.add_argument('--percent', type=int, default=7, required=False,
						help='percent of clips put into test.json instead of train.json')
	args = parser.parse_args()

	main(args)
