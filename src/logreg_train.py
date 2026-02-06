import pickle as pkl

import click
import numpy as np
import pandas as pd


def get_data(path):
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
    y = data_frame["Hogwarts House"].values
    return X, y


def normalize(X, y):
    for i, elem in enumerate(y):
        if elem == "Gryffindor":
            y[i] = 0
        elif elem == "Hufflepuff":
            y[i] = 1
        elif elem == "Ravenclaw":
            y[i] = 2
        elif elem == "Slytherin":
            y[i] = 3

    if np.any(np.isnan(X)):
        X = np.nan_to_num(X, nan=0.0)

    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    X = (X - X_min) / (X_max - X_min)

    return X, y


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def cost(theta, X, y):
    m = len(y)
    prediction = sigmoid(np.dot(X, theta))
    return sum(y * np.log(prediction) + (1 - y) * np.log(1 - prediction)) / -m


def gradient(X, y, m, prediction):
    return np.dot(X.T, prediction - y) / m


def log_reg(X, y, learning_rate=0.01, max_iterations=10000):
    m, n = X.shape
    theta = np.zeros(n)
    old_cost = 0

    for i in range(max_iterations):
        prediction = sigmoid(np.dot(X, theta))
        gradient_value = gradient(X, y, m, prediction).astype(np.float64)
        theta -= learning_rate * gradient_value
        cost_value = cost(theta, X, y)

        if cost_value == old_cost:
            break

        old_cost = cost_value

        if i % 1000 == 0:
            print(f"Iteration {i}, Cost: {cost_value}")

    return theta


def one_vs_all(X, y, learning_rate=0.1, max_iterations=1000):
    _, n = X.shape
    thetas = np.zeros((4, n))
    for i in range(4):
        y_binary = (y == i).astype(int)
        print(f"Training classifier for class {i}")
        thetas[i] = log_reg(X, y_binary, learning_rate, max_iterations)
    return thetas


@click.command()
@click.option(
    "--path",
    default="datasets/dataset_train.csv",
    help="Path of the CSV data file",
)
@click.option("--lrnrt", default=0.1, help="Learning rate")
@click.option("--maxit", default=1000, help="Maximum number of iterations")
def main(path, lrnrt, maxit):
    try:
        X, y = get_data(path)
        X, y = normalize(X, y)

        thetas = one_vs_all(X, y, learning_rate=lrnrt, max_iterations=maxit)

        with open("thetas.pkl", "wb") as file:
            pkl.dump(thetas, file)

    except FileNotFoundError:
        print(f"Error: The file at path '{path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file at path '{path}' is empty or invalid.")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
