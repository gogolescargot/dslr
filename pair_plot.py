#!/usr/bin/python3

import seaborn as sns
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

	data_frame_keys = {key: key[:5] for key in data_frame.keys()[5:]}

	data_frame.rename(columns=data_frame_keys, inplace=True)

	pair_plot = sns.pairplot(data=data_frame, hue="Hogwarts House", diag_kind='hist', diag_kws={'multiple': 'stack'})

	new_labels = [house[:5] for house in set(data_frame["Hogwarts House"])]

	for t, l in zip(pair_plot._legend.texts, new_labels):
		t.set_text(l)

	sns.move_legend(pair_plot, "center right", ncol=1, title=None, frameon=False)

	for ax in pair_plot.axes.flatten():
		ax.set_xticks([])
		ax.set_yticks([])
				
	plt.show()

if __name__ == '__main__':
	main()