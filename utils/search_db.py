import csv
from difflib import get_close_matches

def find_closest_match(query, csv_file, n=3):
    matches = []
    results = {}
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        query = query.lower()
        for row in reader:
            if len(row) >= 4:
                concat_string = (row[1] + " " + row[2])
                matches.append(concat_string.lower())
                results[concat_string.lower()] = [concat_string, row[-1]]
    closest_match = get_close_matches(query, matches, n=n, cutoff=0.6)
    return [results[c][0] for c in closest_match], [results[c][1] for c in closest_match]