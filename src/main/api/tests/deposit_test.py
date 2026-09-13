import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest



@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "amount",
        [
            1000, 6767.67 ,9000
        ]
    )
    def test_valid_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, created_accounts, amount: int | float):
        response = api_manager.user_steps.create_account(create_user_request)
        created_accounts.append(response.id)
        deposit_request = DepositRequest(accountId=response.id, amount=amount)
        deposit_response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        account_from_db = Account.get_account_by_id(db_session, response.id)

        assert account_from_db.balance == response.balance + deposit_request.amount, "Валидный депозит не прошел в БД. Ошибка."
        assert deposit_response.balance == response.balance + deposit_request.amount, "Валидный депозит не прошел. Ошибка"


    @pytest.mark.parametrize(
        "amount",
        [
            -67, 0, 500, 999, 999.01, 9000.01, 10000,
        ]
    )
    def test_invalid_deposit(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, created_accounts, amount: int | float):
        response = api_manager.user_steps.create_account(create_user_request)
        created_accounts.append(response.id)
        deposit_request = DepositRequest(accountId=response.id, amount=amount)
        api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)

        account_from_db = Account.get_account_by_id(db_session, response.id)

        assert account_from_db.balance == response.balance, "Баланс изменился после отклонённого депозита. Ошибка"
