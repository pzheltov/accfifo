import csv

from accfifo.entry import Entry
from accfifo.fifo import FIFO


def read_csv(filename) -> FIFO:
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        entries = [Entry.from_row(row) for row in reader]
        for entry in entries:
            print(entry)
        return FIFO(entries)
