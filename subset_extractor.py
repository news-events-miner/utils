#!/usr/bin/env python
import datetime as dt
import sys
from functools import partial
from csv import DictReader, DictWriter


USAGE = '''
USAGE: ./subset_extractor.py input.csv output.csv left right
    input.csv - path to input file
    output.csv - path to output file
    left - start of filter time window (%Y-%m-%d)
    right - end of filter time window (%Y-%m-%d)
'''


def extract_subset(input_file: str, output_file: str,
                   pass_filter: callable, pre_sorted: bool) -> None:
    started = False

    with (open(input_file, 'r') as input_csv,
          open(output_file, 'w') as output_csv):
        reader = DictReader(input_csv)
        writer = DictWriter(output_csv, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            if pass_filter(row):
                started = True
                writer.writerow(row)
            # Reached subset end
            elif started and pre_sorted:
                break


def filter_by_date(row: dict[str, any], left: dt.date, right: dt.date,
                   date_format: str):
    row_dt = dt.datetime.strptime(row['date'], date_format)

    return left <= row_dt <= right


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(USAGE, file=sys.stderr)
        exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    left = sys.argv[3]
    right = sys.argv[4]

    date_format = '%Y-%m-%d %H:%M:%S'
    params_date_format = '%Y-%m-%d'

    left = dt.datetime.strptime(left, params_date_format)
    right = dt.datetime.strptime(right, params_date_format)

    apply = partial(filter_by_date, left=left, right=right,
                    date_format=date_format)

    extract_subset(input_csv, output_csv, apply, pre_sorted=True)
