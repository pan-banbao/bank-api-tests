import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.user_session import UserSession
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.generators.test_data_generator import DepositDataGenerator


@pytest.mark.api
class TestDeposit:
    def test_valid_deposit(self, db_session: Session, user_session: UserSession, created_account: CreateAccountResponse):
        amount = DepositDataGenerator.valid_amount()
        deposit_request = DepositRequest(accountId=created_account.id, amount=amount)
        deposit_response = user_session.deposit(deposit_request)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == created_account.balance + amount, "Баланс в БД не совпадает с ожидаемым после депозита"
        assert deposit_response.balance == created_account.balance + amount, "API вернул неверный баланс после депозита"
        assert deposit_response.id == created_account.id, "API вернул данные другого счёта"

    def test_invalid_deposit(self, db_session: Session, user_session: UserSession, created_account: CreateAccountResponse):
        amount = DepositDataGenerator.invalid_amount()
        deposit_request = DepositRequest(accountId=created_account.id, amount=amount)
        user_session.deposit_invalid(deposit_request)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == created_account.balance, "Баланс изменился, хотя невалидный депозит должен был быть отклонён"