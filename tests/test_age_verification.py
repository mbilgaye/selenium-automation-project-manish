import time

import pytest

from pages.login_page import LoginPage
from tests.test_data.age_verification_test_data import AGE_VERIFICATION_TEST_DATA, OVER_18_DOB
from tests.test_data.authentication_test_data import AUTHENTICATION_TEST_DATA


def test_age_verification_visible_on_visit(driver):
    login_page = LoginPage(driver).open(LoginPage.URL)
    homepage = login_page.login(AUTHENTICATION_TEST_DATA["valid_username"], AUTHENTICATION_TEST_DATA["valid_password"])
    shop_page = homepage.go_to_shop()
    assert shop_page.is_visible(shop_page.AGE_VERIFICATION_MODAL)


@pytest.mark.parametrize(
    "case_label, dob, verification_type, expected_message",
    AGE_VERIFICATION_TEST_DATA,
    ids=[case[0] for case in AGE_VERIFICATION_TEST_DATA],
)
def test_age_verification(driver, case_label, dob, verification_type, expected_message):
    login_page = LoginPage(driver).open(LoginPage.URL)
    homepage = login_page.login(AUTHENTICATION_TEST_DATA["valid_username"], AUTHENTICATION_TEST_DATA["valid_password"])
    shop_page = homepage.go_to_shop()
    assert shop_page.is_visible(shop_page.AGE_VERIFICATION_MODAL)

    shop_page.confirm_age_verification(dob)

    assert expected_message in shop_page.get_age_verification_message(verification_type)


def test_clearing_cookies_forces_reverification(driver):
    login_page = LoginPage(driver).open(LoginPage.URL)
    homepage = login_page.login(AUTHENTICATION_TEST_DATA["valid_username"], AUTHENTICATION_TEST_DATA["valid_password"])
    shop_page = homepage.go_to_shop()

    shop_page.confirm_age_verification(OVER_18_DOB)
    assert "You are of age" in shop_page.get_age_verification_message("success")
    shop_page.wait_for_age_verification_modal_hidden()
    shop_page.clear_cookies_and_session_storage()
    shop_page.refresh()
    # shop_page.go_to_alcohol_category()

    assert shop_page.is_visible(shop_page.AGE_VERIFICATION_MODAL)