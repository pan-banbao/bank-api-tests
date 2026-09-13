import pytest
from typing import List

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def created_accounts(db_session):
    account_ids: List[int] = []
    yield account_ids
    for account_id in account_ids:
        TransactionCrudDb.delete_by_account_id(db_session, account_id)
        CreditCrudDB.delete_by_account_id(db_session, account_id)
        AccountCrudDb.delete_account(db_session, account_id)


@pytest.fixture
def create_funded_account(api_manager, create_user_request, created_accounts):
    def _create_funded_account(balance):
        account = api_manager.user_steps.create_account(create_user_request)
        created_accounts.append(account.id)
        deposit_request = DepositRequest(accountId=account.id, amount=balance)
        api_manager.user_steps.deposit(create_user_request, deposit_request)
        return account
    return _create_funded_account