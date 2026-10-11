from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


class UserSession:
    def __init__(self, api_manager: ApiManager, actor: CreateUserRequest):
        self.api_manager = api_manager
        self.actor = actor

    def create_account(self):
        return self.api_manager.user_steps.create_account(self.actor)

    def deposit(self, deposit_request: DepositRequest):
        return self.api_manager.user_steps.deposit(self.actor, deposit_request)

    def deposit_invalid(self, deposit_request: DepositRequest):
        return self.api_manager.user_steps.deposit_invalid(self.actor, deposit_request)

    def transfer(self, transfer_request: TransferRequest):
        return self.api_manager.user_steps.transfer(self.actor, transfer_request)

    def transfer_invalid(self, transfer_request: TransferRequest, response_spec):
        return self.api_manager.user_steps.transfer_invalid(self.actor, transfer_request, response_spec)

    def request_credit(self, credit_request_request: CreditRequestRequest):
        return self.api_manager.user_steps.request_credit(self.actor, credit_request_request)

    def request_credit_invalid(self, credit_request_request: CreditRequestRequest, response_spec):
        return self.api_manager.user_steps.request_credit_invalid(self.actor, credit_request_request, response_spec)

    def repay_credit(self, credit_repay_request: CreditRepayRequest):
        return self.api_manager.user_steps.repay_credit(self.actor, credit_repay_request)

    def repay_credit_invalid(self, credit_repay_request: CreditRepayRequest, response_spec):
        return self.api_manager.user_steps.repay_credit_invalid(self.actor, credit_repay_request, response_spec)