import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize(
        "balance, amount",
        [
            (1000, 500),
            (6767, 1337)
        ]
    )
    def test_transfer_between_own_accounts_valid(self, db_session, api_manager, create_user_request, created_accounts,
                                                 create_funded_account, balance, amount):
        first_account = create_funded_account(balance)
        second_account = api_manager.user_steps.create_account(create_user_request)
        created_accounts.append(second_account.id)

        transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=amount)
        transfer_response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        first_account_from_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_from_db.balance == transfer_response.fromAccountIdBalance, "Баланс отправителя в БД не совпадает с тем, что вернул API"
        assert first_account_from_db.balance == balance - amount, "Баланс отправителя после перевода не соответствует ожидаемому (balance - amount)"
        assert second_account_from_db.balance == amount, "Баланс получателя после перевода не совпадает с переведённой суммой"
        assert transfer_response.fromAccountId == first_account.id, "API вернул неверный fromAccountId — перепутан счёт отправителя"
        assert transfer_response.toAccountId == second_account.id, "API вернул неверный toAccountId — перепутан счёт получателя"



    @pytest.mark.parametrize(
        "transfer_amount, use_missing_account, expected_spec",
        [
            (499.9, False, ResponseSpecs.request_bad()),
            (10000.01, False, ResponseSpecs.request_bad()),
            (6767, False, ResponseSpecs.request_unprocessable()),
            (6767, True,  ResponseSpecs.request_not_found())
        ]
    )
    def test_transfer_between_own_accounts_invalid(self, db_session, api_manager, create_user_request,
                                                   created_accounts, create_funded_account, transfer_amount,
                                                   use_missing_account, expected_spec):

        first_account = create_funded_account(5000)

        if use_missing_account:
            to_account_id = 999999999
        else:
            second_account = api_manager.user_steps.create_account(create_user_request)
            created_accounts.append(second_account.id)
            to_account_id = second_account.id

        transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=to_account_id, amount=transfer_amount)
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request, expected_spec)

        first_account_from_db = Account.get_account_by_id(db_session, first_account.id)

        assert first_account_from_db.balance == 5000, "Баланс отправителя изменился, хотя перевод должен был быть отклонён"

        if not use_missing_account:
            second_account_from_db = Account.get_account_by_id(db_session, to_account_id)
            assert second_account_from_db.balance == 0, "Баланс получателя изменился, хотя перевод должен был быть отклонён"