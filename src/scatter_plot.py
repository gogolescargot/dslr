import signal
from itertools import combinations

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
                    f"CSV Error: wrong element type: find in {col}: \
type {type(elem)}, expected {dtype}"
                )
            if col == "Hogwarts House" and elem not in [
                "Ravenclaw",
                "Slytherin",
                "Hufflepuff",
                "Gryffindor",
            ]:
                raise Exception(
                    f"CSV Error: wrong hogwarts house: line {i}, find {elem}, \
expected Ravenclaw, Slytherin, Hufflepuff or Gryffindor"
                )
            if col == "Best Hand" and elem not in ["Left", "Right"]:
                raise Exception(
                    f"CSV Error: wrong best hand: line {i}, find {elem}, \
expected Left or Right"
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

        for course_1, course_2 in combinations(data_frame.keys()[5:], 2):
            sb.scatterplot(
                data=data_frame,
                x=data_frame[course_1],
                y=data_frame[course_2],
                hue="Hogwarts House",
            )
            plt.title(f"Scatter Plot of {course_1} and {course_2}")
            plt.xlabel(f"{course_1} Score")
            plt.ylabel(f"{course_2} Score")
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file at path '{path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file at path '{path}' is empty or invalid.")
    except KeyError as e:
        print(f"Error: Missing key in the data file: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
