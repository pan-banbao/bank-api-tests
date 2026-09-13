import pytest

from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRepay:
    def test_valid_credit_repay(self, db_session, api_manager, create_credit_user_request, created_accounts):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        created_accounts.append(account.id)

        credit_request_request = CreditRequestRequest(accountId=account.id, amount=5000, termMonths = 12)
        credit_response = api_manager.user_steps.request_credit(create_credit_user_request, credit_request_request)

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=credit_request_request.amount
        )

        credit_repay_response = api_manager.user_steps.repay_credit(create_credit_user_request, credit_repay_request)

        assert credit_repay_response.amountDeposited == credit_request_request.amount, "API вернул неверную зачисленную сумму погашения"
        assert credit_repay_response.creditId == credit_repay_request.creditId, "API вернул неверный creditId в ответе на погашение"

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance == 0, "Кредит погашен, но баланс в БД не обнулился"

    @pytest.mark.parametrize(
        "amount_factor, use_other_user, expected_spec",
        [
            (0.5, False, ResponseSpecs.request_unprocessable()),
            (1.0, True, ResponseSpecs.request_not_found()),
        ]
    )
    def test_invalid_credit_repay(self, db_session, api_manager, create_credit_user_request, created_accounts,
                                  amount_factor, use_other_user, expected_spec):
        account = api_manager.user_steps.create_account(create_credit_user_request)
        created_accounts.append(account.id)

        credit_request_request = CreditRequestRequest(accountId=account.id, amount=5000, termMonths=12)
        credit_response = api_manager.user_steps.request_credit(create_credit_user_request, credit_request_request)

        first_user = create_credit_user_request
        if use_other_user:
            second_user = RandomModelGenerator.generate(CreateUserRequest)
            second_user.role = "ROLE_CREDIT_SECRET"
            api_manager.admin_steps.create_user(second_user)
            first_user = second_user

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account.id,
            amount=credit_request_request.amount * amount_factor
        )
        api_manager.user_steps.repay_credit_invalid(first_user, credit_repay_request, expected_spec)

        credit_from_db = CreditCrudDB.get_credit_by_id(db_session, credit_response.creditId)
        assert credit_from_db.balance == -5000, "Долг изменился, хотя погашение должно было быть отклонено"
