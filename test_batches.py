from datetime import date

from model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int) -> tuple[Batch, OrderLine]:
    batch = Batch('batch-001', sku, batch_qty, eta=date.today())
    line = OrderLine('order-123', sku, line_qty)
    return batch, line


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch('batch-001', 'SMALL-TABLE', qty=20, eta=date.today())
    line = OrderLine('order-ref', 'SMALL-TABLE', 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
