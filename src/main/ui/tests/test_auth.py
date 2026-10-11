from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.pages.login_page import LoginPage
from playwright.sync_api import expect

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")

    page.locator(".inventory_item").first.wait_for(state="visible")

    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"


def test_login_locked_out_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    error_text = steps.login_page.get_error_text()
    login_page = LoginPage(page)
    expect(login_page.error_message).to_be_visible()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == "https://www.saucedemo.com/", "Ожидаем возврат на страницу логина"


def test_logout_visual_user(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)

    login.open_login_page().login("visual_user", "secret_sauce")
    assert catalog.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog.logout()
    assert page.url == login.LOGIN_URL, "Ожидаем возврат на страницу логина"