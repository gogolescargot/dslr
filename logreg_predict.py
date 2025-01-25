#!/usr/bin/python3

import pickle as pkl
import numpy as np
import csv

def sigmoid(z):
	return 1 / (1 + np.exp(-z))

def predict(X, thetas):
	scores = np.dot(X, thetas.T)
	
	probabilities = sigmoid(scores)
	
	predictions = []
	for i in range(len(probabilities)):
		max_prob = -1
		max_class = -1
		for j in range(len(probabilities[i])):
			if probabilities[i][j] > max_prob:
				max_prob = probabilities[i][j]
				max_class = j
		predictions.append(max_class)

	return np.array(predictions)

def csv_write(path, X, predictions):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file)
		fields = ["Index", "Hogwarts House"]
		houses = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
		m, _ = X.shape

		writer.writerow(fields)
		for i in range(m):
			writer.writerow([i, houses[predictions[i]]])

def main():
	with open('data.pkl', 'rb') as file:
		data = pkl.load(file)
	
	X = data['X']
	thetas = data['thetas']
	
	predictions = predict(X, thetas)

	csv_write('houses.csv', X, predictions)

if __name__ == '__main__':
	main()
