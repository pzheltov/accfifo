import datetime
import os

import cloup

from rich.console import Console
from rich.table import Table
from accfifo.read_csv import read_csv


@cloup.command()
@cloup.option('-f', '--filename', type=str, default='../pltr.csv', help='Read data from a .csv')
@cloup.option('--format', type=str, default='', help='Tabulate output. rich|plain')
@cloup.version_option('0.2')
def cli(filename: str, format: str):

    fifo = read_csv(filename)

    print("Available Stock          : ", fifo.stock)
    print("Stock Valuation          : ", fifo.valuation)
    print("Factored Average Cost    : ", fifo.avgcost)
    print("Factored Stock Valuation : ", fifo.valuation_factored)
    print("Average Cost             : ", fifo.avgcost_factored)
    print("Trace Length             : ", len(fifo.trace))
    print("Total Runtime            : ", fifo.runtime)
    if format == 'rich':
        table = Table(show_header=True, header_style='bold magenta', box=None)
        table.add_column('in')
        table.add_column('out')
        table.add_column('st')
        for m in fifo.trace:
            (_in, _out) = m
            table.add_row(_in, _out, f'{m.st()}')
        console = Console()
        console.print(table)
    else:
        for element in fifo.trace:
            print(element)


if __name__ == '__main__':
    print(os.getcwd())
    cli()