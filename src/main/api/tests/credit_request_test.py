import pytest

from src.main.api.db.crud.credit_crud import CreditCrudDB
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize(
        "amount",
        [
            5000, 10000, 14999.9
        ]
    )
    def test_valid_credit_request(self, db_session, api_manager, create_credit_user_request, created_accounts, amount):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        created_accounts.append(account.id)

        credit_request_request = CreditRequestRequest(accountId=account.id, amount=amount, termMonths=12)
        response = api_manager.user_steps.request_credit(create_credit_user_request, credit_request_request)

        assert response.id == credit_request_request.accountId
        assert response.termMonths == credit_request_request.termMonths
        assert response.amount == credit_request_request.amount
        assert response.balance == credit_request_request.amount

    @pytest.mark.parametrize(
        "amount, use_missing_account, expected_spec",
        [
            (4999, False, ResponseSpecs.request_bad()),
            (15001, False, ResponseSpecs.request_bad()),
            (7000, True, ResponseSpecs.request_not_found()),
        ]
    )
    def test_invalid_credit_request(self, db_session, api_manager, create_credit_user_request, created_accounts,
                                    amount, use_missing_account: bool, expected_spec):
        if use_missing_account:
            account_id = 999999999
        else:
            account = api_manager.user_steps.create_account(create_credit_user_request)
            created_accounts.append(account.id)
            account_id = account.id

        credit_request_request = CreditRequestRequest(accountId=account_id, amount=amount, termMonths=12)
        api_manager.user_steps.request_credit_invalid(create_credit_user_request, credit_request_request, expected_spec)

        if not use_missing_account:
            credit_from_db = CreditCrudDB.get_credit_by_account_id(db_session, account_id)
            assert credit_from_db is None, "Кредит создан в БД, хотя запрос должен был быть отклонён"
