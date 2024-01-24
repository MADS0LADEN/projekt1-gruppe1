import csv
import os

# Get the directory of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the file
file_path = os.path.join(dir_path, "log.txt")

# Read and process data
csv_data = []
with open(file_path, "r") as file:
    for line in file:
        if " " not in line:  # Skip lines without a space
            continue
        timestamp, values = line.strip().split(" [", 1)  # Split at the first space
        timestamp = timestamp.split(" ")[1]  # Only keep the time part
        values = (
            values.replace("]", "").replace("'", "").split(", ")
        )  # Remove brackets, quotes and split at commas
        csv_data.append([timestamp] + values)  # Include timestamp

# Write to CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Value1", "Value2", "Value3"])  # Header
    writer.writerows(csv_data)  # Data
