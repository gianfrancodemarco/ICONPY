import csv
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile


def all_files_in_path(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def writeCSV(filename, rows, headers=None, mode='w') -> None:
    """
  Writes a csv file at {filename}
  Writes headers as the first row, then writes headers
  """

    with open(filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if headers is not None:
            writer.writerow(headers)
        writer.writerows(rows)


def readCSVtoListOfDict(filename):
    """
    Reads csv file at {filename}
    :returns A list of dicts. The keys are the header of the csv
    """

    with open(filename, encoding='utf-8') as f:
        data = [row for row in csv.DictReader(f, skipinitialspace=True)]

    return data


def clear_string(filename, replacer='', extend_invalid=None):

    invalid = '<>:"/\|?* '

    if extend_invalid is not None:
        invalid += extend_invalid

    for char in invalid:
        filename = filename.replace(char, replacer)

    return filename


def create_zip_file(filename, source_path, source_files):

    # create a ZipFile object
    with ZipFile(filename, 'w') as zipObj:

        # Add multiple files to the zip
        for file in source_files:
            zipObj.write(f'{source_path}/{file}', file)

