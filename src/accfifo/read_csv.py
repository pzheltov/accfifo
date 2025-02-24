import csv
import logging
import sys

from accfifo.entry import Entry
from accfifo.fifo import FIFO


def read_csv(log, filename) -> FIFO:
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        entries = [Entry.from_row(row) for row in reader]
        # for entry in entries:
        #     print(entry)
        return FIFO(entries)
