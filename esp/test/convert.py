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
        line = (
            line.replace("[", "").replace("]", "").replace(" ", "_", 1)
        )  # Remove brackets
        timestamp, values = line.strip("\n").split(" ", 1)

        values_str = "".join(values)  # Convert list to string without any separator
        values = values_str.replace("'", "")
        end = f"{timestamp},{values.replace(' ', '')}"
        # print(end)
        # values = list(values)  # Convert string list to actual list
        csv_data.append(end)  # Include timestamp

# Write to CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Tidspunkt", "Roer", "Omgivelser", "Diff"])  # Header
    writer.writerows(csv_data)  # Data
