import csv

with open('amulets.csv') as inp, open('temp.csv', 'w', newline='') as out:
    reader = csv.reader(inp)
    writer = csv.writer(out, delimiter=',')
    # No need to use `insert(), `append()` simply use `+` to concatenate two lists.
    writer.writerow(['ID'] + next(reader))
    # Iterate over enumerate object of reader and pass the starting index as 1.
    writer.writerows([i] + row for i, row in enumerate(reader, 1))
