from sqlalchemy.orm import Session

import model
import repository


def insert_order_line(session: Session) -> int:
    session.execute('INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "GENERIC-SOFA", 12)')
    [[order_line_id]] = session.execute(
        'SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku',
        {'orderid': 'order1', 'sku': 'GENERIC-SOFA'},
    )
    return order_line_id


def insert_batch(session: Session, batch_id: str) -> int:
    session.execute(
        'INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        {'batch_id': batch_id},
    )
    [[batch]] = session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"', {'batch_id': batch_id},
    )
    return batch


def insert_allocation(session: Session, order_line_id: int, batch_id: int) -> None:
    session.execute(
        'INSERT INTO allocations (order_line_id, batch_id) VALUES (:order_line_id, :batch_id)',
        {'order_line_id': order_line_id, 'batch_id': batch_id},
    )


def test_repository_can_save_a_batch(session):
    batch = model.Batch('batch1', 'RUSTY-SOAPDISH', 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = list(session.execute('SELECT reference, sku, _purchased_quantity, eta FROM "batches"'))
    assert rows == [('batch1', 'RUSTY-SOAPDISH', 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    order_line_id = insert_order_line(session)
    batch_id = insert_batch(session, 'batch')
    insert_batch(session, 'batch2')
    insert_allocation(session, order_line_id, batch_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get('batch')

    expected = model.Batch('batch', 'GENERIC-SOFA', 100, eta=None)
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {model.OrderLine('order1', 'GENERIC-SOFA', 12)}
