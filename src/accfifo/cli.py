import datetime
import os

import cloup
from moneyed import format_money

from rich.console import Console
from rich.table import Table

from accfifo.entry import format_st
from accfifo.fifo import FIFO
from accfifo.read_csv import read_csv
from accfifo.tax_row import TaxRow


@cloup.command()
@cloup.option('-f', '--filename', type=str, default='../../yy.csv', help='Read data from a .csv')
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
        console = Console()
        console.print(trace_table(fifo))
        console.print(tax_table(fifo))
    else:
        for element in fifo.trace:
            print(element)
        for tax_row in fifo.group_as_tax_rows():
            print(tax_row)


def tax_table(fifo: FIFO):
    """Group munches into tax rows identified by (tx, st) pair"""
    table = Table(show_header=True, header_style='bold magenta', box=None)
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


def trace_table(fifo):
    table = Table(show_header=True, header_style='bold magenta', box=None)
    table.add_column('in')
    table.add_column('out')
    table.add_column('st')
    for m in fifo.trace:
        (_in, _out) = m
        st = format_st(m.st())
        table.add_row(_in, _out, st)
    return table


if __name__ == '__main__':
    print(os.getcwd())
    cli()
