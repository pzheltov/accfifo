import datetime
import os

import cloup
from moneyed import format_money

from rich.console import Console
from rich.table import Table

from accfifo.entry import format_st
from accfifo.fifo import FIFO
from accfifo.munch import Munch
from accfifo.read_csv import read_csv
from accfifo.tax_row import TaxRow, trace_table


@cloup.command()
@cloup.option('-f', '--filename', type=str, default='../../yy.csv', help='Read data from a .csv')
@cloup.option('--format', type=str, default='', help='Tabulate output. rich|plain')
@cloup.version_option('0.2')
def cli(filename: str, format: str):

    fifo = read_csv(filename)

    if format == 'rich':
        console = Console()
        print('All transactions')
        console.print(trace_table(fifo.trace))
        print('All transactions grouped by type (ST/LT)')
        console.print(tax_table(fifo))
        for tax_row in fifo.group_as_tax_rows():
            print(f'Out tx #{tax_row.tx}, {"ST" if tax_row.st else "LT"}, proceeds {tax_row.proceeds()}, cost basis {tax_row.cb()}')
            console.print(tax_row)
            print('\n')
    else:
        print("Available Stock          : ", fifo.stock)
        print("Stock Valuation          : ", fifo.valuation)
        print("Factored Average Cost    : ", fifo.avgcost)
        print("Factored Stock Valuation : ", fifo.valuation_factored)
        print("Average Cost             : ", fifo.avgcost_factored)
        print("Trace Length             : ", len(fifo.trace))
        print("Total Runtime            : ", fifo.runtime)

        for element in fifo.trace:
            print(element)
        for tax_row in fifo.group_as_tax_rows():
            print(tax_row)


def tax_table(fifo: FIFO):
    """Group munches into tax rows identified by (tx, st) pair"""
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('tx')
    table.add_column('qty')
    table.add_column('st')
    table.add_column('proceeds',  justify="right")
    table.add_column('cb', justify="right")
    tax_row: TaxRow
    for tax_row in fifo.group_as_tax_rows():
        tx = tax_row.tx
        qty = str(tax_row.qty())
        st = format_st(tax_row.st)
        proceeds = format_money(tax_row.proceeds())
        cb = format_money(tax_row.cb())
        table.add_row(tx, qty, st,  proceeds, str(cb))
    return table


if __name__ == '__main__':
    print(os.getcwd())
    cli()
