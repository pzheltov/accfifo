import datetime

from moneyed import format_money, Money
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from accfifo.entry import Entry, format_st


class Munch(tuple[Entry, Entry]):

    def __str__(self):
        _in: Entry = self[0]
        _out: Entry = self[1]
        cb = format_money(_in.price * _in.quantity, locale='en_US', currency_digits=False)
        proc = format_money(-_out.price * _out.quantity, locale='en_US')
        st = format_st(self.st())
        qty = self.qty()
        return f"({_in}, sh {qty}, CB = {cb:>12}, {_out}), {st}, Proceeds {proc:>12}"

    def st(self):
        return self.term() <= datetime.timedelta(days=365)

    def qty(self):
        _in: Entry = self[0]
        _out: Entry = self[1]
        assert _in.quantity == -_out.quantity, f"Unequal tx: in={_in.quantity} out={_out.quantity}"
        return _in.quantity

    def term(self):
        return self[1].date - self[0].date

    def out_tx(self):
        _out = self[1]
        return _out.tx


    def cb(self) -> Money:
        _in = self[0]
        # return Money(_in.price * _in.quantity, currency=_in.price.currency)
        return _in.quantity * _in.price

    def proceeds(self) -> Money:
        _out = self[1]
        return _out.quantity * _out.price
        # return Money(_out.price * _out.quantity, currency=_out.price.currency)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Munch:[/b]"
        my_table = Table("In", "Out")
        my_table.add_row(self[0])
        my_table.add_row(self[1])
        yield my_table
