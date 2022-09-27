from sqlalchemy.orm import Session

import model


class SqlAlchemyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, batch: model.Batch) -> None:
        self.session.add(batch)

    def get(self, reference: str) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()
