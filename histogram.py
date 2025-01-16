# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    histogram.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ggalon <ggalon@student.42lyon.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/16 15:24:51 by ggalon            #+#    #+#              #
#    Updated: 2025/01/16 17:06:34 by ggalon           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv
import math
import matplotlib.pyplot as plt

def mean(array):
	array = [x for x in array if not math.isnan(x)]
	return sum(array) / len(array)

def std(array):
	array = [x for x in array if not math.isnan(x)]
	mean = sum(array) / len(array)
	variance = sum((x - mean) ** 2 for x in array) / (len(array))
	return math.sqrt(variance)

def read_csv(path):
	with open(path) as csvfile:
		reader = csv.reader(csvfile)
		features = next(reader)
		data = {feature: [] for feature in features}

		for row in reader:
			for i, feature in enumerate(features):
				if i < 6:
					data[feature].append(row[i])
				else:
					data[feature].append(float(row[i]) if row[i] else math.nan)
	return features, data

def compute_stats(data, features):
	
	houses_set = set(data['Hogwarts House'])
	features_group = {feature: {house: [] for house in houses_set} for feature in features[6:]}

	for feature in features[6:]:
		for i, score in enumerate(data[feature]):
			features_group[feature][data['Hogwarts House'][i]].append(score)

	for feature in features[6:]:
		for house in houses_set:
			features_group[feature][house] = mean(features_group[feature][house])

	for feature in features[6:]:
		features_group[feature] = std([features_group[feature][house] for house in houses_set])

	return features_group

def display_stats(std_houses):
	print(f"Most homogeneous score distribution: {min(std_houses, key=std_houses.get)}; {min(std_houses.values())}")
	
	courses = list(std_houses.keys())
	std_devs = list(std_houses.values())
	
	plt.bar(courses, std_devs, width=0.5)
	
	plt.xlabel('Courses')
	plt.ylabel('Standard Deviation')
	
	plt.xticks(rotation=90)
	
	plt.show()

def main():
	file_path = 'datasets/dataset_train.csv'
	features, data = read_csv(file_path)
	
	std_houses = compute_stats(data, features)

	# print(std_houses)

	display_stats(std_houses)

if __name__ == "__main__":
	main()