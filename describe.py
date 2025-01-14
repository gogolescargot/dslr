# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    describe.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ggalon <ggalon@student.42lyon.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/13 11:39:15 by ggalon            #+#    #+#              #
#    Updated: 2025/01/14 20:56:16 by ggalon           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv
import math
import pandas as pd

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
	array.sort()

	k = (len(array) - 1) * percent
	f = math.floor(k)
	c = math.ceil(k)

	if f == c:
		return array[int(k)]

	d0 = array[int(f)] * (c - k)
	d1 = array[int(c)] * (k - f)

	return d0 + d1

def max_len(array):
	max = 0
	for elem in array:
		if len(elem) > max:
			max = len(elem)
	return max

columns = [
	"Index", "Hogwarts House", "First Name", "Last Name", "Birthday", "Best Hand",
	"Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts",
	"Divination", "Muggle Studies", "Ancient Runes", "History of Magic",
	"Transfiguration", "Potions", "Care of Magical Creatures", "Charms", "Flying"
]

data = {col: [] for col in columns}

with open('datasets/dataset_train.csv') as csvfile:
	reader = csv.reader(csvfile)
	features = next(reader)
	
	for row in reader:
		for i, col in enumerate(columns):
			if i < 6:
				data[col].append(row[i])
			else:
				data[col].append(float(row[i]) if row[i] else math.nan)

stat_len = 7

def print_stat(stat_name, func, round_val=False):

	print(f"{stat_name:<{stat_len}}", end="  ")

	for i, col in enumerate(columns[6:]):
		value = func(data[col])

		if round_val:
			value = round(value, 6)

		print(f"{value:>{feature_len[i]}}", end="  ")

	print()

feature_len = []

print(' ' * stat_len, end="  ")

for feature in columns[6:]:
	if (len(feature) < 12):
		value = 12
	else:
		value = len(feature)

	feature_len.append(value)
	print(f"{feature:>{value}}", end="  ")
	
print()

print_stat('count', lambda x: count(x), round_val=False)
print_stat('mean', lambda x: mean(x), round_val=True)
print_stat('std', lambda x: std(x), round_val=True)
print_stat('min', lambda x: min(x), round_val=True)
print_stat('25%', lambda x: percentile(x, 0.25), round_val=True)
print_stat('50%', lambda x: percentile(x, 0.50), round_val=True)
print_stat('75%', lambda x: percentile(x, 0.75), round_val=True)
print_stat('max', lambda x: max(x), round_val=True)


df = pd.read_csv('datasets/dataset_train.csv')

summary = df.describe()

print(summary)