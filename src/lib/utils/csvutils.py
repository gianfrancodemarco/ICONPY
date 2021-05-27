import csv


def writeCSV(filename, rows, headers=None, mode='w') -> None:
    """
  Writes a csv file at {filename}
  Writes headers as the first row, then writes headers
  """

    with open(filename, mode, newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if headers is not None:
            writer.writerow(headers)
        writer.writerows(rows)


def readCSVtoObj(filename, keys):
    """
    Reads csv file at {filename}
    Returns a list of objects mapped into {keys}
    """
    with open(filename, newline='', encoding="UTF-8") as f:
        reader = csv.reader(f, delimiter=",")
        data = []
        # for each row, add a new object to data
        for row in reader:
            i = 0
            obj = {}
            for key in keys:
                obj[key] = row[i]
                i += 1
            data.append(obj)
    return data
