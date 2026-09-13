from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.requesters.crud_requester import CrudRequester
import allure




class UserSteps(BaseSteps):
    @allure.step("Создание счёта пользователем {create_user_request}")
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    @allure.step("Пополнение счёта {deposit_request}")
    def deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password =create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    @allure.step("Попытка невалидного пополнения {deposit_request}")
    def deposit_invalid(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password =create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response

    @allure.step("Перевод {transfer_request}")
    def transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password =create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    @allure.step("Попытка невалидного перевода {transfer_request}")
    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest,
                         response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER,
            response_spec
        ).post(transfer_request)
        return response

    @allure.step("Попытка невалидного запроса кредита {credit_request_request}")
    def request_credit_invalid(self, create_user_request: CreateUserRequest,
                               credit_request_request: CreditRequestRequest, response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            response_spec
        ).post(credit_request_request)
        return response

    @allure.step("Запрос кредита {credit_request_request}")
    def request_credit(self, create_user_request: CreateUserRequest, credit_request_request: CreditRequestRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request_request)
        return response

    @allure.step("Погашение кредита {credit_repay_request}")
    def repay_credit(self, create_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    @allure.step("Попытка невалидного погашения кредита {credit_repay_request}")
    def repay_credit_invalid(self, create_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest,
                             response_spec):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREDIT_REPAY,
            response_spec
        ).post(credit_repay_request)
        return response