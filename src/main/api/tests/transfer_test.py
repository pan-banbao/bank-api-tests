import pytest
from sqlalchemy.orm import Session
from typing import Callable, Tuple
from src.main.api.classes.user_session import UserSession
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.generators.test_data_generator import TransferDataGenerator, DepositDataGenerator, MISSING_ACCOUNT_ID


@pytest.mark.api
class TestTransfer:
    def test_transfer_between_own_accounts_valid(
        self,
        db_session: Session,
        user_session: UserSession,
        valid_transfer_setup: Tuple[CreateAccountResponse, CreateAccountResponse, float, float],
    ):
        first_account, second_account, funded_amount, amount = valid_transfer_setup

        transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=amount)
        transfer_response = user_session.transfer(transfer_request)

        first_account_from_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account.id)

        assert float(first_account_from_db.balance) == pytest.approx(float(transfer_response.fromAccountIdBalance)), "Баланс отправителя в БД не совпадает с ответом API"
        assert float(first_account_from_db.balance) == pytest.approx(funded_amount - amount), "Баланс отправителя не соответствует ожидаемому"
        assert float(second_account_from_db.balance) == pytest.approx(amount), "Баланс получателя не совпадает с переведённой суммой"
        assert transfer_response.fromAccountId == first_account.id, "API перепутал счёт отправителя"
        assert transfer_response.toAccountId == second_account.id, "API перепутал счёт получателя"

    @pytest.mark.parametrize(
        "transfer_amount, use_missing_account, expected_spec",
        [
            (TransferDataGenerator.MIN_AMOUNT - 0.1, False, ResponseSpecs.request_bad()),
            (TransferDataGenerator.MAX_AMOUNT + 0.01, False, ResponseSpecs.request_bad()),
            (DepositDataGenerator.MAX_AMOUNT + 1, False, ResponseSpecs.request_unprocessable()),
            (TransferDataGenerator.MIN_AMOUNT, True, ResponseSpecs.request_not_found()),
        ]
    )
    def test_transfer_between_own_accounts_invalid(
        self,
        db_session: Session,
        user_session: UserSession,
        max_funded_account: CreateAccountResponse,
        created_account: CreateAccountResponse,
        transfer_amount: float,
        use_missing_account: bool,
        expected_spec: Callable,
    ):
        to_account_id = MISSING_ACCOUNT_ID if use_missing_account else created_account.id

        transfer_request = TransferRequest(fromAccountId=max_funded_account.id, toAccountId=to_account_id, amount=transfer_amount)
        user_session.transfer_invalid(transfer_request, expected_spec)

        first_account_from_db = Account.get_account_by_id(db_session, max_funded_account.id)

        assert float(first_account_from_db.balance) == pytest.approx(float(DepositDataGenerator.MAX_AMOUNT)), "Баланс отправителя изменился, хотя перевод должен был быть отклонён"

        if not use_missing_account:
            second_account_from_db = Account.get_account_by_id(db_session, to_account_id)
            assert float(second_account_from_db.balance) == 0, "Баланс получателя изменился, хотя перевод должен был быть отклонён"