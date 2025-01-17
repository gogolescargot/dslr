#!/usr/bin/python3

from itertools import combinations
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import click

def check_csv(data_frame):
	data_frame_keys = {
		'Hogwarts House': object,
		'First Name': object,
		'Last Name': object,
		'Birthday': object,
		'Best Hand': object,
		'Arithmancy': float,
		'Astronomy': float,
		'Herbology': float,
		'Defense Against the Dark Arts': float,
		'Divination': float,
		'Muggle Studies': float,
		'Ancient Runes': float,
		'History of Magic': float,
		'Transfiguration': float,
		'Potions': float,
		'Care of Magical Creatures': float,
		'Charms': float,
		'Flying': float
	}

	if list(data_frame.columns) != list(data_frame_keys.keys()):
		raise Exception("CSV Error: Wrong columns")

	for col, dtype in data_frame_keys.items():
		i = 0
		for elem in data_frame[col]:
			if not isinstance(elem, dtype):
				raise Exception(f"CSV Error: wrong element type: find in {col}: type {type(elem)}, expected {dtype}")
			if col == 'Hogwarts House' and elem not in ['Ravenclaw', 'Slytherin', 'Hufflepuff', 'Gryffindor']:
				raise Exception(f"CSV Error: wrong hogwarts house: line {i}, find {elem}, expected Ravenclaw, Slytherin, Hufflepuff or Gryffindor")
			if col == 'Best Hand' and elem not in ['Left', 'Right']:
				raise Exception(f"CSV Error: wrong best hand: line {i}, find {elem}, expected Left or Right")
			i += 1
	return 0

@click.command()
@click.option('--path', default="datasets/dataset_train.csv", help="Path of the CSV data file")
def main(path):
	data_frame = pd.read_csv(path, index_col='Index')

	check_csv(data_frame)

	for course_1, course_2 in combinations(data_frame.keys()[5:], 2):
		sb.scatterplot(data=data_frame, x=data_frame[course_1], y=data_frame[course_2], hue="Hogwarts House")
		plt.title(f"Scatter Plot of {course_1} and {course_2}")
		plt.xlabel(f"{course_1} Score")
		plt.ylabel(f"{course_2} Score")
		plt.show()

if __name__ == '__main__':
	main()