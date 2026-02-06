import csv
import math

import click


def check_csv(features, data):
    data_frame_keys = {
        "Index": str,
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

    if features != list(data_frame_keys.keys()):
        raise Exception("CSV Error: Wrong columns")

    for col, dtype in data_frame_keys.items():
        i = 0
        for elem in data[col]:
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


def compute_stats(features: list, data: dict):
    stats = {
        "count": [],
        "mean": [],
        "std": [],
        "min": [],
        "25%": [],
        "50%": [],
        "75%": [],
        "max": [],
    }

    for feature in features[6:]:
        column_data = data[feature]
        stats["count"].append(count(column_data))
        stats["mean"].append(mean(column_data))
        stats["std"].append(std(column_data))
        stats["min"].append(min(column_data))
        stats["25%"].append(percentile(column_data, 0.25))
        stats["50%"].append(percentile(column_data, 0.50))
        stats["75%"].append(percentile(column_data, 0.75))
        stats["max"].append(max(column_data))

    return stats


def print_statistics(features: list, stats: dict, round_value=False):
    stat_len = len(max(stats.keys(), key=len))
    feature_len = []

    print(" " * stat_len, end="  ")
    for i, feature in enumerate(features[6:]):
        if round_value:
            value_len = max(
                [len(str(round(stats[stat][i], 6))) for stat in stats]
                + [len(feature)]
            )
        else:
            value_len = max(
                [len(str(stats[stat][i])) for stat in stats] + [len(feature)]
            )
        feature_len.append(value_len)
        print(f"{feature:>{value_len}}", end="  ")
    print()

    for stat_name, values in stats.items():
        print(f"{stat_name:<{stat_len}}", end="  ")
        for i, value in enumerate(values):
            if round_value:
                print(f"{round(value, 6):>{feature_len[i]}}", end="  ")
            else:
                print(f"{value:>{feature_len[i]}}", end="  ")
        print()


@click.command()
@click.option(
    "--path",
    default="datasets/dataset_train.csv",
    help="Path of the CSV data file",
)
@click.option("--round", default=True, help="Round value in the table")
def main(path, round):
    try:
        features, data = read_csv(path)
        check_csv(features, data)
        stats = compute_stats(features, data)
        print_statistics(features, stats, round_value=bool(round))
    except FileNotFoundError:
        print(f"Error: The file at path '{path}' was not found.")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
