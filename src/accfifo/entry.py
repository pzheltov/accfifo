import datetime
import decimal
from decimal import Decimal

import moneyed
from moneyed import format_money
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table


def format_st(st: bool):
    return 'ST' if st else '  '

def get_tx(row: dict) -> str:
    if 'Lot' in row:
        return str(row['Lot'])
    if 'Tx' in row:
        return str(row['Tx'])
    return f'sh{int(row['Qty'])}'


def get_qty(row) -> int:
    qty = row['Qty']
    if qty == '':
        return 0
    return int(qty)


def get_date(row):
    try:
        return datetime.datetime.strptime(row['Date'], '%d-%b-%y')
    except ValueError:
        return datetime.datetime.strptime(row['Date'], '%d-%b-%Y')

def get_cost(row: dict) -> moneyed.Money:
    try:
        return moneyed.Money(row['Cost'], 'USD')
    except decimal.InvalidOperation as e:
        raise RuntimeError(f'Cannot convert {row}') from e

class Entry(object):
    """
    Defines an accounting entry.
    """
    tx: str
    quantity: Decimal
    price: moneyed.Money
    date: datetime.datetime

    def __init__(self, tx: str, quantity, price: moneyed.Money, date: datetime.datetime | None = None, factor=1, **kwargs):
        """
        Initializes an entry object with quantity, price and arbitrary
        data associated with the entry to be used post-fifo-accounting
        analysis purposes.

        Note the factor parameter. This parameter is applied to the price.
        """
        self.tx = tx
        self.quantity = quantity
        self.price = price
        self.factor = factor
        self.date = date
        self.data = kwargs

    @classmethod
    def from_row(cls, row: dict):
        return Entry(tx=get_tx(row),
                     quantity=get_qty(row),
                     price=get_cost(row),
                     date=get_date(row))

    def __repr__(self):
        money = format_money(self.price, locale='en_US')
        if self.date is None:
            return f"{self.quantity:10} @ {money :>6} tx {self.tx:>3}"
        else:
            return f"{self.quantity:10} @ {money :>6} on {self.date.date()} tx {self.tx:>3}"

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        my_table = Table("id", "qty", "price", "date", show_header=False, show_lines=False, show_edge=False)
        money = format_money(self.price, locale='en_US')
        my_table.add_row(f'{self.tx:>3}', f'{self.quantity:10}', f'{money:>6}', str(self.date.date()))
        yield my_table


    @property
    def size(self):
        return abs(self.quantity)

    @property
    def buy(self):
        return self.quantity > 0

    @property
    def sell(self):
        return not self.buy

    @property
    def zero(self):
        return self.quantity == 0

    @property
    def value(self):
        return self.quantity * self.price * self.factor

    def copy(self, quantity=None):
        return Entry(
            tx=self.tx,
            quantity=quantity or self.quantity,
            price=self.price,
            date=self.date,
            factor=self.factor,
            **self.data.copy()
        )
