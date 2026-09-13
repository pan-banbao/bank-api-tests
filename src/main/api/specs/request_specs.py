from src.main.api.models.login_user_request import LoginUserRequest
import requests
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.configs.config import Config

class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str, role: str = "ADMIN"):
        user_data = LoginUserRequest(username=username, password=password, role=role)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=user_data.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()