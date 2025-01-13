# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    describe.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ggalon <ggalon@student.42lyon.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/13 11:39:15 by ggalon            #+#    #+#              #
#    Updated: 2025/01/13 15:04:41 by ggalon           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv
import math

def count(array):
	array = [x for x in array if not math.isnan(x)]
	return len(array)

def mean(array):
	array = [x for x in array if not math.isnan(x)]
	return sum(array) / len(array)

def std(array):
	array = [x for x in array if not math.isnan(x)]
	mean = sum(array) / len(array)
	variance = sum((x - mean) ** 2 for x in array) / (len(array))
	return math.sqrt(variance)

def percentile(array, percent):
	array = [x for x in array if not math.isnan(x)]

	k = (len(array) - 1) * percent
	f = math.floor(k)
	c = math.ceil(k)

	if f == c:
		return array[int(k)]

	d0 = array[int(f)] * (c - k)
	d1 = array[int(c)] * (k - f)

	return d0 + d1

columns = [
	"index", "hogwarts_house", "first_name", "last_name", "birthday", "best_hand",
	"arithmancy", "astronomy", "herbology", "defense_against_the_dark_arts",
	"divination", "muggle_studies", "ancient_runes", "history_of_magic",
	"transfiguration", "potions", "care_of_magical_creatures", "charms", "flying"
]

data = {col: [] for col in columns}

with open('datasets/dataset_test.csv') as csvfile:
	reader = csv.reader(csvfile)
	features = next(reader)
	
	for row in reader:
		for i, col in enumerate(columns):
			if i < 6:
				data[col].append(row[i])
			else:
				data[col].append(float(row[i]) if row[i] else math.nan)

print(' '.join(features))

def print_stat(stat_name, func, is_count=False, round_val=False):

	print(stat_name, end=" ")

	for col in columns:
		if col in ["index", "hogwarts_house", "first_name", "last_name", "birthday", "best_hand"]:
			if is_count:
				print(len(data[col]), end=" ")
			else:
				print('   ', end=" ")
		else:
			value = func(data[col])

			if round_val:
				value = round(value, 2)

			print(value, end=" ")

	print()

print_stat('Count', lambda x: count(x), is_count=True, round_val=False)
print_stat('Mean', lambda x: mean(x), round_val=True)
print_stat('Std', lambda x: std(x), round_val=True)
print_stat('Min', lambda x: min(x), round_val=True)
print_stat('25%', lambda x: percentile(x, 0.25), round_val=True)
print_stat('50%', lambda x: percentile(x, 0.50), round_val=True)
print_stat('75%', lambda x: percentile(x, 0.75), round_val=True)
print_stat('Max', lambda x: max(x), round_val=True)