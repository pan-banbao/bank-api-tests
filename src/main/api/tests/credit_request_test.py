import pytest
from sqlalchemy.orm import Session
from typing import Callable
from src.main.api.classes.user_session import UserSession
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.generators.test_data_generator import CreditDataGenerator, MISSING_ACCOUNT_ID


@pytest.mark.api
class TestCreditRequest:
    def test_valid_credit_request(
        self,
        db_session: Session,
        credit_user_session: UserSession,
        created_credit_account: CreateAccountResponse,
    ):
        amount = CreditDataGenerator.valid_amount()
        term_months = CreditDataGenerator.valid_term_months()

        credit_request_request = CreditRequestRequest(accountId=created_credit_account.id, amount=amount, termMonths=term_months)
        response = credit_user_session.request_credit(credit_request_request)

        credit_from_db = CreditCrudDB.get_credit_by_account_id(db_session, created_credit_account.id)

        assert response.id == credit_request_request.accountId, "API вернул неверный accountId"
        assert response.termMonths == credit_request_request.termMonths, "API вернул неверный срок кредита"
        assert response.amount == credit_request_request.amount, "API вернул неверную сумму кредита"
        assert response.balance == credit_request_request.amount, "Баланс после выдачи кредита не совпадает с суммой"

        assert credit_from_db is not None, "Кредит одобрен, но записи в БД нет"
        assert credit_from_db.amount == amount, "Сумма кредита в БД не совпадает с запрошенной"
        assert credit_from_db.term_months == term_months, "Срок кредита в БД не совпадает с запрошенным"
        assert credit_from_db.account_id == created_credit_account.id, "Кредит привязан не к тому счёту"

    @pytest.mark.parametrize(
        "use_missing_account, expected_spec",
        [
            (False, ResponseSpecs.request_bad()),
            (True, ResponseSpecs.request_not_found()),
        ]
    )
    def test_invalid_credit_request(
        self,
        db_session: Session,
        credit_user_session: UserSession,
        created_credit_account: CreateAccountResponse,
        use_missing_account: bool,
        expected_spec: Callable,
    ):
        amount = CreditDataGenerator.invalid_amount() if not use_missing_account else CreditDataGenerator.valid_amount()
        account_id = MISSING_ACCOUNT_ID if use_missing_account else created_credit_account.id

        credit_request_request = CreditRequestRequest(accountId=account_id, amount=amount, termMonths=CreditDataGenerator.valid_term_months())
        credit_user_session.request_credit_invalid(credit_request_request, expected_spec)

        if not use_missing_account:
            credit_from_db = CreditCrudDB.get_credit_by_account_id(db_session, account_id)
            assert credit_from_db is None, "Кредит создан в БД, хотя запрос должен был быть отклонён"