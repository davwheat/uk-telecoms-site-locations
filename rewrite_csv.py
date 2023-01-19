import csv


def main():
    reader = None

    with open("data.csv", "r") as f:
        # change the delimiter from the default comma to another delimiter
        reader = csv.reader(f, delimiter="*")

        with open("data_converted.csv", "w", newline="") as f2:
            writer = csv.writer(f2)
            writer.writerows(list(reader))


if __name__ == "__main__":
    main()
