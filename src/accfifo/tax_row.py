from decimal import Decimal

from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment
from rich.table import Table

from accfifo.entry import format_st
from accfifo.munch import Munch

from moneyed import format_money, Money

class TaxRow:
    tx: str
    st: bool
    lots: list[Munch]

    def __init__(self):
        self.tx = ""
        self.st = False
        self.lots = []

    def append(self, m: Munch):
        if len(self.lots) == 0:
            self.tx = m.out_tx()
            self.st = m.st()
        self.lots.append(m)

    def qty(self) -> Decimal:
        # noinspection PyTypeChecker
        return sum([m.qty() for m in self.lots])

    def cb(self) -> Money:
        # noinspection PyTypeChecker
        return sum([m.cb() for m in self.lots])

    def proceeds(self) -> Money:
        # noinspection PyTypeChecker
        return -sum([m.proceeds() for m in self.lots])

    def __str__(self):
        st = format_st(self.st)
        cb = format_money(self.cb())
        proceeds = format_money(self.proceeds())
        return f'TaxRow(out.tx={self.tx}, {st} cb={cb:>12}  proceeds={proceeds:>12}): \n{"\n".join([str(m) for m in self.lots])}'

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # st = format_st(self.st)
        # cb = format_money(self.cb(), locale='en_US')
        # proceeds = format_money(self.proceeds())
        yield trace_table(self.lots)

def trace_table(trace: list[Munch]) -> Table:
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('in')
    table.add_column('out')
    table.add_column('st')
    for m in trace:
        (_in, _out) = m
        st = format_st(m.st())
        table.add_row(_in, _out, st)
    return table


