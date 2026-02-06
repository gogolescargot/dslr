import csv
import pickle as pkl
import pandas as pd

import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def load_data(path):
    data_frame = pd.read_csv(path, index_col="Index")
    X = data_frame[
        [
            "Arithmancy",
            "Astronomy",
            "Herbology",
            "Defense Against the Dark Arts",
            "Divination",
            "Muggle Studies",
            "Ancient Runes",
            "History of Magic",
            "Transfiguration",
            "Potions",
            "Care of Magical Creatures",
            "Charms",
            "Flying",
        ]
    ].values
    return X


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
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        fields = ["Index", "Hogwarts House"]
        houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
        m, _ = X.shape

        writer.writerow(fields)
        for i in range(m):
            writer.writerow([i, houses[predictions[i]]])


def main():
    try:
        X = load_data("datasets/dataset_test.csv")

        with open("thetas.pkl", "rb") as file:
            data = pkl.load(file)
        thetas = data

        X = np.nan_to_num(X, nan=0.0)
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)
        X = (X - X_min) / (X_max - X_min)

        predictions = predict(X, thetas)

        csv_write("houses.csv", X, predictions)

    except FileNotFoundError:
        print("Error: The file 'data.pkl' was not found.")
    except KeyError as e:
        print(f"Error: Missing key in the data file: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
