from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction



class TransactionCrudDb:
    @staticmethod
    def delete_by_account_id(db: Session, account_id: int) -> None:
        db.query(Transaction).filter(
            (Transaction.to_account_id == account_id) | (Transaction.from_account_id == account_id)
        ).delete(synchronize_session=False)
        db.commit()