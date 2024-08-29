from decimal import Decimal

from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment

from accfifo.entry import format_st
from accfifo.munch import Munch

from moneyed import format_money, Money

class TaxRow(list[Munch]):
    tx: str
    st: bool

    def __init__(self):
        super().__init__()
        self.tx = ""
        self.st = False

    def append(self, m: Munch):
        if len(self) == 0:
            self.tx = m.out_tx()
            self.st = m.st()
        super().append(m)

    def qty(self) -> Decimal:
        # noinspection PyTypeChecker
        return sum([m.qty() for m in self])

    def cb(self) -> Money:
        # noinspection PyTypeChecker
        return sum([m.cb() for m in self])

    def proceeds(self) -> Money:
        # noinspection PyTypeChecker
        return -sum([m.proceeds() for m in self])

    def __str__(self):
        st = format_st(self.st)
        cb = format_money(self.cb())
        proceeds = format_money(self.proceeds())
        return f'TaxRow(out.tx={self.tx}, {st} cb={cb:>12}  proceeds={proceeds:>12})[{len(self)}]'

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        st = format_st(self.st)
        cb = format_money(self.cb())
        proceeds = format_money(self.proceeds())
        yield Segment(self.tx)
        yield Segment(st)
        yield Segment(cb)
        yield Segment(proceeds)
