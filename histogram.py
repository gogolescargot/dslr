#!/usr/bin/python3

import signal

import click
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb


def check_csv(data_frame):
    data_frame_keys = {
        "Hogwarts House": object,
        "First Name": object,
        "Last Name": object,
        "Birthday": object,
        "Best Hand": object,
        "Arithmancy": float,
        "Astronomy": float,
        "Herbology": float,
        "Defense Against the Dark Arts": float,
        "Divination": float,
        "Muggle Studies": float,
        "Ancient Runes": float,
        "History of Magic": float,
        "Transfiguration": float,
        "Potions": float,
        "Care of Magical Creatures": float,
        "Charms": float,
        "Flying": float,
    }

    if list(data_frame.columns) != list(data_frame_keys.keys()):
        raise Exception("CSV Error: Wrong columns")

    for col, dtype in data_frame_keys.items():
        i = 0
        for elem in data_frame[col]:
            if not isinstance(elem, dtype):
                raise Exception(
                    f"CSV Error: wrong element type: find in {col}: type {type(elem)}, expected {dtype}"
                )
            if col == "Hogwarts House" and elem not in [
                "Ravenclaw",
                "Slytherin",
                "Hufflepuff",
                "Gryffindor",
            ]:
                raise Exception(
                    f"CSV Error: wrong hogwarts house: line {i}, find {elem}, expected Ravenclaw, Slytherin, Hufflepuff or Gryffindor"
                )
            if col == "Best Hand" and elem not in ["Left", "Right"]:
                raise Exception(
                    f"CSV Error: wrong best hand: line {i}, find {elem}, expected Left or Right"
                )
            i += 1
    return 0


@click.command()
@click.option(
    "--path",
    default="datasets/dataset_train.csv",
    help="Path of the CSV data file",
)
def main(path):
    try:
        signal.signal(
            signal.SIGINT,
            lambda *_: (
                print("\033[2DDSLR: CTRL+C sent by user."),
                exit(1),
            ),
        )
        data_frame = pd.read_csv(path, index_col="Index")
        check_csv(data_frame)

        for course in data_frame.keys()[5:]:
            sb.histplot(
                data=data_frame,
                x=course,
                hue="Hogwarts House",
                multiple="stack",
                stat="count",
            )
            plt.title(f"Histogram of {course} Scores by Hogwarts House")
            plt.xlabel(f"{course} Score")
            plt.ylabel("Count")
            plt.show()
    except FileNotFoundError:
        print(f"Error: File not found at path '{path}'")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
