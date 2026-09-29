import pytest
from typing import List

from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.generators.test_data_generator import CreditDataGenerator, DepositDataGenerator, TransferDataGenerator


@pytest.fixture
def created_accounts(db_session):
    account_ids: List[int] = []
    yield account_ids
    for account_id in account_ids:
        TransactionCrudDb.delete_by_account_id(db_session, account_id)
        CreditCrudDB.delete_by_account_id(db_session, account_id)
        AccountCrudDb.delete_account(db_session, account_id)


@pytest.fixture
def created_account(user_session, created_accounts):
    account = user_session.create_account()
    created_accounts.append(account.id)
    return account


@pytest.fixture
def created_credit_account(credit_user_session, created_accounts):
    account = credit_user_session.create_account()
    created_accounts.append(account.id)
    return account


@pytest.fixture
def create_funded_account(user_session, created_accounts):
    def _create_funded_account(balance):
        account = user_session.create_account()
        created_accounts.append(account.id)
        deposit_request = DepositRequest(accountId=account.id, amount=balance)
        user_session.deposit(deposit_request)
        return account
    return _create_funded_account


@pytest.fixture
def max_funded_account(create_funded_account):
    return create_funded_account(DepositDataGenerator.MAX_AMOUNT)


@pytest.fixture
def valid_transfer_setup(create_funded_account, created_account):
    funded_amount = DepositDataGenerator.valid_amount()
    amount = TransferDataGenerator.valid_amount_up_to(funded_amount)
    first_account = create_funded_account(funded_amount)
    return first_account, created_account, funded_amount, amount


@pytest.fixture
def create_active_credit(credit_user_session, created_accounts):
    def _create_active_credit(amount=None, term_months=None) -> tuple:
        amount = amount or CreditDataGenerator.valid_amount()
        term_months = term_months or CreditDataGenerator.valid_term_months()

        account = credit_user_session.create_account()
        created_accounts.append(account.id)

        credit_request_request = CreditRequestRequest(accountId=account.id, amount=amount, termMonths=term_months)
        credit_response = credit_user_session.request_credit(credit_request_request)

        return account, credit_request_request, credit_response
    return _create_active_credit


@pytest.fixture
def build_partial_repay_request():
    def _build(credit_response: CreditRequestResponse, amount_factor: float) -> CreditRepayRequest:
        return CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=credit_response.id,
            amount=credit_response.amount * amount_factor
        )
    return _build