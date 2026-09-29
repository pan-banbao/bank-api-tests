import pytest
from src.main.api.classes.user_session import UserSession
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def user_session(api_manager, create_user_request) -> UserSession:
    return UserSession(api_manager, create_user_request)


@pytest.fixture
def credit_user_session(api_manager, create_credit_user_request) -> UserSession:
    return UserSession(api_manager, create_credit_user_request)


@pytest.fixture
def create_credit_secret_session(api_manager):
    def _create() -> UserSession:
        user = RandomModelGenerator.generate(CreateUserRequest)
        user.role = "ROLE_CREDIT_SECRET"
        api_manager.admin_steps.create_user(user)
        return UserSession(api_manager, user)
    return _create