import pytest
from sqlalchemy.orm import Session
from typing import Callable, Tuple
from src.main.api.classes.user_session import UserSession
from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.generators.test_data_generator import CreditDataGenerator
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:
    def test_valid_credit_repay(
        self,
        db_session: Session,
        credit_user_session: UserSession,
        create_active_credit: Callable[..., Tuple[CreateAccountResponse, CreditRequestRequest, CreditRequestResponse]],
        build_partial_repay_request: Callable[[CreditRequestResponse, float], CreditRepayRequest],
    ):
        account, credit_request_request, credit_response = create_active_credit()
        credit_repay_request = build_partial_repay_request(credit_response, 1.0)

        credit_repay_response = credit_user_session.repay_credit(credit_repay_request)

        assert credit_repay_response.amountDeposited == credit_request_request.amount, "API вернул неверную зачисленную сумму погашения"
        assert credit_repay_response.creditId == credit_repay_request.creditId, "API вернул неверный creditId"

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance == 0, "Кредит погашен, но баланс в БД не обнулился"

    @pytest.mark.parametrize(
        "amount_factor, use_other_user, expected_spec",
        [
            (0.5, False, ResponseSpecs.request_unprocessable()),
            (1.0, True, ResponseSpecs.request_not_found()),
        ]
    )
    def test_invalid_credit_repay(
        self,
        db_session: Session,
        credit_user_session: UserSession,
        create_active_credit: Callable[..., Tuple[CreateAccountResponse, CreditRequestRequest, CreditRequestResponse]],
        create_credit_secret_session: Callable[[], UserSession],
        build_partial_repay_request: Callable[[CreditRequestResponse, float], CreditRepayRequest],
        amount_factor: float,
        use_other_user: bool,
        expected_spec: Callable,
    ):
        credit_amount = CreditDataGenerator.valid_amount()
        account, credit_request_request, credit_response = create_active_credit(amount=credit_amount)

        session = create_credit_secret_session() if use_other_user else credit_user_session
        credit_repay_request = build_partial_repay_request(credit_response, amount_factor)

        session.repay_credit_invalid(credit_repay_request, expected_spec)

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance == -credit_amount, "Долг изменился, хотя погашение должно было быть отклонено"