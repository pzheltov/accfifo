import datetime

from moneyed import format_money
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from accfifo.entry import Entry


class Munch(tuple[Entry, Entry]):

    def __str__(self):
        _in: Entry = self[0]
        _out: Entry = self[1]
        cb = format_money(_in.price * _in.quantity, locale='en_US', currency_digits=False)
        proc = format_money(_out.price * _out.quantity, locale='en_US')
        return f"({_in}, CB = {cb:>12}, {_out}), {self.st()}, Proceeds {proc:>8}"

    def st(self):
        return 'ST' if self.term() <= datetime.timedelta(days=365) else '  '

    def term(self):
        return self[1].date - self[0].date

    def cb(self):
        _in = self[0]
        return _in.price * _in.quantity

    def proceeds(self):
        _out = self[1]
        return _out.price * _out.quantity

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Munch:[/b]"
        my_table = Table("In", "Out")
        my_table.add_row(self[0])
        my_table.add_row(self[1])
        yield my_table
